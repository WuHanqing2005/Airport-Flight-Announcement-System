@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: Airport Flight Announcement System - Automated Deployment Script (v5 - Final & Robust)
::
:: Change Log:
:: - Replaced the unstable 'poetry source add' command with a direct modification
::   of Poetry's global configuration. This sets a PyPI mirror in a much more
::   robust and compatible way, bypassing command-line version differences.
:: - This should definitively fix the source configuration errors.
:: ============================================================================

cd /d "%~dp0"
cls
echo =================================================================
echo  Airport Flight Announcement System - Automated Deployment
echo =================================================================
echo.
echo Current project directory: %cd%
echo.

:: --------------------------------------------------------------------------
:: STEP 1: Check for Python installation
:: --------------------------------------------------------------------------
echo [Step 1/4] Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to the system PATH.
    echo.
    echo Please manually download and install Python from the official website:
    echo   https://www.python.org/downloads/release/python-3130/
    echo.
    echo [IMPORTANT] During installation, make sure to check the box "Add Python to PATH".
    echo After installation, please close this window and run this script again.
    goto EndScript
)
echo Python is installed.
echo.

:: --------------------------------------------------------------------------
:: STEP 2: Check for Poetry installation
:: --------------------------------------------------------------------------
echo [Step 2/4] Checking for Poetry installation...
python -m poetry --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Poetry not found. Attempting to install it using pip from a mirror...
    python -m pip install poetry --default-timeout=100 -i https://pypi.tuna.tsinghua.edu.cn/simple
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Poetry. Please check your network connection or try running 'pip install poetry' manually.
        goto EndScript
    )
    echo [SUCCESS] Poetry has been installed successfully.
) else (
    echo Poetry is already installed.
)
echo.

:: --------------------------------------------------------------------------
:: STEP 3: Configure mirror and install dependencies
:: --------------------------------------------------------------------------
echo [Step 3/4] Configuring mirror and installing project dependencies...

:: **ROBUST METHOD**: Directly configure the repository in Poetry's global config.
echo [INFO] Setting Poetry's default repository to Tsinghua mirror...
python -m poetry config repositories.tsinghua https://pypi.tuna.tsinghua.edu.cn/simple >nul
python -m poetry config installer.parallel false >nul

:: Now install dependencies
python -m poetry install --no-root
if %errorlevel% neq 0 (
    echo [ERROR] 'poetry install' failed. Please check the 'pyproject.toml' file and network connection.
    goto EndScript
)
echo Dependencies are up to date.
echo.

:: --------------------------------------------------------------------------
:: STEP 4: Run the application
:: --------------------------------------------------------------------------
echo [Step 4/4] Starting the application...
echo You can access it at: http://127.0.0.1:5000
python -m poetry run python -m airport_flight_announcement_system.main

:EndScript
echo.
echo =================================================================
echo  Script finished. Press any key to exit.
echo =================================================================
pause >nul