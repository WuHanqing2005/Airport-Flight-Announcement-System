# -*- mode: python ; coding: utf-8 -*-

# --- 版本检查依然保留，这是好的实践 ---
import pkg_resources
try:
    pkg_resources.require('eventlet>=0.30.0')
except Exception as e:
    raise SystemExit(f"FATAL: Dependency check failed: {e}. Please recreate the venv and reinstall dependencies.")

block_cipher = None

a = Analysis(
    # 【修正】这里必须指向 src 目录下的 main.py
    ['src\\airport_flight_announcement_system\\main.py'],
    # 【修正】这里必须包含 src 目录，这样 import 才能找到模块
    pathex=['src'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    # hook 路径依然需要
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)