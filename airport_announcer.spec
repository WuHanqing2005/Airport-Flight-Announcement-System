# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\airport_flight_announcement_system\\main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('material', 'material'), ('data', 'data'), ('templates', 'templates'), ('static', 'static')],
    hiddenimports=['eventlet.hubs.epolls', 'eventlet.hubs.kqueue', 'eventlet.hubs.selects', 'jinja2', 'markupsafe', 'babel'],
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
    name='airport_announcer',
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
)
