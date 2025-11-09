@echo off
echo ========================================
echo   Face Recognition Attendance System
echo   EXE Builder (Fixed Version)
echo ========================================
echo.
echo Cleaning old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.
echo Building EXE file with spec file...
echo This will take 3-5 minutes.
echo.

python -m PyInstaller attendance_system.spec --clean --noconfirm

echo.
if exist dist\AttendanceSystem.exe (
    echo ========================================
    echo ✅ Build complete!
    echo ========================================
    echo.
    echo EXE Location: dist\AttendanceSystem.exe
    echo.
) else (
    echo ========================================
    echo ❌ Build failed!
    echo ========================================
    echo Please check the errors above.
    echo.
)
pause

