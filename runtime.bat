@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: FINAL, PURE, NO-TRICKS VERSION
:: This script contains only the core, stable logic.
:: IT MUST BE RUN FROM A CMD.EXE PROMPT, NOT POWERSHELL.
:: ============================================================================

cd /d "%~dp0"
cls
echo =================================================================
echo  Airport Flight Announcement System - Automated Deployment
echo =================================================================
echo.
echo Current project directory: %cd%
echo.

:: -------------------------
:: STEP 1: Check for Python
:: -------------------------
echo [Step 1/4] Checking for Python installation...
where /q python >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Python not found.
    set /p "install_python=Install Python 3.11 automatically? (y/n): "
    if /i "!install_python!"=="y" (
        echo Downloading Python installer...
        powershell -NoProfile -ExecutionPolicy Bypass -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe', 'python_installer.exe')"
        if not exist "python_installer.exe" ( echo [ERROR] Download failed. & goto EndScript )
        echo Starting Python silent installation...
        start /wait "python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1
        del "python_installer.exe"
        echo [INFO] Python installed. Please CLOSE this window and RUN THIS SCRIPT AGAIN.
        goto EndScript
    ) else ( echo [ABORTED] & goto EndScript )
)
echo Python is installed.
echo.

:: -------------------------
:: STEP 2: Check for Poetry
:: -------------------------
echo [Step 2/4] Checking for Poetry installation...
where /q poetry >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Poetry not found.
    set /p "install_poetry=Install Poetry automatically? (y/n): "
    if /i "!install_poetry!"=="y" (
        echo Installing Poetry...
        powershell -NoProfile -ExecutionPolicy Bypass -Command "(New-Object System.Net.WebClient).DownloadFile('https://install.python-poetry.org', 'install-poetry.py')"
        if not exist "install-poetry.py" ( echo [ERROR] Download failed. & goto EndScript )
        python install-poetry.py
        del "install-poetry.py"
        set "PATH=%APPDATA%\pypoetry\venv\Scripts;%PATH%"
        where /q poetry >nul 2>nul
        if %errorlevel% neq 0 ( echo [ERROR] Poetry installation failed. & goto EndScript )
        echo Poetry installed for this session.
    ) else ( echo [ABORTED] & goto EndScript )
) else (
    echo Poetry is already installed.
)
echo.

:: -------------------------
:: STEP 3: Install dependencies
:: -------------------------
echo [Step 3/4] Installing project dependencies...
poetry install --no-root
if %errorlevel% neq 0 ( echo [ERROR] 'poetry install' failed. & goto EndScript )
echo Dependencies are up to date.
echo.

:: -------------------------
:: STEP 4: Run application
:: -------------------------
echo [Step 4/4] Starting the application...
poetry run python -m airport_flight_announcement_system.main

:EndScript
echo.
echo =================================================================
echo  Script finished. Press any key to exit.
echo =================================================================
pause >nul