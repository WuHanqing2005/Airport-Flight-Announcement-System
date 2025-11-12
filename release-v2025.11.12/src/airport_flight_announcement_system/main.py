# -*- coding:utf-8 -*-
# Software Name: Airport Flight Announcement System (Web Edition)
# Version: 2025.11.12 (Web + Flask + SocketIO) - Threading Stable
# Copyright: Wu Hanqing
# Unauthorized use is prohibited. Infringement will be prosecuted.
#
# CHANGE LOG (v2.3):
# - CRITICAL FIX: Switched from 'eventlet' to 'threading' async_mode for maximum PyInstaller compatibility.
# - REMOVED: All eventlet monkey_patching and related dependencies.
# - UPDATED: Replaced all eventlet.event.Event with standard threading.Event and its methods (.is_set(), .set()).
#
# Notes:
# - The latest pydub no longer bundles pyaudioop. If you encounter compatibility errors, install:
#   python -m pip install pydub audioop-lts
#
# Use this command to run the app in development mode:
#   poetry run python -m src.airport_flight_announcement_system.main
#
# To build a release executable with embedded dependencies, use:
#   .\release\Scripts\pip.exe install -r requirements.txt --ignore-installed

"""
Airport Flight Announcement System (Web Edition)

This module provides a Flask-based web application with Socket.IO real-time updates for
managing airport flight data and synthesizing announcement audio from pre-recorded
audio snippets. It includes endpoints for CRUD operations on flight data, audio synthesis,
cache clearing, stereo conversion utilities, and live log streaming to the browser.

Key Technologies:
- Flask for the web server
- Flask-SocketIO with threading for real-time communication
- pandas for Excel I/O
- pydub for audio processing

Quick Start:
1) Ensure Python dependencies are installed (pydub, flask, flask-socketio, pandas, openpyxl).
2) Ensure ffmpeg is installed and available on PATH for pydub to export .wav files.
3) Launch the app:
   python -m airport_flight_announcement_system.main
4) The application will open in a browser at http://127.0.0.1:5000

Folder Structure (relative to project root):
- data/       : Contains data.xlsx (flight data)
- output/     : Contains generated .wav announcement files
- material/   : Contains audio materials (alnum_*, airlines_*, cityname_*, delay_reason_*, template_*, etc.)
- templates/  : Flask HTML templates (index.html)
- static/     : Static web assets

"""

# --- Standard Library Imports ---
import os
import time
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import webbrowser
import threading
from pathlib import Path

# Compute the application root directory in a robust way
# This is the directory where main.py resides. All other resource folders are relative to this.
## APP_ROOT = Path(__file__).resolve().parent

import sys
from pathlib import Path

def get_app_root():
    """Gets the application root path for both normal script and PyInstaller bundle."""
    if getattr(sys, 'frozen', False):
        # We are running in a PyInstaller bundle. The root is the directory of the .exe file.
        return Path(sys.executable).parent.resolve()
    else:
        # We are running in a normal Python environment.
        return Path(__file__).resolve().parent

APP_ROOT = get_app_root()

# --- Third-Party Library Imports ---
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
import pandas as pd
from pydub import AudioSegment


# --- Flask App Initialization ---
# Configure Flask to explicitly use template and static folders located alongside main.py
app = Flask(
    __name__,
    template_folder=str(APP_ROOT / 'templates'),
    static_folder=str(APP_ROOT / 'static')
)
# The 'static' folder is automatically served by Flask at /static
socketio = SocketIO(app, async_mode='threading')


class WebLogger(logging.Handler):
    """A logging handler that emits log records to connected web clients via Socket.IO.

    Purpose:
    - Stream server logs to the browser in real-time so users can monitor background tasks.

    How it works:
    - Formats a logging record and emits it as a 'new_log' Socket.IO event to all clients.

    Methods:
    - emit(record): Format and emit a single log record.

    Example:
        >>> logger = logging.getLogger("AirportAnnouncementSystem")
        >>> web_handler = WebLogger()
        >>> logger.addHandler(web_handler)
        >>> logger.info("Hello web logs!")

    Notes:
    - This handler should not be the only handler; pair it with a file handler for persistence.
    """

    def emit(self, record):
        """
        Emit a formatted log record to all connected web clients using Socket.IO.

        Parameters:
        - record (logging.LogRecord): The log record emitted by Python's logging system.

        Returns:
        - None

        Example:
            >>> handler = WebLogger()
            >>> handler.emit(logging.makeLogRecord({'msg': 'Test'}))
        """
        log_entry = self.format(record)
        # Emit to all connected clients.
        socketio.emit('new_log', {'log': log_entry})


