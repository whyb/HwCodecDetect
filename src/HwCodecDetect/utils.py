import os
import os.path
import shutil
import tempfile
import sys
import re
import shlex
import subprocess
from pathlib import Path

# ─── Colorful CLI theme (ANSI equivalents of the GUI theme) ─────────────────
# These are only used when --colorful is enabled.

class _ColorfulTheme:
    """ANSI color palette inspired by the GUI Fluent Design dark theme."""
    # Semantic status (matching gui.py's GREEN/RED/TEXT_DIM)
    SUCCESS  = "\033[38;2;74;222;128m"   # #4ade80
    ERROR    = "\033[38;2;248;113;113m"  # #f87171
    WARNING  = "\033[38;2;251;191;36m"   # #fbbf24
    SKIPPED  = "\033[38;2;98;104;120m"   # #626878
    # Accent colors
    ACCENT   = "\033[38;2;107;138;255m"  # #6b8aff
    CYAN     = "\033[38;2;103;232;249m"  # #67e8f9
    PURPLE   = "\033[38;2;192;132;252m"  # #c084fc
    # Text
    TEXT_PRIMARY   = "\033[38;2;236;237;242m"  # #ecedf2
    TEXT_SECONDARY = "\033[38;2;145;151;168m"  # #9197a8
    # Table
    BORDER  = "\033[38;2;58;61;72m"      # #3a3d48
    DIM     = "\033[38;2;98;104;120m"    # #626878
    # Box-drawing characters for tables
    TL = "┌"; TR = "┐"; BL = "└"; BR = "┘"
    H  = "─"; V  = "│"
    LT = "├"; RT = "┤"; TT = "┬"; BT = "┴"; XX = "┼"
    # Symbols (matching gui.py's ● / — style)
    SYM_SUCCESS = " ● "
    SYM_ERROR   = " ● "
    SYM_SKIP    = " — "
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM_STYLE = "\033[2m"


COLORFUL = _ColorfulTheme()

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
            timeout=10,
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
            timeout=10,
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
            timeout=10,
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


def check_codec_support(encoders_dict, decoders_dict, colorful=False):
    """Check which hardware codecs are supported by current ffmpeg version.

    Args:
        encoders_dict: Dictionary of encoder definitions (like ENCODERS)
        decoders_dict: Dictionary of decoder definitions (like DECODERS)
        colorful: If True, use colorful theme for warning output

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
                if colorful:
                    print(f"{COLORFUL.WARNING}⚠ Encoder '{encoder}' is not supported by current FFmpeg version{COLORFUL.RESET}")
                else:
                    print(f"{Fore.YELLOW}Warning: Encoder '{encoder}' is not supported by current FFmpeg version{Style.RESET_ALL}")

    # Check decoders
    for codec, info in decoders_dict.items():
        for decoder in info.get('hw_decoders', []):
            if decoder not in supported_decoders:
                unsupported_decoders.add(decoder)
                if colorful:
                    print(f"{COLORFUL.WARNING}⚠ Decoder '{decoder}' is not supported by current FFmpeg version{COLORFUL.RESET}")
                else:
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


# ---------------------------------------------------------------------------
# Shared FFmpeg subprocess helpers
# ---------------------------------------------------------------------------

def run_ffmpeg_command(command, verbose=True, timeout=10):
    """Execute an FFmpeg command and return (success, stdout, stderr).

    Uses CREATE_NO_WINDOW on Windows to prevent console window flashes.
    Always captures stdout/stderr via PIPE.
    Kills the process if it exceeds *timeout* seconds (default: 10).
    """
    creation_flags = 0
    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NO_WINDOW
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=creation_flags,
            text=True,
            timeout=timeout,
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return (False, "", f"FFmpeg command timed out after {timeout}s")
    except subprocess.CalledProcessError as e:
        return (False, e.stdout, e.stderr)
    except FileNotFoundError:
        return (False, "", "FFmpeg executable not found")


def get_file_extension(codec):
    """Return the appropriate file extension for a given codec."""
    if codec == "prores":
        return ".mov"
    if codec in ("vp8", "vp9"):
        return ".webm"
    return ".mp4"


def format_verbose_log(test_label, codec, name, key, status, stdout, stderr, command, colorful=False):
    """Format and print a verbose FFmpeg test log block."""
    info_str = f"codec: {codec}, {name}, resolution/format: {key}, status: {status}"
    command_str = " ".join(shlex.quote(arg) for arg in command)
    if stdout and stdout.strip() and stderr and stderr.strip():
        command_log = f"{stdout.strip()}\n{stderr.strip()}"
    elif stdout and stdout.strip():
        command_log = stdout.strip()
    elif stderr and stderr.strip():
        command_log = stderr.strip()
    else:
        command_log = "(none)"

    if colorful:
        C = COLORFUL
        status_color = C.SUCCESS if status == "succeeded" else C.ERROR if status == "failed" else C.DIM
        sep = C.BORDER + ("─" * 56) + C.RESET
        log_message = f"""
{sep}
{C.ACCENT}{C.BOLD}[{test_label}]{C.RESET}
{C.TEXT_PRIMARY}{info_str}{C.RESET}

