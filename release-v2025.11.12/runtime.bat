@echo off
title Airport Flight Announcement System

echo =========================================================================
echo   Starting Airport Flight Announcement System...
echo   Please wait, a browser window will open automatically.
echo   DO NOT close this window.
echo =========================================================================

REM 切换到当前脚本所在的目录，确保所有相对路径正确
cd /d %~dp0

REM 使用当前目录下的 python.exe 运行你的主程序
.\python.exe -m src.airport_flight_announcement_system.main

REM 程序结束后暂停，这样如果出错，用户可以看到错误信息
echo.
echo Program has been closed. Press any key to exit.
pause >nul