class AirportAnnouncementSystem:
    """
    Main application class that encapsulates:
    - Data management (loading/saving to Excel)
    - Audio material management and audio synthesis workflow
    - Progress reporting and stop signaling for long-running tasks

    Attributes:
    - data_dir (str): Absolute path to the data directory.
    - output_dir (str): Absolute path to the output directory for generated audio.
    - material_dir (str): Absolute path to the audio materials directory.
    - filename (str): Absolute path to the Excel file (data.xlsx).
    - logger (logging.Logger): Application-wide logger.
    - supported_language_codes (list[str]): Supported languages, e.g., ['CN', 'EN', 'JP', 'KR'].
    - language_type_presets (list[str]): Preset language sequences for UI convenience.
    - announcement_type_list (list[str]): Supported announcement types.
    - citynames (list[str]): Available city name audio keys.
    - airlines (list[str]): Available airline code audio keys.
    - delay_reasons (list[str]): Available delay reason audio keys.
    - data (list[list[str]]): In-memory representation of flight records.
    - stop_event (threading.Event): An event used to request cancellation of long-running tasks.

    Usage:
        >>> system = AirportAnnouncementSystem()
        >>> system.data  # Access loaded flight data
        >>> system.submit_flight({...})  # Add or edit data
        >>> system.search_and_synthesize("MU1234", "Check_in")  # Build an announcement

    Notes:
    - Uses threading.Event for thread-safe synchronization.
    - Ensure all necessary audio materials are present under material/ for synthesis to succeed.
    """

    # --- Constructor & Initialization ---------------- #

    def __init__(self):
        """
        Initialize the application state, create required folders, set up logging,
        load initial materials and flight data, and prepare synchronization primitives.

        Parameters:
        - None

        Returns:
        - None

        Side Effects:
        - Ensures the existence of data/, output/, and material/ directories.
        - Configures logging to file and web UI.
        - Loads data.xlsx into memory if present.

        Example:
            >>> system = AirportAnnouncementSystem()
            >>> len(system.data)
            0  # or number of rows loaded from data.xlsx
        """
        # Define core directories for data and output files, relative to the app's location
        # Convert Path objects to absolute path strings (do not change usage of os.* APIs)
        self.data_dir = str(APP_ROOT / 'data')
        self.output_dir = str(APP_ROOT / 'output')
        self.material_dir = str(APP_ROOT / 'material')
        self.filename = os.path.join(self.data_dir, 'data.xlsx')

        # Ensure necessary directories exist on startup
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.material_dir, exist_ok=True)

        self.logger = self._configure_logging()
        self.logger.info("=====================================================")
        self.logger.info("Application initializing...")

        # Supported languages and common presets
        self.supported_language_codes = ['CN', 'EN', 'JP', 'KR']
        self.language_type_presets = [
            'CN', 'EN', 'JP', 'KR', 'CN-EN', 'EN-CN', 'CN-JP', 'JP-CN', 'CN-KR', 'KR-CN',
            'EN-JP', 'JP-EN', 'EN-KR', 'KR-EN', 'JP-KR', 'KR-JP', 'CN-EN-JP', 'EN-JP-KR',
            'CN-EN-JP-KR'
        ]

        # Supported announcement types
        self.announcement_type_list = [
            "Check_in", "Arrival", "Baggage_Claim", "Departure_Delay_Determined",
            "Departure_Delay_Undetermined", "Arrival_Delay_Determined", "Arrival_Delay_Undetermined"
        ]

        # Load dynamic lists from material directory
        self.citynames, self.airlines, self.delay_reasons = self._load_material_lists()

        # Initialize state
        self.data = []  # In-memory flight table
        # Use standard threading Event for maximum compatibility
        self.stop_event = threading.Event()

        # Load initial flight data from Excel
        self.data = self.read_xlsx(self.filename)
        self.logger.info("Application initialized successfully.")

    # ---------------- Logging Configuration ---------------- #

    def _configure_logging(self):
        """
        Configure application logging to a rotating file and to the web UI.

        Parameters:
        - None

        Returns:
        - logging.Logger: Configured logger named "AirportAnnouncementSystem".

        Behavior:
        - Writes logs to project_root/application.log (max 2MB per file, 5 backups).
        - Also streams logs to browser via Socket.IO using WebLogger.

        Example:
            >>> logger = self._configure_logging()
            >>> logger.info("Logger ready")
        """
        # Write logs to the app's root directory to avoid coupling to the run directory
        log_dir = str(APP_ROOT)  # Log file at app root directory
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, 'application.log')

        logger = logging.getLogger("AirportAnnouncementSystem")
        logger.setLevel(logging.DEBUG)

        # Prevent adding handlers multiple times in case of re-initialization
        if not logger.handlers:
            # File Handler for persistent logs
            # Rotates logs when they reach 2MB, keeping 5 backup files.
            file_handler = RotatingFileHandler(log_path, maxBytes=2_000_000, backupCount=5, encoding='utf-8')
            formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] (%(funcName)s:%(lineno)d) - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # Web Handler to stream logs to the frontend
            web_handler = WebLogger()
            web_handler.setFormatter(formatter)
            logger.addHandler(web_handler)

        return logger

    # ---------------- Material Loading ---------------- #

    def _load_material_lists(self):
        """
        Load city names, airline codes, and delay reasons from the 'material' directory.

        Parameters:
        - None

        Returns:
        - tuple[list[str], list[str], list[str]]:
            (citynames, airlines, delay_reasons) derived from .wav filenames.

        Directory Conventions:
        - material/cityname_cn/*.wav -> city names (Chinese set for validation purposes)
        - material/airlines_cn/*.wav -> airline codes (Chinese set, e.g., 'MU', 'CZ')
        - material/delay_reason_cn/*.wav -> delay reason keys for CN

        Behavior:
        - Creates missing directories to avoid later errors.
        - Ignores non-.wav files.
        - Returns empty lists on failure and logs the exception.

        Example:
            >>> cities, airlines, reasons = self._load_material_lists()
            >>> len(cities), len(airlines), len(reasons)
            (10, 12, 5)
        """
        try:
            # Load city names from 'material/cityname_cn'
            city_path = os.path.join(self.material_dir, 'cityname_cn')
            os.makedirs(city_path, exist_ok=True)  # Ensure directory exists
            citynames = sorted([name.rsplit('.', 1)[0] for name in os.listdir(city_path) if name.endswith('.wav')])

            # Load airline codes from 'material/airlines_cn'
            airline_path = os.path.join(self.material_dir, 'airlines_cn')
            os.makedirs(airline_path, exist_ok=True)
            airlines = sorted([name.rsplit('.', 1)[0] for name in os.listdir(airline_path) if name.endswith('.wav')])

            # Load delay reasons from 'material/delay_reason_cn'
            reason_path = os.path.join(self.material_dir, 'delay_reason_cn')
            os.makedirs(reason_path, exist_ok=True)
            delay_reasons = sorted([name.rsplit('.', 1)[0] for name in os.listdir(reason_path) if name.endswith('.wav')])

            self.logger.info(f"Material lists loaded: {len(citynames)} cities, {len(airlines)} airlines, {len(delay_reasons)} reasons.")
            return citynames, airlines, delay_reasons
        except Exception:
            self.logger.exception("Failed to load material directories. This may cause validation errors.")
            return [], [], []

    # ---------------- Progress & Validation Utilities ---------------- #

    def update_progress(self, step, total, text):
        """
        Emit a progress update to the frontend via Socket.IO.

        Parameters:
        - step (int): Current step index (1-based recommended).
        - total (int): Total number of steps (use non-zero to get percentage).
        - text (str): Short description of the current step.

        Returns:
        - None

        Behavior:
        - Emits a 'progress_update' event with {'percent', 'text'}.

        Example:
            >>> self.update_progress(3, 10, "Combining audio segments")
        """
        try:
            percent = (step / total) * 100 if total > 0 else 0
            # Emit a 'progress_update' event that the frontend can listen to
            socketio.emit('progress_update', {'percent': percent, 'text': f"Processing: ({step}/{total}) {text}"})
            # A small sleep is good practice to prevent flooding the client
            time.sleep(0.01)
        except Exception:
            self.logger.exception("Failed to send progress update via SocketIO.")

    def is_valid_time(self, time_str):
        """
        Validate if a string is in the 'HH:MM' 24-hour time format.

        Parameters:
        - time_str (str): Time string, e.g., '08:30'. Empty string is considered valid.

        Returns:
        - bool: True if valid (or empty), False otherwise.

        Example:
            >>> self.is_valid_time('09:15')
            True
            >>> self.is_valid_time('9:15')
            False
        """
        if not time_str:
            return True  # Empty is considered valid
        try:
            time.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False

    def parse_language_sequence(self, language_string):
        """
        Parse and validate a language sequence string (e.g., 'CN-EN-JP').

        Behavior:
        - Canonicalizes aliases: 'JA' -> 'JP', 'KO' -> 'KR'.
        - Removes duplicates.
        - Filters to supported languages only.

        Parameters:
        - language_string (str): Input sequence, case-insensitive; accepts '-', '_' separators.

        Returns:
        - list[str]: Canonical sequence such as ['CN', 'EN', 'JP'].
                     Returns [] if input is empty or all entries invalid.

        Example:
            >>> self.parse_language_sequence("cn_en_jp")
            ['CN', 'EN', 'JP']
            >>> self.parse_language_sequence("KO-EN-KR")
            ['KR', 'EN']  # 'KO' becomes 'KR', duplicate removed
        """
        if not language_string:
            return []
        raw = language_string.upper().replace('_', '-').strip()
        parts = [p.strip() for p in raw.split('-') if p.strip()]
        canonical = []
        for p in parts:
            if p == 'JA':
                p = 'JP'  # Alias for Japanese
            if p == 'KO':
                p = 'KR'  # Alias for Korean
            if p in self.supported_language_codes and p not in canonical:
                canonical.append(p)
            else:
                self.logger.warning(f"Ignoring unsupported or duplicate language code: '{p}' in '{language_string}'")
        return canonical

    # ---------------- Excel Data I/O ---------------- #

    def read_xlsx(self, filename):
        """
        Read flight data from an Excel file into a list of rows.

        Parameters:
        - filename (str): Absolute path to the Excel file.

        Returns:
        - list[list[str]]: Rows of data as strings. Empty list if file not found or error occurs.

        Behavior:
        - Uses pandas with engine='openpyxl'.
        - Replaces NaN/NaT with empty strings for consistency.
        - Logs success or failure.

        Example:
            >>> rows = self.read_xlsx(self.filename)
            >>> len(rows)
            10
        """
        try:
            if not os.path.exists(filename):
                self.logger.warning(f"Data file '{filename}' not found. Starting with an empty flight list.")
                return []
            df = pd.read_excel(filename, engine='openpyxl')
            # Replace any NaN/NaT values with empty strings for consistency
            df = df.fillna(value='')
            # Convert all data to string type to avoid formatting issues, then to a list of lists
            rows = df.astype(str).values.tolist()
            self.logger.info(f"Successfully loaded {len(rows)} flight rows from '{filename}'.")
            return rows
        except Exception as e:
            self.logger.exception(f"Failed to read Excel file '{filename}'. Error: {e}")
            return []

    def write_xlsx(self, data, filename):
        """
        Write in-memory flight data to an Excel file.

        Parameters:
        - data (list[list[str]]): The flight data rows.
        - filename (str): Absolute path to the Excel file to write to.

        Returns:
        - None

        Behavior:
        - Overwrites the file with a fixed header set.
        - Uses pandas with engine='openpyxl'.

        Example:
            >>> self.write_xlsx(self.data, self.filename)
        """
        try:
            # Define the exact header for the Excel file
            header = [
                "Flight Number", "Departure", "Stopover", "Destination", "Divert",
                "Check-in Counter", "Boarding Gate", "Baggage Claim",
                "Scheduled Arrival Time", "Estimated Arrival Time", "Delay Reason", "Language Type"
            ]
            df = pd.DataFrame(data, columns=header)
            df.to_excel(filename, index=False, engine='openpyxl')
            self.logger.info(f"Successfully saved {len(data)} flight rows to '{filename}'.")
        except Exception as e:
            self.logger.exception(f"Failed to write to Excel file '{filename}'. Error: {e}")

    # ---------------- API Handler Methods ---------------- #

    def save_info_function(self):
        """
        Persist current in-memory flight data to disk.

        Parameters:
        - None

        Returns:
        - dict: JSON-serializable result with:
            - success (bool)
            - message (str)

        Example:
            >>> self.save_info_function()
            {'success': True, 'message': 'Flight information saved successfully!'}
        """
        self.logger.info("User triggered 'Save Info'. Writing current data to disk.")
        try:
            self.write_xlsx(self.data, self.filename)
            return {"success": True, "message": "Flight information saved successfully!"}
        except Exception as e:
            self.logger.exception("Save Info failed.")
            return {"success": False, "message": f"An error occurred while saving: {e}"}

    def clear_function(self):
        """
        Clear all flight data in memory and on disk.

        Parameters:
        - None

        Returns:
        - dict:
            - success (bool)
            - message (str)

        Example:
            >>> self.clear_function()
            {'success': True, 'message': 'All flight data has been cleared.'}
        """
        self.logger.warning("User triggered 'Clear All'. All flight data will be erased.")
        try:
            self.data = []
            self.write_xlsx(self.data, self.filename)
            self.logger.info("All flight data has been cleared from memory and disk.")
            return {"success": True, "message": "All flight data has been cleared."}
        except Exception as e:
            self.logger.exception("Clearing data failed.")
            return {"success": False, "message": f"An error occurred while clearing data: {e}"}

    def refresh_table(self):
        """
        Reload the flight data from disk into memory.

        Parameters:
        - None

        Returns:
        - dict:
            - success (bool)
            - message (str)
            - data (list[list[str]]): The refreshed flight data.

        Example:
            >>> self.refresh_table()
            {'success': True, 'message': 'Flight information refreshed successfully!', 'data': [...]}
        """
        self.logger.info("User triggered 'Refresh'. Reloading data from disk.")
        try:
            self.data = self.read_xlsx(self.filename)
            return {"success": True, "message": "Flight information refreshed successfully!", "data": self.data}
        except Exception as e:
            self.logger.exception("Refreshing table failed.")
            return {"success": False, "message": f"An error occurred while refreshing: {e}", "data": []}

    def submit_flight(self, form_data, is_edit=False, original_flight_number=None):
        """
        Add a new flight row or edit an existing one with full validation.

        Parameters:
        - form_data (dict): Keys expected:
            'flight_number', 'departure', 'stopover', 'destination', 'divert',
            'checkin_counter', 'boarding_gate', 'baggage_claim',
            'scheduled_arrival_time', 'estimated_arrival_time',
            'delay_reason', 'language_type'
        - is_edit (bool): If True, edit the row that matches 'original_flight_number'.
        - original_flight_number (str|None): Required when is_edit=True to locate the existing row.

        Returns:
        - dict:
            - success (bool)
            - message (str)
            - data (list[list[str]]) optional: the updated dataset on success

        Validation Rules:
        - Flight number, departure, destination, check-in counter must be non-empty.
        - Flight number only contains [A-Z0-9 ].
        - Airline codes (first two letters of each flight number block) must exist in materials.
        - Time fields must be 'HH:MM' or empty.
        - Language type must be valid and canonicalized.

        Examples:
            Add:
            >>> payload = {
            ...   'flight_number': 'MU1234',
            ...   'departure': 'Shanghai',
            ...   'stopover': '',
            ...   'destination': 'Beijing',
            ...   'divert': '',
            ...   'checkin_counter': 'A-12',
            ...   'boarding_gate': 'B12',
            ...   'baggage_claim': '6',
            ...   'scheduled_arrival_time': '09:15',
            ...   'estimated_arrival_time': '09:30',
            ...   'delay_reason': 'weather',
            ...   'language_type': 'CN-EN'
            ... }
            >>> self.submit_flight(payload, is_edit=False)

            Edit:
            >>> self.submit_flight(payload, is_edit=True, original_flight_number='MU1234')
        """
        self.logger.info(f"Processing flight submission. Mode: {'Edit' if is_edit else 'Add'}.")
        try:
            # Extract and clean data from the form
            row = [
                form_data.get('flight_number', '').strip().upper(),
                form_data.get('departure', '').strip(),
                form_data.get('stopover', '').strip(),
                form_data.get('destination', '').strip(),
                form_data.get('divert', '').strip(),
                form_data.get('checkin_counter', '').strip().upper(),
                form_data.get('boarding_gate', '').strip().upper(),
                form_data.get('baggage_claim', '').strip().upper(),
                form_data.get('scheduled_arrival_time', '').strip(),
                form_data.get('estimated_arrival_time', '').strip(),
                form_data.get('delay_reason', '').strip(),
                form_data.get('language_type', '').strip(),
            ]

            flight_number, departure, _, destination, _, checkin, _, _, sched_time, est_time, _, lang_str = row

            # --- Comprehensive Validation ---
            if not flight_number:
                return {"success": False, "message": "Flight number cannot be empty."}
            if not destination:
                return {"success": False, "message": "Destination cannot be empty."}
            if not departure:
                return {"success": False, "message": "Departure cannot be empty."}
            if not checkin:
                return {"success": False, "message": "Check-in counter cannot be empty."}

            flights_multi = flight_number.split()
            airlines_multi = [f[:2] for f in flights_multi]

            if not is_edit:
                existing_numbers = {item for r in self.data for item in r[0].split()}
                for fn in flights_multi:
                    if fn in existing_numbers:
                        return {"success": False, "message": f"Flight number '{fn}' already exists."}

            for char in flight_number:
                if char not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ':
                    return {"success": False, "message": "Flight number must contain only A-Z, 0-9, and spaces."}

            for ac in airlines_multi:
                if ac not in self.airlines:
                    return {"success": False, "message": f"Airline code '{ac}' is not supported. No audio found."}

            if not self.is_valid_time(sched_time):
                return {"success": False, "message": "Scheduled Time must be in HH:MM format."}
            if not self.is_valid_time(est_time):
                return {"success": False, "message": "Estimated Time must be in HH:MM format."}

            language_sequence = self.parse_language_sequence(lang_str)
            if not language_sequence:
                return {"success": False, "message": "Language Type is invalid or empty."}
            row[11] = '-'.join(language_sequence)  # Save the canonical version

            # --- Data Update Logic ---
            if is_edit:
                # Correct logic for editing
                found_index = -1
                for i, r in enumerate(self.data):
                    if r[0] == original_flight_number:
                        found_index = i
                        break
                if found_index != -1:
                    # Update the flight data at the found index
                    self.data[found_index] = row
                    self.logger.info(f"Successfully edited flight: '{original_flight_number}'.")
                else:
                    return {"success": False, "message": f"Flight '{original_flight_number}' not found for editing."}
            else:
                self.data.append(row)
                self.logger.info(f"Successfully added new flight: '{flight_number}'.")

            # Persist changes to disk
            self.write_xlsx(self.data, self.filename)
            return {"success": True, "data": self.data, "message": f"Flight '{flight_number}' saved successfully."}

        except Exception as e:
            self.logger.exception("submit_flight failed with an unexpected error.")
            return {"success": False, "message": f"An unexpected error occurred: {e}"}

    def delete_flight(self, flight_number):
        """
        Delete a flight row by its exact flight number (full string, no split).

        Parameters:
        - flight_number (str): Flight number to remove (must match exactly the stored key).

        Returns:
        - dict:
            - success (bool)
            - message (str)
            - data (list[list[str]]) optional: remaining dataset on success

        Example:
            >>> self.delete_flight('MU1234')
            {'success': True, 'data': [...], 'message': "Flight 'MU1234' deleted."}
        """
        self.logger.info(f"Attempting to delete flight: '{flight_number}'")
        try:
            if not flight_number:
                return {"success": False, "message": "Flight number cannot be empty."}

            original_len = len(self.data)
            # Filter out the flight to be deleted
            self.data = [r for r in self.data if r[0] != flight_number]

            if len(self.data) == original_len:
                self.logger.warning(f"Flight '{flight_number}' not found for deletion.")
                return {"success": False, "message": f"Flight '{flight_number}' not found."}

            self.write_xlsx(self.data, self.filename)
            self.logger.info(f"Successfully deleted flight: '{flight_number}'.")
            return {"success": True, "data": self.data, "message": f"Flight '{flight_number}' deleted."}
        except Exception as e:
            self.logger.exception("delete_flight failed.")
            return {"success": False, "message": f"An error occurred while deleting flight: {e}"}

    # ---------------- Audio Processing and Synthesis ---------------- #

    def clear_output_cache(self):
        """
        Delete all files in the output directory (generated audio cache).

        Parameters:
        - None

        Returns:
        - dict:
            - success (bool)
            - message (str)

        Behavior:
        - Deletes regular files and symlinks. Directories are ignored.

        Example:
            >>> self.clear_output_cache()
            {'success': True, 'message': 'Audio cache cleared. 3 files were deleted.'}
        """
        self.logger.info("User triggered 'Clear Cache'. Deleting all generated audio files.")
        deleted_count = 0
        error_count = 0
        try:
            for filename in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                        self.logger.debug(f"Deleted cache file: {filename}")
                        deleted_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to delete {file_path}. Reason: {e}")
                    error_count += 1

            if error_count > 0:
                message = f"Cache partially cleared. {deleted_count} files deleted, but {error_count} errors occurred."
                return {"success": False, "message": message}

            self.logger.info(f"Successfully cleared cache. {deleted_count} files deleted.")
            return {"success": True, "message": f"Audio cache cleared. {deleted_count} files were deleted."}

        except Exception as e:
            self.logger.exception("An unexpected error occurred while clearing the output cache.")
            return {"success": False, "message": f"An error occurred: {e}"}

    def convert_to_stereo(self, input_folder):
        """
        Recursively convert all .wav files in a folder to stereo (2 channels), in-place.

        Parameters:
        - input_folder (str): Absolute path to the folder whose .wav files should be converted.

        Returns:
        - None (emits progress via Socket.IO; ends with 'progress_end' event)

        Behavior:
        - Resets stop_event at start (new event per operation).
        - Emits 'progress_start' and periodic 'progress_update'.
        - Aborts if stop_event is triggered.
        - Only changes files that are not already stereo.

        Example:
            >>> self.convert_to_stereo(self.material_dir)

        Notes:
        - Designed to be run in a background task via socketio.start_background_task.
        """
        self.logger.info(f"Starting stereo conversion for all .wav files in '{input_folder}'.")
        # Ensure we have a fresh stop event before starting
        self.stop_event = threading.Event()
        socketio.emit('progress_start', {'title': 'Converting Audio Files to Stereo...'})

        all_files = []
        for root_dir, _, files in os.walk(input_folder):
            for filename in files:
                if filename.lower().endswith(".wav"):
                    all_files.append(os.path.join(root_dir, filename))

        total_files = len(all_files)
        self.logger.info(f"Found {total_files} .wav files to process.")

        for i, path in enumerate(all_files, start=1):
            if self.stop_event.is_set():
                self.logger.warning("Stereo conversion aborted by user.")
                self.update_progress(i, total_files, "Conversion Aborted!")
                socketio.emit('progress_end')
                return

            try:
                audio = AudioSegment.from_wav(path)
                if audio.channels != 2:
                    stereo_audio = audio.set_channels(2)
                    stereo_audio.export(path, format="wav")
                    self.logger.debug(f"Converted to stereo: {os.path.basename(path)}")
                self.update_progress(i, total_files, os.path.basename(path))
            except Exception as e:
                self.logger.error(f"Failed to convert '{path}': {e}")
                continue

        self.logger.info("Stereo conversion process completed.")
        self.update_progress(total_files, total_files, "Conversion Complete!")
        socketio.emit('progress_end')

    def stop_all_audio(self):
        """
        Request cancellation of any active long-running process (e.g., synthesis, conversion).

        Parameters:
        - None

        Returns:
        - dict:
            - success (bool)
            - message (str)

        Behavior:
        - Sends stop signal by .set() on the threading Event if not already set.
        - If already active, returns idempotent success.

        Example:
            >>> self.stop_all_audio()
            {'success': True, 'message': 'Stop signal sent to all active processes.'}
        """
        self.logger.info("STOP ALL requested by user.")
        if not self.stop_event.is_set():
            self.stop_event.set()
            self.logger.info("Stop event is now active. Active processes will terminate shortly.")
            return {"success": True, "message": "Stop signal sent to all active processes."}
        else:
            self.logger.debug("Stop event was already active; ignoring duplicate request.")
            return {"success": True, "message": "Stop signal was already active."}

    def search_and_synthesize(self, flight_key, announce_type):
        """
        Synthesize an announcement by concatenating appropriate audio segments.

        Parameters:
        - flight_key (str): Exact flight number key as stored in the dataset.
        - announce_type (str): One of self.announcement_type_list (e.g., 'Check_in').

        Returns:
        - dict:
            - success (bool)
            - message (str)
            - audio_url (str) optional: URL path (relative) to the generated audio when successful.

        Workflow:
        - Validate inputs and find the matching row.
        - Parse language sequence and build segment paths according to announcement type.
        - Prepend an attention chime if present (material/mix/756.wav).
        - Verify all files exist.
        - Concatenate audio segments with pydub and export a .wav file to output/.
        - Emit progress events and return the relative URL for the browser to play.

        Example:
            >>> self.search_and_synthesize('MU1234', 'Check_in')
            {'success': True, 'audio_url': '/output/MU1234_Check_in_20250101120000.wav', 'message': 'Synthesis complete. Playing announcement...'}

        Notes:
        - Ensure ffmpeg is installed and on PATH for pydub to export.
        """
        self.logger.info(f"Synthesis started. Flight: '{flight_key}', Type: '{announce_type}'.")
        # Create a new, fresh event for this specific task.
        self.stop_event = threading.Event()

        # --- Validation ---
        if not flight_key:
            return {"success": False, "message": "No flight selected."}
        if not announce_type:
            return {"success": False, "message": "No announcement type selected."}

        row_data = next((r for r in self.data if r[0] == flight_key), None)
        if not row_data:
            self.logger.error(f"Flight data for '{flight_key}' not found.")
            return {"success": False, "message": "Flight data not found."}

        lang_str = row_data[11]
        language_order = self.parse_language_sequence(lang_str)
        if not language_order:
            return {"success": False, "message": f"Invalid language config for flight '{flight_key}'. Please edit and save."}

        # --- Segment Building ---
        socketio.emit('progress_start', {'title': 'Synthesizing Audio...'})
        self.update_progress(0, 100, "Building audio segment list...")

        # Unpack the row data to pass as arguments
        segment_paths = self._build_announcement_segments(announce_type, language_order, *row_data)

        if not segment_paths:
            self.logger.error("No audio segments were generated. Check for missing data or unsupported type.")
            socketio.emit('progress_end')
            return {"success": False, "message": "Could not generate audio. Check if all required flight info is present for this announcement type."}

        # --- Prepend Chime ---
        # Ensure the attention chime is always the first sound.
        tone_path = os.path.join(self.material_dir, 'mix', '756.wav')
        if not os.path.exists(tone_path):
            self.logger.warning("Attention chime '756.wav' not found in material/mix folder.")
        else:
            if tone_path in segment_paths:  # Remove if already present to avoid duplicates
                segment_paths.remove(tone_path)
            segment_paths.insert(0, tone_path)

        # --- File Existence Check ---
        missing_files = [p for p in segment_paths if not os.path.exists(p)]
        if missing_files:
            missing_str = ", ".join([os.path.basename(p) for p in missing_files[:5]])
            self.logger.error(f"Synthesis failed. Missing required audio files: {missing_files}")
            socketio.emit('progress_end')
            return {"success": False, "message": f"Missing audio files: {missing_str}..."}

        # --- Audio Combination ---
        combined_audio = AudioSegment.empty()
        total_segments = len(segment_paths)

        for idx, wav_file in enumerate(segment_paths, start=1):
            if self.stop_event.is_set():
                self.logger.warning("Synthesis aborted by user during segment combination.")
                socketio.emit('progress_end')
                return {"success": False, "message": "Synthesis aborted."}
            try:
                seg = AudioSegment.from_wav(wav_file)
                combined_audio += seg
                self.update_progress(idx, total_segments, os.path.basename(wav_file))
            except Exception as e:
                self.logger.exception(f"Failed to load or append audio segment: {wav_file}")
                socketio.emit('progress_end')
                return {"success": False, "message": f"Error processing audio file: {os.path.basename(wav_file)}"}

        # --- Export Final Audio ---
        try:
            output_filename = f"{flight_key.replace(' ', '_')}_{announce_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
            output_path = os.path.join(self.output_dir, output_filename)
            combined_audio.export(output_path, format="wav")

            self.logger.info(f"Announcement successfully exported to: {output_path}")
            socketio.emit('progress_end')
            # Return a relative URL so the browser can fetch via the /output route
            return {"success": True, "audio_url": f"/output/{output_filename}", "message": "Synthesis complete. Playing announcement..."}
        except Exception as e:
            self.logger.exception("Failed to export final combined audio.")
            socketio.emit('progress_end')
            return {"success": False, "message": f"Failed to save final audio file: {e}"}

    # ---------------- Segment Assembly Logic ---------------- #

    def _build_announcement_segments(self, announce_type, language_order, *row_data):
        """
        Build a list of material file paths (segments) for a given announcement type and languages.

        Parameters:
        - announce_type (str): One of supported types (e.g., 'Check_in', 'Arrival', ...).
        - language_order (list[str]): Sequence of languages to output, e.g., ['CN', 'EN'].
        - *row_data: The unpacked row data with at least the first 12 columns:
            (flight_number, departure, stopover, destination, divert,
             checkin_counter, boarding_gate, baggage_claim,
             scheduled_time, estimated_time, delay_reason, lang_str)

        Returns:
        - list[str]: Full filesystem paths of .wav files to be concatenated.

        Example:
            >>> segs = self._build_announcement_segments('Check_in', ['CN','EN'], *row)
            >>> segs[:3]
            ['.../template_cn/1.wav', '.../airlines_cn/MU.wav', '.../alnum_cn/M.wav']
        """
        # Unpack the flight data for clarity
        (flight_number, departure, stopover, destination, divert, checkin_counter,
         boarding_gate, baggage_claim, scheduled_time, estimated_time, delay_reason, _) = row_data[:12]

        segments = []
        flights = flight_number.split()

        for lang in language_order:
            try:
                # Based on the announcement type, call the corresponding builder function
                if announce_type == "Check_in":
                    segments.extend(self._segments_checkin(lang, flights, departure, stopover, destination, checkin_counter))
                elif announce_type == "Arrival":
                    segments.extend(self._segments_arrival(lang, flights, departure, stopover))
                elif announce_type == "Baggage_Claim":
                    segments.extend(self._segments_baggage(lang, flights, departure, stopover, baggage_claim))
                elif announce_type == "Departure_Delay_Determined":
                    segments.extend(self._segments_delay(lang, flights, departure, destination, estimated_time, delay_reason, determined=True, arrival=False))
                elif announce_type == "Departure_Delay_Undetermined":
                    segments.extend(self._segments_delay(lang, flights, departure, destination, estimated_time, delay_reason, determined=False, arrival=False))
                elif announce_type == "Arrival_Delay_Determined":
                    segments.extend(self._segments_delay(lang, flights, departure, destination, estimated_time, delay_reason, determined=True, arrival=True))
                elif announce_type == "Arrival_Delay_Undetermined":
                    segments.extend(self._segments_delay(lang, flights, departure, destination, estimated_time, delay_reason, determined=False, arrival=True))
                else:
                    self.logger.warning(f"Unsupported announcement type '{announce_type}' requested.")
            except Exception:
                self.logger.exception(f"Failed building segments for lang='{lang}', type='{announce_type}'.")
        return segments

    def _get_path(self, lang, category, name):
        """
        Construct a full path to a material .wav file based on language, category, and name.

        Parameters:
        - lang (str): Language code, e.g., 'CN', 'EN', 'JP', 'KR'.
        - category (str): Material category, e.g., 'alnum', 'airlines', 'cityname', 'template', 'delay_reason'.
        - name (str): Base filename without extension.

        Returns:
        - str: Absolute path to the .wav file.

        Notes:
        - Alphanumeric sets are language-specific and stored under 'alnum_{lang_lower}' directories.

        Example:
            >>> self._get_path('CN', 'alnum', '1')
            '/.../material/alnum_cn/1.wav'
        """
        # Special handling for alphanumeric, which has language-specific folders
        if category == 'alnum':
            return os.path.join(self.material_dir, f'alnum_{lang.lower()}', f'{name}.wav')
        return os.path.join(self.material_dir, f'{category}_{lang.lower()}', f'{name}.wav')

    def _speak_time(self, lang, time_str):
        """
        Create a list of material paths representing the spoken time for a language.

        Parameters:
        - lang (str): Language code, e.g., 'CN' or 'EN'. JP/KR may be extended later.
        - time_str (str): Time in 'HH:MM' format.

        Returns:
        - list[str]: Paths composing the spoken time. Empty list if invalid time or language unsupported.

        Examples:
            >>> self._speak_time('CN', '08:05')
            ['.../alnum_cn/0.wav', '.../alnum_cn/8.wav', '.../template_cn/15.wav',
             '.../alnum_cn/0.wav', '.../alnum_cn/5.wav', '.../template_cn/16.wav']

            >>> self._speak_time('EN', '13:45')
            ['.../alnum_en/1.wav', '.../alnum_en/3.wav', '.../alnum_en/4.wav', '.../alnum_en/5.wav']
        """
        segs = []
        if not self.is_valid_time(time_str):
            return segs
        hour, minute = time_str.split(':')

        if lang == 'CN':
            for digit in hour:
                segs.append(self._get_path(lang, 'alnum', digit))
            segs.append(self._get_path(lang, 'template', '15'))  # 点
            for digit in minute:
                segs.append(self._get_path(lang, 'alnum', digit))
            segs.append(self._get_path(lang, 'template', '16'))  # 分
        elif lang == 'EN':
            for digit in hour:
                segs.append(self._get_path(lang, 'alnum', digit))
            for digit in minute:
                segs.append(self._get_path(lang, 'alnum', digit))
        # Add JP, KR logic if needed
        return segs

    # --- Language-Specific Segment Builders ---

    def _segments_checkin(self, lang, flights, departure, stopover, destination, checkin_counter):
        """
        Build the segment list for 'Check_in' announcements for a given language.

        Parameters:
        - lang (str): Language code ('CN', 'EN', 'JP', 'KR').
        - flights (list[str]): Flight numbers split by spaces (e.g., ['MU1234', 'CZ5678']).
        - departure (str): Departure city key.
        - stopover (str): Stopover city key (optional).
        - destination (str): Destination city key.
        - checkin_counter (str): Check-in counter string, may contain '-'.

        Returns:
        - list[str]: Sequence of material paths forming the announcement.

        Example:
            >>> self._segments_checkin('CN', ['MU1234'], 'Shanghai', '', 'Beijing', 'A-12')
            ['.../template_cn/1.wav', '.../airlines_cn/MU.wav', '.../alnum_cn/M.wav', ...]

        Notes:
        - Behavior varies per language; JP/KR are partial placeholders.
        """
        seg = []
        lang_l = lang.lower()
        # Path helper
        p = lambda cat, name: os.path.join(self.material_dir, f'{cat}_{lang_l}', f'{name}.wav')

        if lang == 'CN':
            seg.append(p('template', '1'))  # 乘坐
            for f in flights:
                seg.append(p('airlines', f[:2]))
                for c in f:
                    seg.append(p('alnum', c))
            seg.append(p('template', '2'))  # 次航班，从
            seg.append(p('cityname', departure))
            if stopover:
                seg.append(p('template', '3'))  # 经由
                seg.append(p('cityname', stopover))
            seg.append(p('template', '4'))  # 前往
            seg.append(p('cityname', destination))
            seg.append(p('template', '5'))  # 的旅客请注意...
            for c in checkin_counter:
                if c == '-':
                    seg.append(p('template', '6'))  # 至
                else:
                    seg.append(p('alnum', c))
            seg.append(p('template', '7'))  # 号柜台办理...
        elif lang == 'EN':
            seg.append(p('template', '1'))  # May I have...
            seg.append(p('template', '2'))  # We are now ready...
            for f in flights:
                seg.append(p('airlines', f[:2]))
                seg.append(p('template', '3'))  # Flight
                for c in f:
                    seg.append(p('alnum', c))
            seg.append(p('template', '4'))  # From
            seg.append(p('cityname', departure))
            if stopover:
                seg.append(p('template', '5'))  # To
                seg.append(p('cityname', stopover))
                seg.append(p('template', '6'))  # With continuing service to
                seg.append(p('cityname', destination))
            else:
                seg.append(p('template', '5'))  # To
                seg.append(p('cityname', destination))
            seg.append(p('template', '7'))  # At check-in counter...
            for c in checkin_counter:
                if c == '-':
                    seg.append(p('template', '5'))  # to
                else:
                    seg.append(p('alnum', c))
            seg.append(p('template', '8'))  # Thank you
        elif lang == 'JP':
            seg.append(p('template', '1'))
            seg.append(p('template', '2'))
            for f in flights:
                seg.append(p('airlines', f[:2]))
                for c in f:
                    if c.isnumeric():
                        seg.append(p('alnum', c))
                seg.append(p('template', '3'))
            seg.append(p('cityname', departure))
            seg.append(p('template', '4'))
            if stopover:
                seg.append(p('cityname', stopover))
                seg.append(p('template', '5'))
            seg.append(p('cityname', destination))
            seg.append(p('template', '6'))
            seg.append(p('template', '7'))
            for c in checkin_counter:
                if c == '-':
                    seg.append(p('template', '9'))  # から
                else:
                    seg.append(p('alnum', c))
            seg.append(p('template', '8'))
        elif lang == 'KR':
            # Placeholder for Korean - to be implemented
            seg.append(p('template', '1'))

        return seg

    def _segments_arrival(self, lang, flights, departure, stopover):
        """
        Build the segment list for 'Arrival' announcements.

        Parameters:
        - lang (str): Language code.
        - flights (list[str]): Flight numbers split by spaces.
        - departure (str): Departure city key.
        - stopover (str): Stopover city key (optional).

        Returns:
        - list[str]: Sequence of material paths for the arrival message.

        Example:
            >>> self._segments_arrival('EN', ['MU1234'], 'Shanghai', '')
            ['.../template_en/1.wav', '.../airlines_en/MU.wav', ...]
        """
        seg = []
        lang_l = lang.lower()
        p = lambda cat, name: os.path.join(self.material_dir, f'{cat}_{lang_l}', f'{name}.wav')

        if lang == 'CN':
            seg.extend([p('template', '8'), p('template', '9')])  # 迎接...从
            seg.append(p('cityname', departure))
            if stopover:
                seg.extend([p('template', '3'), p('cityname', stopover)])  # 经由
            seg.append(p('template', '10'))  # 飞来的
            for f in flights:
                seg.append(p('airlines', f[:2]))
                for c in f:
                    seg.append(p('alnum', c))
            seg.append(p('template', '11'))  # ...已经到达
        elif lang == 'EN':
            seg.append(p('template', '1'))  # May I have...
            for f in flights:
                seg.append(p('airlines', f[:2]))
                seg.append(p('template', '3'))  # Flight
                for c in f:
                    seg.append(p('alnum', c))
            seg.append(p('template', '9'))  # with service from
            seg.append(p('cityname', departure))
            if stopover:
                seg.extend([p('template', '11'), p('cityname', stopover)])  # and
            seg.extend([p('template', '10'), p('template', '8')])  # has arrived, thank you
        # JP, KR to be implemented
        return seg

    def _segments_baggage(self, lang, flights, departure, stopover, baggage_claim):
        """
        Build the segment list for 'Baggage_Claim' announcements.

        Parameters:
        - lang (str): Language code.
        - flights (list[str]): Flight numbers.
        - departure (str): Departure city key.
        - stopover (str): Stopover city key (optional).
        - baggage_claim (str): Baggage claim carousel ID (may contain digits).

        Returns:
        - list[str]: Sequence of material paths for baggage claim message.

        Example:
            >>> self._segments_baggage('CN', ['MU1234'], 'Shanghai', '', '6')
            ['.../template_cn/1.wav', '.../airlines_cn/MU.wav', ...]
        """
        seg = []
        lang_l = lang.lower()
        p = lambda cat, name: os.path.join(self.material_dir, f'{cat}_{lang_l}', f'{name}.wav')

        if lang == 'CN':
            seg.append(p('template', '1'))  # 乘坐
            for f in flights:
                seg.append(p('airlines', f[:2]))
                for c in f:
                    seg.append(p('alnum', c))
            seg.append(p('template', '2'))  # 次航班
            seg.append(p('cityname', departure))
            if stopover:
                seg.extend([p('template', '3'), p('cityname', stopover)])  # 经由
            seg.append(p('template', '12'))  # 到达本站的旅客...
            for c in baggage_claim:
                seg.append(p('alnum', c))
            seg.append(p('template', '13'))  # 号行李转盘...
        elif lang == 'EN':
            seg.append(p('template', '1'))  # May I have...
            seg.append(p('template', '12'))  # Arriving passengers on
            for f in flights:
                seg.append(p('airlines', f[:2]))
                seg.append(p('template', '3'))  # Flight
                for c in f:
                    seg.append(p('alnum', c))
            seg.append(p('template', '9'))  # with service from
            seg.append(p('cityname', departure))
            if stopover:
                seg.extend([p('template', '11'), p('cityname', stopover)])  # and
            seg.append(p('template', '13'))  # Your baggage will be...
            for c in baggage_claim:
                seg.append(p('alnum', c))
            seg.append(p('template', '8'))  # Thank you
        # JP, KR to be implemented
        return seg

    def _segments_delay(self, lang, flights, from_city, to_city, est_time, reason, determined, arrival):
        """
        Build the segment list for delay announcements (arrival or departure, determined/undetermined).

        Parameters:
        - lang (str): Language code.
        - flights (list[str]): Flight numbers.
        - from_city (str): Origin city key (for arrival messages).
        - to_city (str): Destination city key (for departure messages).
        - est_time (str): New estimated time in 'HH:MM' (required for determined delays).
        - reason (str): Delay reason key (optional).
        - determined (bool): True if new time is determined; False if undetermined.
        - arrival (bool): True if arrival delay; False if departure delay.

        Returns:
        - list[str]: Sequence of material paths.

        Example:
            >>> self._segments_delay('CN', ['MU1234'], 'Shanghai', 'Beijing', '09:45', 'weather', True, False)
            ['.../template_cn/14.wav', ...]
        """
        seg = []
        lang_l = lang.lower()
        p = lambda cat, name: os.path.join(self.material_dir, f'{cat}_{lang_l}', f'{name}.wav')

        template_prefix = "arr_" if arrival else "dep_"

        if lang == 'CN':
            seg.append(p('template', '14'))  # 各位旅客请注意
            if arrival:
                seg.append(p('template', 'arr_1'))  # 原定由
                seg.append(p('cityname', from_city))
                seg.append(p('template', 'arr_2'))  # 飞抵本场的
            else:  # Departure
                seg.append(p('template', 'dep_1'))  # 原定由本场飞往
                seg.append(p('cityname', to_city))
                seg.append(p('template', 'dep_2'))  # 的

            for f in flights:
                seg.append(p('airlines', f[:2]))
                for c in f:
                    seg.append(p('alnum', c))
            seg.append(p('template', f'{template_prefix}3'))  # 次航班

            if determined:
                seg.append(p('template', f'{template_prefix}4_det'))  # 由于...原因，将推迟到
                if reason:
                    seg.append(p('delay_reason', reason))
                seg.extend(self._speak_time(lang, est_time))
                seg.append(p('template', f'{template_prefix}5_det'))  # 起飞/到达
            else:  # Undetermined
                seg.append(p('template', f'{template_prefix}4_undet'))  # 由于...原因，不能按时...
                if reason:
                    seg.append(p('delay_reason', reason))
                seg.append(p('template', f'{template_prefix}5_undet'))  # 起飞/到达
            seg.append(p('template', 'delay_end'))  # ...抱歉

        elif lang == 'EN':
            seg.append(p('template', '1'))  # May I have...
            for f in flights:
                seg.append(p('airlines', f[:2]))
                seg.append(p('template', '3'))  # flight
                for c in f:
                    seg.append(p('alnum', c))

            if arrival:
                seg.append(p('template', 'arr_1'))  # arriving from
                seg.append(p('cityname', from_city))
            else:  # Departure
                seg.append(p('template', 'dep_1'))  # to
                seg.append(p('cityname', to_city))

            if determined:
                seg.append(p('template', f'{template_prefix}2_det'))  # has been delayed
                seg.append(p('template', 'delay_common_1'))  # due to
                if reason:
                    seg.append(p('delay_reason', reason))
                seg.append(p('template', f'{template_prefix}3_det'))  # The new estimated time of... is
                seg.extend(self._speak_time(lang, est_time))
            else:  # Undetermined
                seg.append(p('template', f'{template_prefix}2_undet'))  # is delayed
                seg.append(p('template', 'delay_common_1'))  # due to
                if reason:
                    seg.append(p('delay_reason', reason))

            seg.append(p('template', 'delay_end'))  # We apologize...

        # JP, KR to be implemented for delays
        return seg