{C.CYAN}[FFmpeg Command]{C.RESET}
{C.DIM_STYLE}{command_str}{C.RESET}

{C.CYAN}[Command Log]{C.RESET}
{command_log}

""".strip()
        print(log_message)
    else:
        log_message = f"""
==================================================
[{test_label}]
{info_str}

[FFmpeg Command]
{command_str}

[Command Log]
{command_log}

""".strip()
        print(log_message)


# ---------------------------------------------------------------------------
# ANSI / display helpers
# ---------------------------------------------------------------------------

_ANSI_ESCAPE_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def get_display_width(s):
    """Calculate the display width of a string, ignoring ANSI escape codes."""
    return len(_ANSI_ESCAPE_RE.sub('', s))


# ---------------------------------------------------------------------------
# Pixel format helpers
# ---------------------------------------------------------------------------

def get_out_pix_fmt(bit_depth, chroma):
    """Map (bit_depth, chroma) to the output pixel format string."""
    if bit_depth == 8:
        if chroma == "4:2:0":
            return "yuv420p"
        elif chroma == "4:2:2":
            return "yuv422p"
        else:
            return "yuv444p"
    elif bit_depth == 10:
        if chroma == "4:2:0":
            return "p010le"
        elif chroma == "4:2:2":
            return "yuv422p10le"
        else:
            return "yuv444p10le"
    else:  # 12-bit
        if chroma == "4:2:0":
            return "yuv420p12le"
        elif chroma == "4:2:2":
            return "yuv422p12le"
        else:
            return "yuv444p12le"


# ---------------------------------------------------------------------------
# Resource / temp directory helpers
# ---------------------------------------------------------------------------

def get_resource_path(relative_path):
    """Resolve a resource path, handling PyInstaller _MEIPASS."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def prepare_temp_dir(suffix):
    """Create a clean temporary directory for HwCodecDetect tests.

    Removes any existing directory with the same name first.
    On Windows, kills lingering ffmpeg processes that may hold file locks.
    Returns the path to the new directory.
    """
    temp_dir = os.path.join(get_temp_path(), f"HwCodecDetect_{suffix}")
    if os.path.exists(temp_dir):
        # On Windows, lingering ffmpeg processes from a previous (possibly
        # interrupted) run can hold file locks.  Kill them so rmtree succeeds.
        if sys.platform == "win32":
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", "ffmpeg.exe"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5,
                )
            except Exception:
                pass
        shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir


# ---------------------------------------------------------------------------
# Codec support reporting
# ---------------------------------------------------------------------------

def print_codec_support_report(unsupported_encoders, unsupported_decoders, colorful=False):
    """Print a summary of unsupported codecs."""
    if colorful:
        C = COLORFUL
        if unsupported_encoders or unsupported_decoders:
            print(f"\n{C.WARNING}⚠ Found {len(unsupported_encoders)} unsupported encoder(s) and {len(unsupported_decoders)} unsupported decoder(s){C.RESET}")
            print(f"{C.DIM}  These codecs will be marked as unavailable in the results.{C.RESET}\n")
        else:
            print(f"{C.SUCCESS}✔ All defined hardware codecs are supported.{C.RESET}\n")
    else:
        if unsupported_encoders or unsupported_decoders:
            print(f"\nFound {len(unsupported_encoders)} unsupported encoder(s) and {len(unsupported_decoders)} unsupported decoder(s).")
            print("These codecs will be marked as unavailable '-' in the results.\n")
        else:
            print("All defined hardware codecs are supported.\n")
