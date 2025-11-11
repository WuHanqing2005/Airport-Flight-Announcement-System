@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: FINAL VERSION - LOCAL INSTALLER PRIORITY
:: Logic: Checks for a local 'python-3.13.0-amd64.exe'. If found, uses it.
:: If not found, directs the user to the Python download page.
:: This version is stable and follows the user's latest request precisely.
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
    echo [WARNING] Python not found on this system.
    echo.
    
    :: New Logic: Check for the local installer first.
    set "LOCAL_PYTHON_INSTALLER=python-3.13.0-amd64.exe"
    
    if exist "%LOCAL_PYTHON_INSTALLER%" (
        echo [INFO] Local Python installer found. Preparing to install...
        echo [INFO] This may require administrator privileges (UAC).
        echo.
        
        start /wait "%LOCAL_PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1
        
        echo [SUCCESS] The Python installation process has finished.
        echo [IMPORTANT] To continue, please CLOSE this window and RUN THIS SCRIPT AGAIN.
        goto EndScript
        
    ) else (
        echo [ERROR] The local Python installer ("%LOCAL_PYTHON_INSTALLER%") was not found in the project directory.
        echo.
        echo Please manually download the correct Python 3.13.0 version for your system
        echo from the official website:
        echo.
        echo   https://www.python.org/downloads/release/python-3130/
        echo.
        echo After installing Python, run this script again.
        goto EndScript
    )
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
        powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest 'https://install.python-poetry.org' -OutFile 'install-poetry.py'"
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