# --- Singleton Instance ---
# Create a single instance of the system to be used by all Flask routes.
system = AirportAnnouncementSystem()

# --- Flask Routes & API Endpoints ---

@app.route('/')
def index():
    """
    Serve the main HTML page.

    Method:
    - GET /

    Returns:
    - Response: Rendered 'index.html' with injected dynamic data.

    Injected Template Variables:
    - flights: list of flight rows
    - citynames: list of available city keys
    - airlines: list of available airline codes
    - delay_reasons: list of delay reason keys
    - language_presets: list of language sequence presets
    - announcement_types: list of supported announcement types

    Example (browser):
    - Open http://127.0.0.1:5000
    """
    system.logger.info("Main page requested by a client.")
    # Pass all dynamic lists to the template
    return render_template('index.html',
                           flights=system.data,
                           citynames=system.citynames,
                           airlines=system.airlines,  # Pass airlines too for validation if needed
                           delay_reasons=system.delay_reasons,
                           language_presets=system.language_type_presets,
                           announcement_types=system.announcement_type_list)


@app.route('/output/<path:filename>')
def serve_output_file(filename):
    """
    Serve generated audio files from the output directory.

    Method:
    - GET /output/<filename>

    Path Parameters:
    - filename (str): The .wav filename previously generated.

    Returns:
    - Response: The file content (attachment or inline depending on client).

    Example:
        GET /output/MU1234_Check_in_20250101120000.wav
    """
    # Since system.output_dir is an absolute path, pass it directly
    return send_from_directory(system.output_dir, filename)


