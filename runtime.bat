@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: Airport Flight Announcement System - Automated Deployment Script (v3)
::
:: Change Log:
:: - Added Tsinghua University PyPI mirror to 'pip install' to prevent network timeouts.
:: - Increased pip command timeout to 100 seconds.
:: - Changed 'poetry' commands to 'python -m poetry' to avoid PATH issues after installation.
:: - Improved error handling logic for the installation step.
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
:: STEP 3: Install dependencies using Poetry
:: --------------------------------------------------------------------------
echo [Step 3/4] Installing project dependencies...
python -m poetry install --no-root -i https://pypi.tuna.tsinghua.edu.cn/simple
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