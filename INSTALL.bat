@echo off
title Installation - Face Recognition Attendance System
color 0B

echo ========================================
echo   Face Recognition Attendance System
echo   Installation Wizard
echo ========================================
echo.
echo This will install required dependencies...
echo.
pause

echo.
echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo ✅ Python is installed!
)

echo.
echo Step 2: Installing dependencies...
echo This may take 2-3 minutes...
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Installation failed!
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo ✅ Installation completed successfully!
    echo ========================================
    echo.
    echo You can now run the application using:
    echo   - Double-click RUN_APP.bat
    echo   - Or run: python attendance_app.py
    echo.
)

pause