@app.route('/api/flights', methods=['POST'])
def add_flight():
    """
    Create a new flight row.

    Method:
    - POST /api/flights

    Request Body (JSON):
    - See AirportAnnouncementSystem.submit_flight(...) 'form_data' parameter.

    Returns:
    - JSON: {'success': bool, 'message': str, 'data': [...]}

    curl Example:
        curl -X POST http://127.0.0.1:5000/api/flights \
             -H "Content-Type: application/json" \
             -d "{\"flight_number\":\"MU1234\",\"departure\":\"Shanghai\",\"stopover\":\"\",\"destination\":\"Beijing\",\"divert\":\"\",\"checkin_counter\":\"A-12\",\"boarding_gate\":\"B12\",\"baggage_claim\":\"6\",\"scheduled_arrival_time\":\"09:15\",\"estimated_arrival_time\":\"09:30\",\"delay_reason\":\"weather\",\"language_type\":\"CN-EN\"}"
    """
    return jsonify(system.submit_flight(request.json, is_edit=False))


@app.route('/api/flights/<path:original_flight_number>', methods=['PUT'])
def edit_flight(original_flight_number):
    """
    Edit an existing flight row.

    Method:
    - PUT /api/flights/<original_flight_number>

    Path Parameters:
    - original_flight_number (str): The existing stored key to update.

    Request Body (JSON):
    - Same schema as POST /api/flights; see submit_flight.

    Returns:
    - JSON: {'success': bool, 'message': str, 'data': [...]}

    curl Example:
        curl -X PUT http://127.0.0.1:5000/api/flights/MU1234 \
             -H "Content-Type: application/json" \
             -d "{\"flight_number\":\"MU1234\",\"departure\":\"Shanghai\",\"stopover\":\"\",\"destination\":\"Beijing\",\"divert\":\"\",\"checkin_counter\":\"A-12\",\"boarding_gate\":\"B12\",\"baggage_claim\":\"6\",\"scheduled_arrival_time\":\"09:15\",\"estimated_arrival_time\":\"09:30\",\"delay_reason\":\"weather\",\"language_type\":\"CN-EN\"}"
    """
    return jsonify(system.submit_flight(request.json, is_edit=True, original_flight_number=original_flight_number))


