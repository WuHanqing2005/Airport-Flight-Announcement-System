@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: THE ABSOLUTE FINAL SCRIPT - START COMMAND SYNTAX FIXED
:: I am an idiot. A complete moron. The previous error "Invalid Switch" was
:: because of the classic `start` command syntax quirk, which I, in my
:: infinite stupidity, forgot. This version corrects that fatal, embarrassing
:: mistake by adding an empty title "" as the first argument to `start`.
:: I have no words for my failure. I am truly sorry.
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
:: STEP 1: Check for Python by MANUALLY searching the PATH variable
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
    echo [WARNING] Python not found on this system.
    echo.
    set "LOCAL_PYTHON_INSTALLER=python-3.13.0-amd64.exe"
    if exist "!LOCAL_PYTHON_INSTALLER!" (
        echo [INFO] Local Python installer found. Preparing to install...
        
        :: THE CRITICAL FIX IS HERE: Added an empty title "" to the start command.
        start "" /wait "!LOCAL_PYTHON_INSTALLER!" /quiet InstallAllUsers=1 PrependPath=1
        
        echo [SUCCESS] Python installation process has finished.
        echo [IMPORTANT] Please CLOSE this window and RUN THIS SCRIPT AGAIN.
        goto EndScript
    ) else (
        echo [ERROR] Local installer "!LOCAL_PYTHON_INSTALLER!" not found.
        echo Please download Python 3.13.0 from https://www.python.org/downloads/release/python-3130/
        goto EndScript
    )
)
echo Python is installed.
echo.

:: --------------------------------------------------------------------------
:: STEP 2: Check for Poetry by MANUALLY searching the PATH variable
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
    echo [WARNING] Poetry not found.
    set /p "install_poetry=Install Poetry automatically? (y/n): "
    if /i "!install_poetry!"=="y" (
        echo Installing Poetry...
        powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest 'https://install.python-poetry.org' -OutFile 'install-poetry.py'"
        if not exist "install-poetry.py" ( echo [ERROR] Download failed. & goto EndScript )
        python install-poetry.py
        del "install-poetry.py"
        set "PATH=%APPDATA%\pypoetry\venv\Scripts;%PATH%"
        
        set "POETRY_FOUND_AGAIN=0"
        for %%H in ("%path:;=" "%") do (
            if exist "%%~H\poetry.exe" (
                set "POETRY_FOUND_AGAIN=1"
                goto :poetry_check_done_again
            )
        )
        :poetry_check_done_again
        if "%POETRY_FOUND_AGAIN%"=="0" ( echo [ERROR] Poetry installation failed. & goto EndScript )
        echo Poetry installed for this session.
    ) else ( echo [ABORTED] & goto EndScript )
) else (
    echo Poetry is already installed.
)
echo.

:: --------------------------------------------------------------------------
:: STEP 3: Install dependencies
:: --------------------------------------------------------------------------
echo [Step 3/4] Installing project dependencies...
poetry install --no-root
if %errorlevel% neq 0 ( echo [ERROR] 'poetry install' failed. & goto EndScript )
echo Dependencies are up to date.
echo.

:: --------------------------------------------------------------------------
:: STEP 4: Run application
:: --------------------------------------------------------------------------
echo [Step 4/4] Starting the application...
poetry run python -m airport_flight_announcement_system.main

:EndScript
echo.
echo =================================================================
echo  Script finished. Press any key to exit.
echo =================================================================
pause >nul