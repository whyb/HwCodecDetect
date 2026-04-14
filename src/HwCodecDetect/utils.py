import os
import os.path
import tempfile
import sys
from pathlib import Path

def get_temp_path():
    app_id = "HwCodecDetect"
    
    candidates = []

    candidates.append(os.path.join(tempfile.gettempdir(), app_id))

    if sys.platform == "win32":
        local_appdata = os.getenv("LOCALAPPDATA")
        if local_appdata:
            candidates.append(os.path.join(local_appdata, app_id))
    elif sys.platform == "darwin":
        candidates.append(os.path.expanduser(f"~/Library/Caches/{app_id}"))
    elif sys.platform.startswith("linux"):
        xdg_cache = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
        candidates.append(os.path.join(xdg_cache, app_id))

    candidates.append(os.path.expanduser(f"~/.{app_id}"))

    for path in candidates:
        if not path:
            continue
        
        try:
            os.makedirs(path, mode=0o755, exist_ok=True)
            test_file = os.path.join(path, ".perm_test")
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write("test")
            
            if os.path.exists(test_file):
                os.remove(test_file)
                return path
        except Exception as e:
            print(f"Warning: Attempting path {path} failed: {e}")
            continue

    return os.getcwd()


def get_local_version():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    v_path = os.path.join(base_path, "VERSION")

    if not os.path.exists(v_path):
        v_path = os.path.join(base_path, "..", "..", "VERSION")

    try:
        with open(v_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Unknown Version"