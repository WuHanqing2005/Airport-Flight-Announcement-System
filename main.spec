# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/airport_flight_announcement_system/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/airport_flight_announcement_system/static', 'static'),
        ('src/airport_flight_announcement_system/templates', 'templates'),
        ('src/airport_flight_announcement_system/data', 'data'),
        ('src/airport_flight_announcement_system/material', 'material')
    ],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Set True to show the CMD window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)