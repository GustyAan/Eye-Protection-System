# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('models', 'models'), ('data', 'data'), ('config.py', '.'), ('camera.py', '.'), ('detector.py', '.'), ('state_manager.py', '.'), ('logger_db.py', '.'), ('gui_user.py', '.'), ('gui_dev.py', '.')],
    hiddenimports=['tkinter', 'PIL', 'PIL._tkinter_finder', 'matplotlib', 'matplotlib.backends.backend_tkagg', 'sqlite3'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Eye_Protection_System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\pens_logo.ico'],
)
