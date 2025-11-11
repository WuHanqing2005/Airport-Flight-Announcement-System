@echo off
setlocal ENABLEDELAYEDEXPANSION
REM Always run from this script's directory
pushd "%~dp0"

REM 1) Check Poetry
where poetry >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Poetry not found. Please install Poetry first:
  echo https://python-poetry.org/docs/#installation
  pause
  popd
  exit /b 1
)

REM 2) Ensure deps are installed (first run may take a while)
echo [INFO] Installing dependencies with Poetry (this may run only the first time)...
poetry install --no-interaction --no-ansi
if errorlevel 1 (
  echo [ERROR] poetry install failed.
  pause
  popd
  exit /b 1
)

REM 3) Launch your app (GUI/Web)
echo [INFO] Starting application...
poetry run python -m airport_flight_announcement_system.main
set EXITCODE=%ERRORLEVEL%

REM Optional: If it's a web app, auto-open browser after a short delay
REM ping -n 3 127.0.0.1 >nul
REM start "" "http://127.0.0.1:5000"

popd
exit /b %EXITCODE%