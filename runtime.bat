@echo off
setlocal enabledelayedexpansion

:: 1. Set the working directory to the script's location
:: 将当前目录切换到bat文件所在的目录
cd /d "%~dp0"
echo =================================================================
echo  Airport Flight Announcement System Runtime Environment Setup
echo =================================================================
echo.
echo Current project directory: %cd%
echo.

:: 2. Check for Python installation
:: 检查Python是否安装并已添加到PATH
echo [Step 1/4] Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Python is not found on your system.
    echo.
    set /p "install_python=Do you want to automatically download and install Python now? (y/n): "
    if /i "!install_python!"=="y" (
        echo.
        echo Downloading Python installer... Please wait.
        :: 使用PowerShell下载Python安装包 (以Python 3.11.8为例，这是一个稳定版本)
        set "PYTHON_INSTALLER=python_installer.exe"
        set "PYTHON_URL=https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
        powershell -NoProfile -ExecutionPolicy Bypass -Command "(New-Object System.Net.WebClient).DownloadFile('%PYTHON_URL%', '%PYTHON_INSTALLER%')"
        
        if not exist %PYTHON_INSTALLER% (
            echo [ERROR] Failed to download Python installer. Please check your internet connection.
            pause
            exit /b 1
        )
        
        echo.
        echo Download complete. Starting Python installation...
        echo This will be a quiet installation. Please approve any User Account Control (UAC) prompts.
        
        :: /quiet: 静默安装
        :: PrependPath=1: 将Python添加到系统PATH (非常重要！)
        :: InstallAllUsers=1: 为所有用户安装 (推荐)
        start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
        
        del %PYTHON_INSTALLER%
        
        echo.
        echo Python installation should be complete.
        echo IMPORTANT: A terminal restart is needed to refresh the environment variables.
        echo Please close this window and run the script again.
        echo.
        pause
        exit /b 0

    ) else (
        echo.
        echo Please visit https://www.python.org/downloads/ to download and install Python manually.
        echo IMPORTANT: During installation, please make sure to check the box that says "Add Python to PATH".
        echo.
        pause
        exit /b 1
    )
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% found.
echo.


:: 3. Check for Poetry installation
:: 检查Poetry是否安装
echo [Step 2/4] Checking for Poetry installation...
poetry --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Poetry is not found. Poetry is required to manage project dependencies.
    echo.
    set /p "install_poetry=Do you want to install Poetry automatically now? (y/n): "
    if /i "!install_poetry!"=="y" (
        echo.
        echo Installing Poetry using the recommended installer...
        echo This may take a few moments.
        powershell -NoProfile -ExecutionPolicy Bypass -Command "(New-Object System.Net.WebClient).DownloadFile('https://install.python-poetry.org', 'install-poetry.py')"
        python install-poetry.py
        del install-poetry.py
        echo.
        echo IMPORTANT:
        echo Poetry has been installed. You may need to restart your terminal or computer
        echo for the PATH environment variable to be updated.
        echo The script will now add Poetry to the PATH for this session and continue.
        echo.
        set "PATH=%APPDATA%\pypoetry\venv\Scripts;%PATH%"
        
        :: Verify again after attempting to add to PATH
        poetry --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo [ERROR] Poetry installation seems to have failed or PATH is not correctly set.
            echo Please restart your terminal/computer and run this script again.
            pause
            exit /b 1
        )
        echo Poetry installed and configured for this session successfully.
    ) else (
        echo Please install Poetry manually by following the instructions at https://python-poetry.org/docs/#installation
        pause
        exit /b 1
    )
) else (
    echo Poetry is already installed.
)
echo.

:: 4. Install dependencies using Poetry
:: 使用Poetry安装项目依赖
echo [Step 3/4] Installing project dependencies with Poetry...
echo This might take a while if this is the first time running the script.
poetry install --no-root
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install project dependencies using 'poetry install'.
    echo Please check the error messages above. You might need to resolve them manually.
    echo.
    pause
    exit /b 1
)
echo Dependencies are up to date.
echo.

:: 5. Run the application
:: 运行主程序
echo [Step 4/4] Starting the Airport Flight Announcement System...
echo =================================================================
echo.
poetry run python -m airport_flight_announcement_system.main

echo.
echo =================================================================
echo The program has exited.
echo =================================================================
pause
endlocal