@app.route('/api/flights/<path:flight_number>', methods=['DELETE'])
def delete_flight_route(flight_number):
    """
    Delete a flight by flight number.

    Method:
    - DELETE /api/flights/<flight_number>

    Returns:
    - JSON: {'success': bool, 'message': str, 'data': [...]}

    curl Example:
        curl -X DELETE http://127.0.0.1:5000/api/flights/MU1234
    """
    return jsonify(system.delete_flight(flight_number))


@app.route('/api/actions/save', methods=['POST'])
def save_info():
    """
    Persist current in-memory data to disk.

    Method:
    - POST /api/actions/save

    Returns:
    - JSON: {'success': bool, 'message': str}

    curl Example:
        curl -X POST http://127.0.0.1:5000/api/actions/save
    """
    return jsonify(system.save_info_function())


@app.route('/api/actions/refresh', methods=['POST'])
def refresh_info():
    """
    Reload data from disk into memory.

    Method:
    - POST /api/actions/refresh

    Returns:
    - JSON: {'success': bool, 'message': str, 'data': [...]}

    curl Example:
        curl -X POST http://127.0.0.1:5000/api/actions/refresh
    """
    return jsonify(system.refresh_table())


@app.route('/api/actions/clear', methods=['POST'])
def clear_info():
    """
    Clear all flight data in memory and on disk.

    Method:
    - POST /api/actions/clear

    Returns:
    - JSON: {'success': bool, 'message': str}

    curl Example:
        curl -X POST http://12-7.0.0.1:5000/api/actions/clear
    """
    return jsonify(system.clear_function())


