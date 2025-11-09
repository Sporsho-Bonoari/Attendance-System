@echo off
title Create Distribution Package
color 0B

echo ========================================
echo   Creating Distribution Package
echo ========================================
echo.

REM Create distribution folder
set DIST_FOLDER=AttendanceSystem_Distribution

if exist %DIST_FOLDER% (
    echo Removing old distribution folder...
    rmdir /s /q %DIST_FOLDER%
)

echo Creating distribution folder...
mkdir %DIST_FOLDER%
mkdir %DIST_FOLDER%\data

echo.
echo Copying files...

REM Copy main files
copy attendance_app.py %DIST_FOLDER%\
copy attendance_db.py %DIST_FOLDER%\
copy requirements.txt %DIST_FOLDER%\

REM Copy data
copy data\haarcascade_frontalface_default.xml %DIST_FOLDER%\data\

REM Copy batch files
copy INSTALL.bat %DIST_FOLDER%\
copy RUN_APP.bat %DIST_FOLDER%\

REM Copy documentation
copy USER_GUIDE.txt %DIST_FOLDER%\README.txt

echo.
echo ========================================
echo ✅ Distribution package created!
echo ========================================
echo.
echo Location: %DIST_FOLDER%\
echo.
echo Package contents:
echo   - attendance_app.py (Main application)
echo   - attendance_db.py (Database module)
echo   - requirements.txt (Dependencies)
echo   - data\haarcascade...xml (Face detection model)
echo   - INSTALL.bat (Setup script)
echo   - RUN_APP.bat (Run script)
echo   - README.txt (User guide)
echo.
echo 📦 Total size: ~5 MB (small and portable!)
echo.
echo Next steps:
echo 1. ZIP the "%DIST_FOLDER%" folder
echo 2. Share with users
echo 3. Users run INSTALL.bat once
echo 4. Users run RUN_APP.bat to use
echo.
echo ✨ Camera will work perfectly! ✨
echo.

pause

