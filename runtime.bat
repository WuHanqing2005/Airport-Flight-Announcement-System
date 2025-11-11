@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: Airport Flight Announcement System - Automated Deployment Script
::
:: Change Log:
:: - Python installation is now manual. If not found, the user is given a URL
::   to download it, making the process more robust.
:: - Poetry installation now uses 'pip install poetry', which is simpler and
::   less prone to errors than downloading an installer script.
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
set "PYTHON_FOUND=0"
for %%G in ("%path:;=" "%") do (
    if exist "%%~G\python.exe" (
        set "PYTHON_FOUND=1"
        goto :python_check_done
    )
)
:python_check_done

if "%PYTHON_FOUND%"=="0" (
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
set "POETRY_FOUND=0"
for %%G in ("%path:;=" "%") do (
    if exist "%%~G\poetry.exe" (
        set "POETRY_FOUND=1"
        goto :poetry_check_done_loop_end
    )
)
:poetry_check_done_loop_end

if "%POETRY_FOUND%"=="0" (
    echo [INFO] Poetry not found. Attempting to install it using pip...
    pip install poetry
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Poetry using 'pip'. Please check your Python/pip installation.
        goto EndScript
    )
    echo [SUCCESS] Poetry has been installed.
) else (
    echo Poetry is already installed.
)
echo.

:: --------------------------------------------------------------------------
:: STEP 3: Install dependencies using Poetry
:: --------------------------------------------------------------------------
echo [Step 3/4] Installing project dependencies...
poetry install --no-root
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
poetry run python -m airport_flight_announcement_system.main

:EndScript
echo.
echo =================================================================
echo  Script finished. Press any key to exit.
echo =================================================================
pause >nul