# hook-eventlet.py
from PyInstaller.utils.hooks import collect_submodules

# Collect all submodules from 'eventlet'.
hiddenimports = collect_submodules('eventlet')

# CRITICAL: Collect all submodules from 'dns' (dnspython).
hiddenimports += collect_submodules('dns')