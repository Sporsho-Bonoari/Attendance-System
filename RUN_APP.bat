@echo off
title Face Recognition Attendance System
color 0A
cls

echo ========================================
echo   Face Recognition Attendance System
echo        Starting Application...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo.
    echo Please run INSTALL.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import cv2, sklearn, PIL" >nul 2>&1
if errorlevel 1 (
    echo ⚠ Dependencies not installed!
    echo.
    echo Please run INSTALL.bat first.
    echo.
    pause
    exit /b 1
)

REM Run the application
echo ✅ Starting application...
echo.
pythonw attendance_app.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ❌ Application encountered an error
    echo ========================================
    echo.
    echo Please check:
    echo - Camera is connected and working
    echo - Camera permission is enabled
    echo - No other apps are using the camera
    echo.
    pause
)


