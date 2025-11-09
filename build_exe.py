"""
Build EXE file for Face Recognition Attendance System
"""
import os
import subprocess
import shutil

print("=" * 60)
print("🚀 Building Face Recognition Attendance System EXE")
print("=" * 60)

# Clean previous builds
print("\n📦 Cleaning previous builds...")
if os.path.exists('build'):
    shutil.rmtree('build')
    print("✅ Removed 'build' folder")

if os.path.exists('dist'):
    shutil.rmtree('dist')
    print("✅ Removed 'dist' folder")

# Build command
print("\n🔨 Building EXE file...")
print("This may take a few minutes...")

# Use spec file for better control
cmd = [
    'python', '-m', 'PyInstaller',
    'attendance_system.spec',
    '--clean',  # Clean cache
    '--noconfirm'  # Don't ask for confirmation
]

try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print("✅ Build successful!")
    
    print("\n" + "=" * 60)
    print("🎉 EXE file created successfully!")
    print("=" * 60)
    print(f"\n📁 Location: dist\\AttendanceSystem.exe")
    print(f"📊 Size: ~{os.path.getsize('dist/AttendanceSystem.exe') / (1024*1024):.1f} MB")
    
    print("\n📋 Next Steps:")
    print("1. Go to 'dist' folder")
    print("2. Copy 'AttendanceSystem.exe' to any location")
    print("3. Make sure 'data' folder is in the same directory")
    print("4. Double-click to run!")
    
    print("\n💡 Tips:")
    print("• First run may be slower (Windows Defender scan)")
    print("• Keep data folder with the EXE file")
    print("• Share the entire folder (EXE + data)")
    
except subprocess.CalledProcessError as e:
    print("\n❌ Build failed!")
    print(f"Error: {e}")
    print("\nOutput:")
    print(e.stdout)
    print("\nError output:")
    print(e.stderr)

