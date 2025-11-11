@echo off
setlocal enabledelayedexpansion

:: If this script was launched from PowerShell, PS sets PSModulePath.
:: Detect that and relaunch in a real cmd.exe window to avoid PowerShell-specific behaviors.
if defined PSModulePath (
    echo Detected PowerShell. Relaunching script in a new cmd window for compatibility...
    start "" cmd /k "%~f0"
    exit /b
)

:: ====================================================================
:: Airport Flight Announcement System - Automated Deployment (CMD mode)
:: ====================================================================
cd /d "%~dp0"

echo =================================================================
echo  Airport Flight Announcement System - Automated Deployment
echo =================================================================
echo.
echo Current project directory: %cd%
echo.

:: -------------------------
:: STEP 1: Check for Python (registry-based)
:: -------------------------
echo [Step 1/4] Checking for Python installation...
set "PYTHON_FOUND=0"

:: Check Current User installations
reg query "HKCU\Software\Python\PythonCore" >nul 2>nul
if %errorlevel% equ 0 set "PYTHON_FOUND=1"

:: Check Local Machine installations (32/64-bit)
if %PYTHON_FOUND% equ 0 (
    reg query "HKLM\Software\Python\PythonCore" >nul 2>nul
    if %errorlevel% equ 0 set "PYTHON_FOUND=1"
)
if %PYTHON_FOUND% equ 0 (
    reg query "HKLM\Software\WOW6432Node\Python\PythonCore" >nul 2>nul
    if %errorlevel% equ 0 set "PYTHON_FOUND=1"
)

if "%PYTHON_FOUND%"=="0" (
    echo [WARNING] No installed Python found via registry.
    echo.
    set /p "install_python=Automatically download and install Python 3.11 now? (y/n): "
    if /i "!install_python!"=="y" (
        echo Downloading Python installer...
        set "PYTHON_INSTALLER=python_installer.exe"
        set "PYTHON_URL=https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
        powershell -NoProfile -ExecutionPolicy Bypass -Command "(New-Object System.Net.WebClient).DownloadFile('%PYTHON_URL%', '%PYTHON_INSTALLER%')"
        if not exist "%PYTHON_INSTALLER%" (
            echo [ERROR] Download failed. Check internet/firewall.
            goto EndScript
        )
        echo Starting Python silent installation (may require UAC)...
        start /wait "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1
        del "%PYTHON_INSTALLER%"
        echo [INFO] Python install attempted. Close this window and run the script again after installation completes.
        goto EndScript
    ) else (
        echo [ABORTED] Please install Python manually and add to PATH.
        goto EndScript
    )
) else (
    echo Python installation detected.
)
echo.

:: -------------------------
:: STEP 2: Check for Poetry
:: -------------------------
echo [Step 2/4] Checking for Poetry installation...
where /q poetry >nul 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Poetry not found.
    echo.
    set /p "install_poetry=Install Poetry automatically now? (y/n): "
    if /i "!install_poetry!"=="y" (
        powershell -NoProfile -ExecutionPolicy Bypass -Command "(New-Object System.Net.WebClient).DownloadFile('https://install.python-poetry.org', 'install-poetry.py')"
        if not exist "install-poetry.py" (
            echo [ERROR] Failed to download Poetry installer.
            goto EndScript
        )
        python install-poetry.py
        del "install-poetry.py"
        set "PATH=%APPDATA%\pypoetry\venv\Scripts;%PATH%"
        where /q poetry >nul 2>nul
        if %errorlevel% neq 0 (
            echo [ERROR] Poetry installation failed or PATH not updated. Please restart terminal and try again.
            goto EndScript
        )
        echo Poetry installed for this session.
    ) else (
        echo [ABORTED] Please install Poetry manually.
        goto EndScript
    )
) else (
    echo Poetry is already installed.
)
echo.

:: -------------------------
:: STEP 3: Install dependencies
:: -------------------------
echo [Step 3/4] Installing project dependencies with Poetry...
poetry install --no-root
if %errorlevel% neq 0 (
    echo [ERROR] 'poetry install' failed. See above for details.
    goto EndScript
)
echo Dependencies installed/updated.
echo.

:: -------------------------
:: STEP 4: Run main application
:: -------------------------
echo [Step 4/4] Starting the Airport Flight Announcement System...
poetry run python -m airport_flight_announcement_system.main

:EndScript
echo.
echo =================================================================
echo  Script finished. Press any key to exit.
echo =================================================================
pause >nul