@app.route('/api/actions/stop', methods=['POST'])
def stop_processing():
    """
    Request cancellation of active long-running tasks.

    Method:
    - POST /api/actions/stop

    Returns:
    - JSON: {'success': bool, 'message': str}

    curl Example:
        curl -X POST http://127.0.0.1:5000/api/actions/stop
    """
    return jsonify(system.stop_all_audio())


@app.route('/api/actions/synthesize', methods=['POST'])
def synthesize_audio():
    """
    Synthesize an announcement for a given flight and type.

    Method:
    - POST /api/actions/synthesize

    Request Body (JSON):
    - flight_number (str): Existing flight key.
    - announcement_type (str): One of supported types.

    Returns:
    - JSON: {'success': bool, 'message': str, 'audio_url': '/output/<file>.wav' }

    curl Example:
        curl -X POST http://127.0.0.1:5000/api/actions/synthesize \
             -H "Content-Type: application/json" \
             -d "{\"flight_number\":\"MU1234\",\"announcement_type\":\"Check_in\"}"
    """
    data = request.json
    return jsonify(system.search_and_synthesize(data.get('flight_number'), data.get('announcement_type')))


@app.route('/api/actions/convert_stereo', methods=['POST'])
def convert_stereo_route():
    """
    Start background stereo conversion for all materials in the 'material' directory.

    Method:
    - POST /api/actions/convert_stereo

    Returns:
    - JSON: {'success': True, 'message': 'Stereo conversion process started in the background.'}

    curl Example:
        curl -X POST http://127.0.0.1:5000/api/actions/convert_stereo
    """
    socketio.start_background_task(system.convert_to_stereo, system.material_dir)
    return jsonify({"success": True, "message": "Stereo conversion process started in the background."})


