import os
import os.path
import tempfile
import sys
import re
import subprocess
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


def get_ffmpeg_supported_codecs():
    """Get supported encoders, decoders and hwaccels from ffmpeg.

    Returns:
        tuple: (supported_encoders, supported_decoders) - two sets containing:
            - supported_encoders: set of supported encoder names and hwaccel methods
            - supported_decoders: set of supported decoder names and hwaccel methods
    """
    supported_encoders = set()
    supported_decoders = set()

    creation_flags = 0
    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NO_WINDOW
    try:
        # Get encoders
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            creationflags=creation_flags,
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                # Parse lines like:  V....D av1_nvenc          NVIDIA NVENC av1 encoder (codec av1)
                # Format: [VSA][6 chars of flags] [codec name] [description]
                match = re.search(r'^\s*[VSA].{6}\s*(\S+)', line)
                if match:
                    supported_encoders.add(match.group(1))

        # Get decoders
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-decoders"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            creationflags=creation_flags,
        )
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                # Parse lines like:  V..... av1_cuvid          Nvidia CUVID AV1 decoder (codec av1)
                match = re.search(r'^\s*[VSA].{6}\s*(\S+)', line)
                if match:
                    supported_decoders.add(match.group(1))

        # Get hardware acceleration methods
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-hwaccels"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            creationflags=creation_flags,
        )
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                line = line.strip()
                # Skip empty lines and header
                if not line or line.startswith('Hardware acceleration'):
                    continue
                # Add hwaccel methods to both encoders and decoders
                supported_encoders.add(line)
                supported_decoders.add(line)

    except Exception as e:
        print(f"Warning: Failed to get ffmpeg codecs: {e}", file=sys.stderr)

    return supported_encoders, supported_decoders


def check_codec_support(encoders_dict, decoders_dict):
    """Check which hardware codecs are supported by current ffmpeg version.

    Args:
        encoders_dict: Dictionary of encoder definitions (like ENCODERS)
        decoders_dict: Dictionary of decoder definitions (like DECODERS)

    Returns:
        tuple: (unsupported_encoders, unsupported_decoders) - two sets containing
               the names of unsupported encoders and decoders
    """
    from colorama import Fore, Style

    supported_encoders, supported_decoders = get_ffmpeg_supported_codecs()

    unsupported_encoders = set()
    unsupported_decoders = set()

    # Check encoders
    for codec, info in encoders_dict.items():
        for encoder in info.get('hw_encoders', []):
            if encoder not in supported_encoders:
                unsupported_encoders.add(encoder)
                print(f"{Fore.YELLOW}Warning: Encoder '{encoder}' is not supported by current FFmpeg version{Style.RESET_ALL}")

    # Check decoders
    for codec, info in decoders_dict.items():
        for decoder in info.get('hw_decoders', []):
            if decoder not in supported_decoders:
                unsupported_decoders.add(decoder)
                print(f"{Fore.YELLOW}Warning: Decoder '{decoder}' is not supported by current FFmpeg version{Style.RESET_ALL}")

    return unsupported_encoders, unsupported_decoders

def get_stty_cfg():
    try:
        return subprocess.check_output(["stty", "--save"], text=True).strip()
    except:
        return None

def set_stty_cfg(cfg):
    if not cfg: return
    try:
        subprocess.run(["stty", cfg])
    except:
        pass
