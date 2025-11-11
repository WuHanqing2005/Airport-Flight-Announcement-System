# -*- mode: python ; coding: utf-8 -*-

"""
Spec file placed at project ROOT.
Run from root:
    poetry run pyinstaller main.spec
or:
    pyinstaller main.spec
"""

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# 项目根目录 = 当前工作目录（要求你在根目录执行命令）
PROJECT_ROOT = Path.cwd()
SRC_DIR = PROJECT_ROOT / "src"

# 入口脚本。如果你的真实入口不是 main.py 请改成 app.py 等：
ENTRY_SCRIPT = str(SRC_DIR / "main.py")

# 打包的资源目录（位于项目根目录）。按实际增删。
RESOURCE_DIRS = ["templates", "static", "data", "material"]

datas = []
for d in RESOURCE_DIRS:
    p = PROJECT_ROOT / d
    if p.exists():
        datas.append((str(p), d))

# 收集 eventlet 全部子模块，解决动态导入问题
hiddenimports = collect_submodules("eventlet")

# 如果你还用了 flask_socketio 也可收集：
try:
    hiddenimports += collect_submodules("flask_socketio")
except Exception:
    pass

# 额外收集可能需要的包数据
datas += collect_data_files("eventlet")

a = Analysis(
    [ENTRY_SCRIPT],
    pathex=[str(SRC_DIR)],  # src 布局关键
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="airport-flight-announcement",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 调试阶段保留 True
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="airport-flight-announcement",
)