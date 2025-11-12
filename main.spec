# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

hidden_imports = []
hidden_imports += collect_submodules('eventlet')
hidden_imports += collect_submodules('dns')
hidden_imports += collect_submodules('greenlet')

a = Analysis(
    ['src/airport_flight_announcement_system/main.py'],
    pathex=[],
    # --- 这是新加入的关键部分 ---
    binaries=[('external_binaries/ffmpeg.exe', '.')],
    # ---------------------------
    datas=[
        ('src/airport_flight_announcement_system/static', 'static'),
        ('src/airport_flight_announcement_system/templates', 'templates'),
        ('src/airport_flight_announcement_system/data', 'data'),
        ('src/airport_flight_announcement_system/material', 'material')
    ],
    hiddenimports=hidden_imports,
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
    name='AFAS',
    debug=False, # 可以先关掉debug，如果还出问题再打开
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Web服务最终应该在后台运行
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
    name='AFAS',
)