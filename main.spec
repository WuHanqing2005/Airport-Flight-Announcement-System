# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

# spec 所在目录 = 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

# 入口脚本：如果不是 src/main.py，请改成你的实际入口，如 src/app.py
ENTRY_SCRIPT = str(SRC_DIR / "main.py")

# 需要随包分发的资源目录（按你的项目实际增删）
resource_dirs = ["templates", "static", "data", "material"]

# 收集资源
datas = []
for d in resource_dirs:
    p = PROJECT_ROOT / d
    if p.exists():
        datas.append((str(p), d))  # (源路径, 打包后目标路径)

# 动态导入缺失时，可把库名加到这里
hiddenimports = [
    # 例如: "pydub", "engineio", ...
]

a = Analysis(
    [ENTRY_SCRIPT],
    pathex=[str(SRC_DIR)],      # 关键：让 src 布局下的包可被找到
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
    name="airport-flight-announcement",  # 可改成你想要的可执行文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 调试阶段建议 True；发布可改 False 或用 -w
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,     # 如要图标，填 .ico 路径，例如 str(PROJECT_ROOT/"assets"/"app.ico")
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