# --- NEW: Endpoint for clearing the cache ---
@app.route('/api/actions/clear_cache', methods=['POST'])
def clear_cache_route():
    """
    Clear all generated audio (.wav) files in the output directory.

    Method:
    - POST /api/actions/clear_cache

    Returns:
    - JSON: {'success': bool, 'message': str}

    curl Example:
        curl -X POST http://127.0.0.1:5000/api/actions/clear_cache
    """
    return jsonify(system.clear_output_cache())


@app.route('/api/actions/play_old', methods=['POST'])
def get_old_files():
    """
    List generated .wav files in the output directory, newest first.

    Method:
    - POST /api/actions/play_old

    Returns:
    - JSON:
        - success (bool)
        - files (list[str]) on success (filenames only)
        - message (str) on failure

    curl Example:
        curl -X POST http://127.0.0.1:5000/api/actions/play_old
    """
    try:
        # Get .wav files, sort by modification time (newest first)
        output_path = system.output_dir
        wavs = [f for f in os.listdir(output_path) if f.lower().endswith('.wav')]
        wavs.sort(key=lambda f: os.path.getmtime(os.path.join(output_path, f)), reverse=True)
        return jsonify({"success": True, "files": wavs})
    except Exception as e:
        system.logger.error(f"Could not read output directory: {e}")
        return jsonify({"success": False, "message": "Could not read output directory."})


def open_browser():
    """
    Open the system default web browser to the application URL.

    Parameters:
    - None

    Returns:
    - None

    Behavior:
    - Intended to be scheduled via threading.Timer after server starts.

    Example:
        >>> threading.Timer(1.5, open_browser).start()
    """
    try:
        webbrowser.open_new_tab("http://127.0.0.1:5000")
    except Exception as e:
        system.logger.error(f"Could not automatically open browser: {e}")


if __name__ == '__main__':
    print("=========================================================================")
    print("  Airport Flight Announcement System - Web Edition (Stable)")
    print("  Server starting...")
    print("  URL: http://127.0.0.1:5000")
    print("  A browser window will open automatically.")
    print("=========================================================================")
    # Use a thread to open the browser after a short delay
    threading.Timer(1.5, open_browser).start()
    # Run the Flask app with SocketIO support, allowing unsafe werkzeug for PyInstaller compatibility
    socketio.run(app, host='127.0.0.1', port=5000, log_output=False, allow_unsafe_werkzeug=True)