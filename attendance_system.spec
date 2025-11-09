# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# Hidden imports for sklearn and scipy
hidden_imports = [
    'sklearn.neighbors._typedefs',
    'sklearn.neighbors._quad_tree',
    'sklearn.tree',
    'sklearn.tree._utils',
    'sklearn.utils._cython_blas',
    'sklearn.utils._typedefs',
    'sklearn.utils._heap',
    'sklearn.utils._sorting',
    'sklearn.utils._vector_sentinel',
    'sklearn.utils._array_api',
    'sklearn.externals',
    'sklearn.externals.array_api_compat',
    'sklearn.externals.array_api_compat.numpy',
    'sklearn.externals.array_api_compat.numpy.fft',
    'sklearn.externals.array_api_compat.numpy.linalg',
    'scipy._lib.messagestream',
    'scipy._cyutility',
    'scipy.sparse.csgraph._validation',
    'scipy.sparse._csparsetools',
    'scipy.special._ufuncs_cxx',
    'scipy.linalg.cython_blas',
    'scipy.linalg.cython_lapack',
    'scipy.integrate',
    'scipy.integrate._odepack',
    'scipy.integrate._quadpack',
    'scipy.integrate._ode',
    'scipy.integrate._dop',
    'scipy.integrate._lsoda',
    'scipy.special',
    'scipy.special._ufuncs',
    'scipy.special._cdflib',
    'numpy.fft',
    'numpy.linalg',
    'numpy.random',
    'cv2',
    'PIL._tkinter_finder',
    'win32com.client',
    'win32com.shell',
    'win32api',
    'win32con',
    'pywintypes',
    'pythoncom',
]

# Collect all sklearn submodules
all_sklearn = collect_submodules('sklearn')
all_scipy = collect_submodules('scipy')

import os
from glob import glob

# Get OpenCV DLLs
cv2_path = os.path.dirname(__import__('cv2').__file__)
cv2_binaries = []
for dll in glob(os.path.join(cv2_path, '*.dll')):
    cv2_binaries.append((dll, '.'))

a = Analysis(
    ['attendance_app.py'],
    pathex=[],
    binaries=cv2_binaries,
    datas=[('data', 'data')],
    hiddenimports=hidden_imports + all_sklearn + all_scipy,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib.tests',
        'numpy.random._examples',
        'IPython',
        'jupyter',
        'notebook',
        'torch.distributions',
        'torchvision.datasets',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AttendanceSystem',
    debug=True,  # Enable debug mode
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disable UPX compression for debugging
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console window to see errors
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

