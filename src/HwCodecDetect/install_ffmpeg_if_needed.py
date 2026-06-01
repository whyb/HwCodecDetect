"""
FFmpeg installation checker and auto-installer.

Supports:
  - Windows (winget, chocolatey, scoop, manual download for x86_64/ARM64/x86)
  - Linux (apt, dnf, yum, pacman, zypper, apk, xbps, emerge, nix, snap, flatpak, static binary fallback)
  - macOS (Homebrew, MacPorts, conda, nix, manual download, auto Homebrew install)
  - FreeBSD / OpenBSD / NetBSD (pkg, pkg_add, ports)

Features:
  - CPU architecture detection (x86_64, ARM64, ARMv7, etc.)
  - Comprehensive Linux distribution detection
  - Download with retry, timeout, progress bar, and SSL/CA-bundle support
  - Post-installation verification (ffmpeg + ffprobe)
  - Graceful fallback chain with informative error messages
  - Docker/CI environment awareness
  - Preserves Windows registry PATH value type (REG_SZ / REG_EXPAND_SZ)
"""

import os
import sys
import platform
import subprocess
import shutil
import urllib.request
import urllib.error
import zipfile
import tempfile
import time
import ssl

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DOWNLOAD_TIMEOUT = 120  # seconds per download attempt
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds, multiplied by attempt number

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def _run_cmd(command, check=False, timeout=120):
    """Run a subprocess command, returning the CompletedProcess.

    On Windows the CREATE_NO_WINDOW flag is used so that no console window
    pops up.  All exceptions are caught and the caller receives ``None``.
    """
    creation_flags = 0
    if sys.platform == "win32":
        try:
            creation_flags = subprocess.CREATE_NO_WINDOW
        except AttributeError:
            pass
    try:
        return subprocess.run(
            command,
            check=check,
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=creation_flags,
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired, KeyboardInterrupt):
        return None


def _is_frozen():
    """Return True when running inside a PyInstaller / cx_Freeze bundle."""
    return getattr(sys, "frozen", False) or getattr(sys, "_MEIPASS", None) is not None


# ---------------------------------------------------------------------------
# Architecture detection
# ---------------------------------------------------------------------------

_ARCH_MAP = {
    "x86_64": "x86_64",
    "amd64": "x86_64",
    "x86_32": "x86",
    "i386": "x86",
    "i686": "x86",
    "aarch64": "aarch64",
    "arm64": "aarch64",       # macOS Apple Silicon
    "armv7l": "armv7",
    "armv6l": "armv6",
}


def get_architecture():
    """Return a normalised architecture string such as ``x86_64``, ``aarch64``,
    ``armv7``, etc."""
    machine = platform.machine().lower()
    return _ARCH_MAP.get(machine, machine)


def _get_python_arch_bits():
    """Return the pointer size of the running Python interpreter (32 or 64)."""
    import struct
    return struct.calcsize("P") * 8


# ---------------------------------------------------------------------------
# Linux distribution detection
# ---------------------------------------------------------------------------

def get_linux_distro():
    """Detect the Linux distribution using ``/etc/os-release`` and fallbacks.

    Returns a dict with keys: ``id``, ``id_like`` (list), ``name``.
    All values are lower-cased.
    """
    distro = {"id": "unknown", "id_like": [], "name": ""}

    # ---- Primary: /etc/os-release (standard on virtually all modern distros) ----
    os_release = "/etc/os-release"
    if not os.path.exists(os_release):
        os_release = "/usr/lib/os-release"

    if os.path.exists(os_release):
        # Parse INI-style file manually (safer than configparser because
        # /etc/os-release may contain unquoted values with special chars).
        try:
            with open(os_release, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip().lower()
                    # Strip optional surrounding quotes from value
                    value = value.strip().strip('"').strip("'")
                    if key == "id":
                        distro["id"] = value.lower()
                    elif key == "id_like":
                        # May be space- or comma-separated
                        raw = value.replace(",", " ")
                        distro["id_like"] = [v.strip().lower() for v in raw.split() if v.strip()]
                    elif key == "name":
                        distro["name"] = value
        except OSError:
            pass

    # ---- Fallback heuristics ----
    if distro["id"] == "unknown":
        fallbacks = [
            ("/etc/arch-release", "arch"),
            ("/etc/debian_version", "debian"),
            ("/etc/redhat-release", "redhat"),
            ("/etc/centos-release", "centos"),
            ("/etc/fedora-release", "fedora"),
            ("/etc/alpine-release", "alpine"),
            ("/etc/SuSE-release", "suse"),
            ("/etc/void-release", "void"),
        ]
        for path, name in fallbacks:
            if os.path.exists(path):
                distro["id"] = name
                break

    return distro


def _distro_matches(distro, *candidates):
    """Check if the detected distro (or any of its ``id_like`` parents) matches
    one of the *candidates*."""
    ids = {distro["id"]} | set(distro.get("id_like", []))
    for c in candidates:
        if c in ids:
            return True
    return False


# ---------------------------------------------------------------------------
# Docker / CI detection helpers
# ---------------------------------------------------------------------------

def _is_docker_or_ci():
    """Return True when likely running inside Docker or a CI system."""
    if os.path.exists("/.dockerenv"):
        return True
    # cgroup v1
    try:
        with open("/proc/1/cgroup", "r", errors="ignore") as f:
            if "docker" in f.read():
                return True
    except OSError:
        pass
    # Common CI environment variables
    for var in ("CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_HOME", "BUILDKITE", "TRAVIS", "CIRCLECI", "TF_BUILD"):
        if os.environ.get(var):
            return True
    return False


def _is_root():
    """Return True if running as root (UID 0)."""
    if sys.platform == "win32":
        return False  # Windows doesn't have UID 0 concept in the same way
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False


def _sudo_prefix():
    """Return the command prefix for privilege escalation.

    If already root or inside Docker (as root) → empty list.
    If ``sudo`` is available → ``["sudo"]``.
    Otherwise → empty list (will likely fail with a permission error, but
    the caller can catch that).
    """
    if _is_root():
        return []
    if shutil.which("sudo"):
        return ["sudo"]
    return []


# ---------------------------------------------------------------------------
# System proxy detection
# ---------------------------------------------------------------------------

def _ensure_system_proxy():
    """Detect the system proxy and set ``HTTP_PROXY`` / ``HTTPS_PROXY``
    environment variables if they are not already set.

    This ensures both ``urllib.request`` and child subprocesses (winget, choco,
    brew, etc.) can reach the internet through a corporate / system proxy.
    """
    # Skip if proxy env vars are already configured
    if os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY") or os.environ.get("ALL_PROXY"):
        return

    proxy_url = None

    # --- Windows: read from registry ---
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                0, winreg.KEY_READ,
            )
            try:
                enabled, _ = winreg.QueryValueEx(key, "ProxyEnable")
                if enabled:
                    server, _ = winreg.QueryValueEx(key, "ProxyServer")
                    if server:
                        # server may be "host:port" or "http=host:port;https=host:port"
                        if "=" in server or ";" in server:
                            # Multi-protocol format: pick http or first entry
                            for part in server.split(";"):
                                part = part.strip()
                                if part.startswith("http="):
                                    proxy_url = "http://" + part.split("=", 1)[1]
                                    break
                            if not proxy_url:
                                proxy_url = "http://" + server.split(";")[0].strip().split("=", 1)[-1]
                        else:
                            proxy_url = "http://" + server
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
        except Exception:
            pass

    # --- macOS: read from SystemConfiguration via scutil ---
    elif sys.platform == "darwin":
        result = _run_cmd(["scutil", "--proxy"], timeout=10)
        if result and result.returncode == 0:
            proxy_host = None
            proxy_port = None
            for line in result.stdout.splitlines():
                line = line.strip()
                if line.startswith("HTTPSPort") or line.startswith("HTTPPort"):
                    parts = line.split(":", 1)
                    if len(parts) == 2 and parts[1].strip():
                        proxy_port = parts[1].strip()
                if line.startswith("HTTPSProxy") or line.startswith("HTTPProxy"):
                    parts = line.split(":", 1)
                    if len(parts) == 2 and parts[1].strip():
                        if not proxy_host:  # first one wins (HTTPS preferred)
                            proxy_host = parts[1].strip()
            if proxy_host:
                if ":" in proxy_host:
                    proxy_url = "http://" + proxy_host
                elif proxy_port:
                    proxy_url = f"http://{proxy_host}:{proxy_port}"
                else:
                    proxy_url = "http://" + proxy_host
        # Fallback: stdlib (reads macOS SystemConfiguration)
        if not proxy_url:
            try:
                proxies = urllib.request.getproxies()
                proxy_url = proxies.get("https") or proxies.get("http")
            except Exception:
                pass

    # --- Linux: check desktop environment proxy settings ---
    elif sys.platform.startswith("linux"):
        # GNOME / Unity / Cinnamon (gsettings)
        if not proxy_url:
            for schema in ("org.gnome.system.proxy.http", "org.gnome.system.proxy"):
                result = _run_cmd(
                    ["gsettings", "get", schema, "host"], timeout=5,
                )
                if result and result.returncode == 0 and result.stdout.strip() not in ("''", ""):
                    host = result.stdout.strip().strip("'")
                    port_result = _run_cmd(
                        ["gsettings", "get", schema, "port"], timeout=5,
                    )
                    port = port_result.stdout.strip().strip("'") if port_result else ""
                    if host:
                        proxy_url = f"http://{host}:{port}" if port else f"http://{host}"
                        break

        # KDE (kreadconfig5 / kreadconfig6)
        if not proxy_url:
            for cmd_name in ("kreadconfig6", "kreadconfig5"):
                if not shutil.which(cmd_name):
                    continue
                result = _run_cmd(
                    [cmd_name, "--group", "Proxy Settings", "--key", "httpProxy"], timeout=5,
                )
                if result and result.returncode == 0 and result.stdout.strip():
                    proxy_url = "http://" + result.stdout.strip()
                    break

        # /etc/environment (system-wide)
        if not proxy_url:
            try:
                with open("/etc/environment", "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("http_proxy=") or line.startswith("HTTP_PROXY="):
                            proxy_url = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break
            except OSError:
                pass

    if proxy_url:
        os.environ.setdefault("HTTP_PROXY", proxy_url)
        os.environ.setdefault("HTTPS_PROXY", proxy_url)
        print(f"  Using system proxy: {proxy_url}")


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------

def _get_ssl_context():
    """Create an SSL context that honours system / env configuration."""
    ctx = ssl.create_default_context()
    # Honour custom CA bundles commonly used in corporate environments
    ca_file = (
        os.environ.get("SSL_CERT_FILE")
        or os.environ.get("REQUESTS_CA_BUNDLE")
        or os.environ.get("CURL_CA_BUNDLE")
    )
    if ca_file and os.path.isfile(ca_file):
        ctx.load_verify_locations(ca_file)
    return ctx


def _download_file(url, dest_path, description="file"):
    """Download *url* to *dest_path* with retry, timeout, and progress.

    Returns True on success, False on failure.  Prints progress to stdout.
    """
    ssl_ctx = _get_ssl_context()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "HwCodecDetect/1.0"})
            with urllib.request.urlopen(req, timeout=DOWNLOAD_TIMEOUT, context=ssl_ctx) as resp:
                total = resp.headers.get("Content-Length")
                total = int(total) if total else None

                downloaded = 0
                last_pct_printed = -1
                last_size_printed = -1
                with open(dest_path, "wb") as f:
                    while True:
                        chunk = resp.read(65536)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total:
                            pct = int(downloaded * 100 / total)
                            if pct != last_pct_printed and pct % 10 == 0:
                                last_pct_printed = pct
                                print(f"\r  Downloading {description}: {pct}%  ", end="", flush=True)
                        else:
                            # Content-Length unknown: print progress every 1 MB
                            mb = downloaded // (1024 * 1024)
                            if mb != last_size_printed and mb > last_size_printed:
                                last_size_printed = mb
                                print(f"\r  Downloading {description}: {mb} MB  ", end="", flush=True)
                if total:
                    print(f"\r  Downloading {description}: 100%  ")
                else:
                    print(f"\r  Downloading {description}: {downloaded // (1024 * 1024)} MB done  ")
                return True

        except (urllib.error.URLError, urllib.error.HTTPError, OSError, ssl.SSLError) as e:
            wait = RETRY_BACKOFF * attempt
            code = getattr(e, "code", None)
            if code in (404, 403):
                # Don't retry client errors
                print(f"\n  Download failed (HTTP {code}): {url}", file=sys.stderr)
                return False
            if attempt < MAX_RETRIES:
                print(f"\n  Download attempt {attempt} failed: {e}. Retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"\n  Download failed after {MAX_RETRIES} attempts: {e}", file=sys.stderr)
                return False

    return False


# ---------------------------------------------------------------------------
# Post-install verification
# ---------------------------------------------------------------------------

def verify_ffmpeg(ffmpeg_path=None):
    """Run ``ffmpeg -version`` to verify the binary works.

    If *ffmpeg_path* is given, use that; otherwise rely on PATH lookup.
    Returns True if verification succeeds.
    """
    cmd = [ffmpeg_path or "ffmpeg", "-version"]
    result = _run_cmd(cmd, timeout=15)
    return result is not None and result.returncode == 0


def _try_find_ffmpeg_in_common_locations():
    """On some platforms, a freshly installed ffmpeg may not be in the *current*
    PATH but exists in well-known directories.  Return the directory path if
    found, else ``None``.
    """
    system = platform.system()
    candidates = []

    if system == "Windows":
        # Winget installs to %LOCALAPPDATA%\Microsoft\WinGet\Packages or ProgramFiles
        local = os.environ.get("LOCALAPPDATA", "")
        if local:
            # Search WinGet Packages directory
            winget_pkg = os.path.join(local, "Microsoft", "WinGet", "Packages")
            if os.path.isdir(winget_pkg):
                for entry in os.listdir(winget_pkg):
                    if "ffmpeg" in entry.lower():
                        pkg_dir = os.path.join(winget_pkg, entry)
                        # Dynamically search for a bin/ containing ffmpeg.exe
                        for root, dirs, files in os.walk(pkg_dir):
                            if "ffmpeg.exe" in files:
                                candidates.append(root)
                                break
                        # Also try a direct bin/ subfolder
                        bin_dir2 = os.path.join(pkg_dir, "bin")
                        if os.path.isdir(bin_dir2) and bin_dir2 not in candidates:
                            candidates.append(bin_dir2)
        # Chocolatey
        choco = os.environ.get("ProgramData", "")
        if choco:
            choco_bin = os.path.join(choco, "chocolatey", "bin")
            if os.path.isdir(choco_bin):
                candidates.append(choco_bin)
        # Scoop
        scoop_dir = os.path.expanduser("~/scoop/apps/ffmpeg/current")
        if os.path.isdir(scoop_dir):
            candidates.append(scoop_dir)
        # Common manual install locations
        for base in ("C:\\ffmpeg\\bin", "C:\\Program Files\\ffmpeg\\bin", os.path.expanduser("~/ffmpeg/bin")):
            if os.path.isdir(base):
                candidates.append(base)

    elif system == "Darwin":
        # Homebrew
        for prefix in ("/opt/homebrew/bin", "/usr/local/bin"):  # Apple Silicon / Intel
            if os.path.isfile(os.path.join(prefix, "ffmpeg")):
                candidates.append(os.path.dirname(os.path.join(prefix, "ffmpeg")))
        # MacPorts
        if os.path.isdir("/opt/local/bin"):
            candidates.append("/opt/local/bin")
        # Conda
        conda_prefix = os.environ.get("CONDA_PREFIX")
        if conda_prefix:
            candidates.append(os.path.join(conda_prefix, "bin"))

    elif system == "Linux":
        for p in ("/usr/local/bin", "/usr/bin", "/snap/bin", "/opt/ffmpeg/bin",
                   os.path.expanduser("~/.local/bin"),
                   os.path.expanduser("~/bin")):
            if os.path.isfile(os.path.join(p, "ffmpeg")):
                candidates.append(p)
        # Conda / Nix
        conda_prefix = os.environ.get("CONDA_PREFIX")
        if conda_prefix:
            candidates.append(os.path.join(conda_prefix, "bin"))
        nix_profile = os.path.expanduser("~/.nix-profile/bin")
        if os.path.isdir(nix_profile):
            candidates.append(nix_profile)

    elif system in ("FreeBSD", "OpenBSD", "NetBSD"):
        for p in ("/usr/local/bin", "/usr/bin"):
            if os.path.isfile(os.path.join(p, "ffmpeg")):
                candidates.append(p)

    for d in candidates:
        ffmpeg_full = os.path.join(d, "ffmpeg")
        if os.path.isfile(ffmpeg_full):
            return d
    return None


def _prepend_to_path(dir_path):
    """Prepend *dir_path* to ``PATH`` in both the current process and the
    subprocess environment so that child processes can find ffmpeg.
    """
    os.environ["PATH"] = dir_path + os.pathsep + os.environ.get("PATH", "")


# ---------------------------------------------------------------------------
# Manual install suggestions
# ---------------------------------------------------------------------------

def _suggest_manual_install():
    """Print clear manual-install instructions and return False."""
    system = platform.system()
    arch = get_architecture()
    print("\n" + "=" * 60, file=sys.stderr)
    print("Automatic FFmpeg installation failed.", file=sys.stderr)
    print("Please install FFmpeg manually:", file=sys.stderr)

    if system == "Windows":
        print(f"""
  Method 1 – winget:
    winget install --id Gyan.FFmpeg -e

  Method 2 – choco:
    choco install ffmpeg

  Method 3 – scoop:
    scoop install ffmpeg

  Method 4 – Download manually:
    Architecture: {arch}
    https://github.com/BtbN/FFmpeg-Builds/releases
    Download the file matching: ffmpeg-master-latest-win{ '64' if arch == 'x86_64' else 'arm64' }-gpl-shared.zip
    Extract and add the 'bin' folder to your system PATH.
""", file=sys.stderr)
    elif system == "Darwin":
        print(f"""
  Method 1 – Homebrew (recommended):
    brew install ffmpeg

  Method 2 – MacPorts:
    sudo port install ffmpeg

  Method 3 – Download manually:
    https://evermeet.cx/ffmpeg/
    https://ffmpeg.org/download.html
""", file=sys.stderr)
    elif system == "Linux":
        print(f"""
  Debian/Ubuntu:     sudo apt update && sudo apt install ffmpeg
  Fedora/RHEL 8+:   sudo dnf install ffmpeg
  CentOS 7:         sudo yum install epel-release && sudo yum install ffmpeg
  Arch Linux:       sudo pacman -S ffmpeg
  openSUSE:         sudo zypper install ffmpeg
  Alpine:           apk add ffmpeg
  Void Linux:       sudo xbps-install -S ffmpeg
  Static binary:    https://johnvansickle.com/ffmpeg/
""", file=sys.stderr)
    elif system in ("FreeBSD", "OpenBSD", "NetBSD"):
        print(f"""
  FreeBSD:          sudo pkg install ffmpeg
  OpenBSD:          sudo pkg_add ffmpeg
  FreeBSD ports:    cd /usr/ports/multimedia/ffmpeg && sudo make install clean
  NetBSD:           sudo pkgin install ffmpeg
""", file=sys.stderr)
    else:
        print(f"""
  Please see: https://ffmpeg.org/download.html
  Architecture: {arch}
""", file=sys.stderr)

    print("=" * 60, file=sys.stderr)
    return False


# ===================================================================
# Windows installation
# ===================================================================

def _windows_download_fallback():
    """Download a pre-built FFmpeg binary as a last resort on Windows."""
    arch = get_architecture()
    bits = _get_python_arch_bits()

    # Candidate URLs ordered by preference.
    urls = []
    if arch == "x86_64":
        urls = [
            "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip",
            "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
            "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
        ]
    elif arch == "aarch64":
        urls = [
            "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-winarm64-gpl-shared.zip",
            "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
        ]
    elif bits == 32:
        urls = [
            "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win32-gpl-shared.zip",
            "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
        ]

    if not urls:
        print(f"  No pre-built FFmpeg available for Windows {arch}/{bits}bit.", file=sys.stderr)
        return False

    # Determine a writable install directory
    install_dir = None
    # Try a location next to the current script / package
    if not _is_frozen():
        install_dir = os.path.join(os.path.expanduser("~"), ".hwcodecdetect", "ffmpeg")
    else:
        local = os.environ.get("LOCALAPPDATA")
        if local:
            install_dir = os.path.join(local, "HwCodecDetect", "ffmpeg")
    if not install_dir:
        install_dir = os.path.join(tempfile.gettempdir(), "HwCodecDetect_ffmpeg")

    for url in urls:
        print(f"  Trying download: {url}")
        with tempfile.TemporaryDirectory() as tmp:
            zip_path = os.path.join(tmp, "ffmpeg.zip")
            if not _download_file(url, zip_path, description="FFmpeg"):
                continue

            # Extract
            try:
                print("  Extracting...")
                with zipfile.ZipFile(zip_path, "r") as zf:
                    # Find the bin directory inside the zip
                    bin_entries = [n for n in zf.namelist() if "/bin/ffmpeg.exe" in n or "\\bin\\ffmpeg.exe" in n]
                    if bin_entries:
                        # Extract entire bin folder content
                        for entry in bin_entries:
                            # Find the bin directory prefix
                            idx = entry.lower().find("/bin/")
                            if idx == -1:
                                idx = entry.lower().find("\\bin\\")
                            bin_prefix = entry[:idx + 5]  # include "bin/" or "bin\\"
                            break
                    else:
                        # Fallback: extract all
                        zf.extractall(tmp)
                        # Search for ffmpeg.exe
                        for root, dirs, files in os.walk(tmp):
                            if "ffmpeg.exe" in files:
                                bin_prefix = root + os.sep
                                break
                        else:
                            print("  Could not locate ffmpeg.exe in archive.", file=sys.stderr)
                            continue

                    # Create install directory
                    os.makedirs(install_dir, exist_ok=True)

                    # Extract bin contents
                    for entry in zf.namelist():
                        if entry.startswith(bin_prefix) and not entry.endswith("/"):
                            data = zf.read(entry)
                            fname = os.path.basename(entry)
                            if fname:
                                target = os.path.join(install_dir, fname)
                                with open(target, "wb") as f:
                                    f.write(data)

            except (zipfile.BadZipFile, OSError) as e:
                print(f"  Extraction failed: {e}", file=sys.stderr)
                continue

            # Verify
            ffmpeg_exe = os.path.join(install_dir, "ffmpeg.exe")
            if os.path.isfile(ffmpeg_exe) and verify_ffmpeg(ffmpeg_exe):
                _prepend_to_path(install_dir)
                # Also try to persist the PATH change for the user
                _try_add_to_user_path_windows(install_dir)
                print(f"  FFmpeg installed to: {install_dir}")
                return True
            else:
                print("  Downloaded file verification failed.", file=sys.stderr)

    return False


def _try_add_to_user_path_windows(dir_path):
    """Attempt to add *dir_path* to the user's PATH via the registry.

    This is a best-effort operation; failures are silently ignored.
    """
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_ALL_ACCESS)
        try:
            current_path, reg_type = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current_path, reg_type = "", winreg.REG_EXPAND_SZ
        if dir_path.lower() not in current_path.lower():
            new_path = dir_path + ";" + current_path if current_path else dir_path
            winreg.SetValueEx(key, "Path", 0, reg_type, new_path)
            # Notify the system about the change (broadcast WM_SETTINGCHANGE)
            try:
                import ctypes
                HWND_BROADCAST = 0xFFFF
                WM_SETTINGCHANGE = 0x001A
                SMTO_ABORTIFHUNG = 0x0002
                ctypes.windll.user32.SendMessageTimeoutW(
                    HWND_BROADCAST, WM_SETTINGCHANGE, 0,
                    "Environment", SMTO_ABORTIFHUNG, 5000, None
                )
            except Exception:
                pass
            print(f"  Added {dir_path} to user PATH (will take effect in new terminals).")
        winreg.CloseKey(key)
    except Exception:
        pass  # Best-effort


def install_on_windows():
    """Install FFmpeg on Windows using a cascade of methods."""
    print("FFmpeg not found. Attempting to install for Windows...")

    # Method 1: Winget
    if shutil.which("winget"):
        print("  [1/4] Trying Winget...")
        result = _run_cmd(
            ["winget", "install", "--id", "Gyan.FFmpeg", "-e",
             "--accept-package-agreements", "--accept-source-agreements"],
            timeout=300,
        )
        if result and result.returncode == 0:
            # Winget may install to a location not yet in PATH
            extra = _try_find_ffmpeg_in_common_locations()
            if extra:
                _prepend_to_path(extra)
            if shutil.which("ffmpeg") or (extra and verify_ffmpeg(os.path.join(extra, "ffmpeg.exe"))):
                print("  FFmpeg installed via Winget.")
                return 0
        print("  Winget installation failed or verification failed.", file=sys.stderr)

    # Method 2: Chocolatey
    if shutil.which("choco"):
        print("  [2/4] Trying Chocolatey...")
        result = _run_cmd(["choco", "install", "ffmpeg", "-y"], timeout=300)
        if result and result.returncode == 0:
            extra = _try_find_ffmpeg_in_common_locations()
            if extra:
                _prepend_to_path(extra)
            if shutil.which("ffmpeg"):
                print("  FFmpeg installed via Chocolatey.")
                return 0
        print("  Chocolatey installation failed.", file=sys.stderr)

    # Method 3: Scoop
    if shutil.which("scoop"):
        print("  [3/4] Trying Scoop...")
        result = _run_cmd(["scoop", "install", "ffmpeg"], timeout=300)
        if result and result.returncode == 0:
            extra = _try_find_ffmpeg_in_common_locations()
            if extra:
                _prepend_to_path(extra)
            if shutil.which("ffmpeg"):
                print("  FFmpeg installed via Scoop.")
                return 0
        print("  Scoop installation failed.", file=sys.stderr)

    # Method 4: Manual download
    print("  [4/4] Downloading pre-built FFmpeg binary...")
    if _windows_download_fallback():
        print("  FFmpeg installed via manual download.")
        return 0

    return -1 if not _suggest_manual_install() else -1


# ===================================================================
# Linux installation
# ===================================================================

def install_on_linux():
    """Install FFmpeg on Linux using the appropriate package manager, with
    a static-binary download as the ultimate fallback."""
    print("FFmpeg not found. Attempting to install for Linux...")

    distro = get_linux_distro()
    sudo = _sudo_prefix()
    is_docker = _is_docker_or_ci()

    # If running in Docker as non-root, try without sudo first (likely won't
    # need it in most Docker images).
    if is_docker and not _is_root():
        sudo = []  # Most Docker images either run as root or have the pkg mgr

    # ---- Package manager cascade ----
    pm_tried = []

    # Debian / Ubuntu / Linux Mint / Pop!_OS / etc.
    if _distro_matches(distro, "debian", "ubuntu", "linuxmint", "pop", "kali", "raspbian", "deepin", "uos"):
        pm_name = "apt-get"
        cmd = sudo + ["apt-get", "install", "-y", "ffmpeg"]
        if not shutil.which("apt-get"):
            cmd = None
        else:
            pm_tried.append(pm_name)
            print(f"  Trying {pm_name}...")
            # First try update (best-effort)
            _run_cmd(sudo + ["apt-get", "update", "-qq"], timeout=60)
            result = _run_cmd(cmd, timeout=180)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print(f"  FFmpeg installed via {pm_name}.")
                return 0
            print(f"  {pm_name} installation failed.", file=sys.stderr)

    # Fedora / RHEL 8+ / CentOS 8+ / Rocky / Alma / Amazon Linux 2+
    elif _distro_matches(distro, "fedora", "rhel", "centos", "rocky", "almalinux", "amzn", "ol"):
        # Determine dnf vs yum
        if shutil.which("dnf"):
            pm_name = "dnf"
            cmd = sudo + ["dnf", "install", "-y", "ffmpeg"]
        elif shutil.which("yum"):
            pm_name = "yum"
            cmd = sudo + ["yum", "install", "-y", "ffmpeg"]
        else:
            cmd = None

        if cmd:
            pm_tried.append(pm_name)
            print(f"  Trying {pm_name}...")
            result = _run_cmd(cmd, timeout=180)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print(f"  FFmpeg installed via {pm_name}.")
                return 0
            # Fedora/RHEL often need RPM Fusion for ffmpeg
            if pm_name == "dnf":
                print("  Trying to enable RPM Fusion repository...")
                rpmfusion_cmd = None
                if _distro_matches(distro, "fedora"):
                    rpmfusion_cmd = sudo + [
                        "dnf", "install", "-y",
                        "https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm",
                    ]
                else:
                    rpmfusion_cmd = sudo + [
                        "dnf", "install", "-y",
                        "https://download1.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %rhel).noarch.rpm",
                    ]
                # Resolve shell variables via rpm -E
                if rpmfusion_cmd:
                    rpm_macro = "%fedora" if _distro_matches(distro, "fedora") else "%rhel"
                    rpm_result = _run_cmd(["rpm", "-E", rpm_macro], timeout=10)
                    if rpm_result and rpm_result.stdout.strip():
                        rpm_version = rpm_result.stdout.strip()
                        rpmfusion_cmd = [c.replace("$(rpm -E %fedora)", rpm_version)
                                          .replace("$(rpm -E %rhel)", rpm_version)
                                          for c in rpmfusion_cmd]
                if rpmfusion_cmd:
                    _run_cmd(rpmfusion_cmd, timeout=120)
                    result = _run_cmd(cmd, timeout=180)
                    if result and result.returncode == 0 and shutil.which("ffmpeg"):
                        print(f"  FFmpeg installed via {pm_name} (with RPM Fusion).")
                        return 0
            print(f"  {pm_name} installation failed.", file=sys.stderr)

    # Arch / Manjaro / EndeavourOS
    elif _distro_matches(distro, "arch", "manjaro", "endeavouros", "garuda", "arcolinux"):
        if shutil.which("pacman"):
            pm_name = "pacman"
            cmd = sudo + ["pacman", "-S", "--noconfirm", "ffmpeg"]
            pm_tried.append(pm_name)
            print(f"  Trying {pm_name}...")
            result = _run_cmd(cmd, timeout=180)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print(f"  FFmpeg installed via {pm_name}.")
                return 0
            print(f"  {pm_name} installation failed.", file=sys.stderr)

    # openSUSE / SLES
    elif _distro_matches(distro, "opensuse", "sles", "suse"):
        if shutil.which("zypper"):
            pm_name = "zypper"
            cmd = sudo + ["zypper", "--non-interactive", "install", "ffmpeg"]
            pm_tried.append(pm_name)
            print(f"  Trying {pm_name}...")
            result = _run_cmd(cmd, timeout=180)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print(f"  FFmpeg installed via {pm_name}.")
                return 0
            print(f"  {pm_name} installation failed.", file=sys.stderr)

    # Alpine
    elif _distro_matches(distro, "alpine"):
        if shutil.which("apk"):
            pm_name = "apk"
            cmd = sudo + ["apk", "add", "ffmpeg"]
            pm_tried.append(pm_name)
            print(f"  Trying {pm_name}...")
            result = _run_cmd(cmd, timeout=180)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print(f"  FFmpeg installed via {pm_name}.")
                return 0
            print(f"  {pm_name} installation failed.", file=sys.stderr)

    # Void Linux
    elif _distro_matches(distro, "void"):
        if shutil.which("xbps-install"):
            pm_name = "xbps-install"
            cmd = sudo + ["xbps-install", "-Sy", "ffmpeg"]
            pm_tried.append(pm_name)
            print(f"  Trying {pm_name}...")
            result = _run_cmd(cmd, timeout=180)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print(f"  FFmpeg installed via {pm_name}.")
                return 0
            print(f"  {pm_name} installation failed.", file=sys.stderr)

    # Gentoo
    elif _distro_matches(distro, "gentoo"):
        if shutil.which("emerge"):
            pm_name = "emerge"
            # -v verbose, --ask=n skip interactive prompt (non-interactive safe)
            cmd = sudo + ["emerge", "-v", "--ask=n", "media-video/ffmpeg"]
            pm_tried.append(pm_name)
            print(f"  Trying {pm_name} (this may take a while)...")
            result = _run_cmd(cmd, timeout=3600)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print(f"  FFmpeg installed via {pm_name}.")
                return 0
            print(f"  {pm_name} installation failed.", file=sys.stderr)

    # NixOS
    elif _distro_matches(distro, "nixos", "nix"):
        # Try `nix profile` first (newer Nix), then fall back to `nix-env`
        if shutil.which("nix"):
            pm_name = "nix profile"
            cmd = ["nix", "profile", "install", "nixpkgs#ffmpeg"]
            pm_tried.append(pm_name)
            print(f"  Trying {pm_name}...")
            result = _run_cmd(cmd, timeout=300)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print(f"  FFmpeg installed via {pm_name}.")
                return 0
            print(f"  {pm_name} installation failed.", file=sys.stderr)
        if shutil.which("nix-env"):
            pm_name = "nix-env"
            cmd = ["nix-env", "-iA", "nixpkgs.ffmpeg"]
            pm_tried.append(pm_name)
            print(f"  Trying {pm_name}...")
            result = _run_cmd(cmd, timeout=300)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print(f"  FFmpeg installed via {pm_name}.")
                return 0
            print(f"  {pm_name} installation failed.", file=sys.stderr)

    # ---- Generic: try common package managers if nothing matched above ----
    if not pm_tried:
        for pm_name, cmd_list in [
            ("apt-get", sudo + ["apt-get", "install", "-y", "ffmpeg"]),
            ("dnf", sudo + ["dnf", "install", "-y", "ffmpeg"]),
            ("yum", sudo + ["yum", "install", "-y", "ffmpeg"]),
            ("pacman", sudo + ["pacman", "-S", "--noconfirm", "ffmpeg"]),
            ("zypper", sudo + ["zypper", "--non-interactive", "install", "ffmpeg"]),
            ("apk", sudo + ["apk", "add", "ffmpeg"]),
        ]:
            if shutil.which(pm_name.split("-")[0]):
                print(f"  Trying {pm_name} (generic fallback)...")
                result = _run_cmd(cmd_list, timeout=180)
                if result and result.returncode == 0 and shutil.which("ffmpeg"):
                    print(f"  FFmpeg installed via {pm_name}.")
                    return 0
                print(f"  {pm_name} failed.", file=sys.stderr)

    # ---- Snap / Flatpak (universal Linux packages) ----
    if shutil.which("snap"):
        print("  Trying snap...")
        result = _run_cmd(sudo + ["snap", "install", "ffmpeg"], timeout=300)
        if result and result.returncode == 0:
            # snap installs to /snap/bin which may not be in PATH
            snap_bin = "/snap/bin"
            if os.path.isfile(os.path.join(snap_bin, "ffmpeg")):
                _prepend_to_path(snap_bin)
            if shutil.which("ffmpeg"):
                print("  FFmpeg installed via snap.")
                return 0
        print("  snap installation failed.", file=sys.stderr)

    if shutil.which("flatpak"):
        print("  Trying flatpak...")
        result = _run_cmd(
            ["flatpak", "install", "-y", "flathub", "org.freedesktop.Platform.ffmpeg-full//23.08"],
            timeout=300,
        )
        if result and result.returncode == 0:
            print("  FFmpeg flatpak runtime installed (may require app integration).")
            return 0
        print("  flatpak installation failed.", file=sys.stderr)

    # ---- Fallback: download static build ----
    print("  Package manager installation failed. Trying static binary download...")
    if _linux_download_static_fallback():
        return 0

    return -1 if not _suggest_manual_install() else -1


def _linux_download_static_fallback():
    """Download John Van Sickle's static FFmpeg build (x86_64 / ARM64 / ARMv7)."""
    arch = get_architecture()
    urls = {
        "x86_64": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz",
        "aarch64": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz",
        "armv7": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-armhf-static.tar.xz",
    }
    url = urls.get(arch)
    if not url:
        print(f"  No static FFmpeg build available for {arch}.", file=sys.stderr)
        return False

    install_dir = os.path.expanduser("~/.local/bin")
    os.makedirs(install_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tar_path = os.path.join(tmp, "ffmpeg.tar.xz")
        print(f"  Downloading static FFmpeg ({arch})...")
        if not _download_file(url, tar_path, description=f"FFmpeg static ({arch})"):
            return False

        # Extract – prefer tar, fall back to python tarfile
        print("  Extracting...")
        result = _run_cmd(["tar", "-xJf", tar_path, "-C", tmp], timeout=60)
        if result is None or result.returncode != 0:
            # Try python tarfile
            try:
                import tarfile
                with tarfile.open(tar_path, "r:xz") as tf:
                    tf.extractall(tmp)
            except Exception as e:
                print(f"  Extraction failed: {e}", file=sys.stderr)
                return False

        # Find the ffmpeg (and ffprobe) binaries in the extracted content
        for root, _dirs, files in os.walk(tmp):
            if "ffmpeg" in files:
                for binary in ("ffmpeg", "ffprobe"):
                    if binary in files:
                        src = os.path.join(root, binary)
                        dst = os.path.join(install_dir, binary)
                        shutil.copy2(src, dst)
                        os.chmod(dst, 0o755)
                _prepend_to_path(install_dir)
                print(f"  FFmpeg installed to {os.path.join(install_dir, 'ffmpeg')}")
                return True

    print("  Could not locate ffmpeg binary in downloaded archive.", file=sys.stderr)
    return False


# ===================================================================
# macOS installation
# ===================================================================

def install_on_macos():
    """Install FFmpeg on macOS via Homebrew, MacPorts, conda, or manual download."""
    print("FFmpeg not found. Attempting to install for macOS...")

    sudo = _sudo_prefix()
    method = 0
    total = 6

    # Method 1: Homebrew
    if shutil.which("brew"):
        method += 1
        print(f"  [{method}/{total}] Trying Homebrew...")
        result = _run_cmd(["brew", "install", "ffmpeg"], timeout=600)
        if result and result.returncode == 0 and shutil.which("ffmpeg"):
            print("  FFmpeg installed via Homebrew.")
            return 0
        print("  Homebrew installation failed.", file=sys.stderr)

    # Method 2: MacPorts
    if shutil.which("port"):
        method += 1
        print(f"  [{method}/{total}] Trying MacPorts...")
        result = _run_cmd(sudo + ["port", "install", "ffmpeg"], timeout=600)
        if result and result.returncode == 0 and shutil.which("ffmpeg"):
            print("  FFmpeg installed via MacPorts.")
            return 0
        print("  MacPorts installation failed.", file=sys.stderr)

    # Method 3: Conda
    if shutil.which("conda"):
        method += 1
        print(f"  [{method}/{total}] Trying Conda...")
        result = _run_cmd(["conda", "install", "-c", "conda-forge", "ffmpeg", "-y"], timeout=600)
        if result and result.returncode == 0 and shutil.which("ffmpeg"):
            print("  FFmpeg installed via Conda.")
            return 0
        print("  Conda installation failed.", file=sys.stderr)

    # Method 4: Nix
    if shutil.which("nix") or shutil.which("nix-env"):
        method += 1
        print(f"  [{method}/{total}] Trying Nix...")
        if shutil.which("nix"):
            result = _run_cmd(["nix", "profile", "install", "nixpkgs#ffmpeg"], timeout=300)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print("  FFmpeg installed via Nix (nix profile).")
                return 0
        if shutil.which("nix-env"):
            result = _run_cmd(["nix-env", "-iA", "nixpkgs.ffmpeg"], timeout=300)
            if result and result.returncode == 0 and shutil.which("ffmpeg"):
                print("  FFmpeg installed via Nix (nix-env).")
                return 0
        print("  Nix installation failed.", file=sys.stderr)

    # Method 5: Install Homebrew automatically (before manual download)
    if not shutil.which("brew"):
        method += 1
        print(f"  [{method}/{total}] Attempting to install Homebrew first...")
        result = _run_cmd(
            ['/bin/bash', '-c',
             '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)'],
            timeout=300,
        )
        if result and result.returncode == 0:
            # Try brew again
            brew_path = "/opt/homebrew/bin/brew" if platform.machine() == "arm64" else "/usr/local/bin/brew"
            if os.path.isfile(brew_path):
                _prepend_to_path(os.path.dirname(brew_path))
            if shutil.which("brew"):
                result = _run_cmd(["brew", "install", "ffmpeg"], timeout=600)
                if result and result.returncode == 0 and shutil.which("ffmpeg"):
                    print("  FFmpeg installed via Homebrew (auto-installed).")
                    return 0
        print("  Homebrew auto-installation failed.", file=sys.stderr)

    # Method 6: Manual download
    method += 1
    print(f"  [{method}/{total}] Downloading pre-built FFmpeg binary...")
    if _macos_download_fallback():
        print("  FFmpeg installed via manual download.")
        return 0

    return -1 if not _suggest_manual_install() else -1


def _macos_download_fallback():
    """Download a pre-built FFmpeg for macOS from evermeet.cx."""
    arch = get_architecture()
    urls = []
    if arch == "aarch64":
        urls = [
            "https://evermeet.cx/ffmpeg/getrelease/ffmpeg/arm",
            "https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip",
        ]
    else:
        urls = [
            "https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip",
        ]

    install_dir = os.path.expanduser("~/.local/bin")
    os.makedirs(install_dir, exist_ok=True)

    for url in urls:
        print(f"  Downloading from {url}...")
        zip_path = os.path.join(tempfile.gettempdir(), "ffmpeg_mac.zip")
        if not _download_file(url, zip_path, description="FFmpeg for macOS"):
            continue

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(install_dir)
            ffmpeg_bin = os.path.join(install_dir, "ffmpeg")
            if os.path.isfile(ffmpeg_bin):
                os.chmod(ffmpeg_bin, 0o755)
                _prepend_to_path(install_dir)
                print(f"  FFmpeg installed to {ffmpeg_bin}")
                return True
        except (zipfile.BadZipFile, OSError) as e:
            print(f"  Extraction failed: {e}", file=sys.stderr)
            continue

    return False


# ===================================================================
# BSD installation
# ===================================================================

def install_on_bsd():
    """Install FFmpeg on FreeBSD / OpenBSD / NetBSD via pkg or ports."""
    print("FFmpeg not found. Attempting to install for BSD...")

    # Method 1: pkg (FreeBSD / NetBSD)
    if shutil.which("pkg"):
        print("  Trying pkg...")
        result = _run_cmd(["pkg", "install", "-y", "ffmpeg"], timeout=300)
        if result and result.returncode == 0 and shutil.which("ffmpeg"):
            print("  FFmpeg installed via pkg.")
            return 0
        print("  pkg installation failed.", file=sys.stderr)

    # Method 2: pkg_add (OpenBSD)
    if shutil.which("pkg_add"):
        print("  Trying pkg_add...")
        result = _run_cmd(["pkg_add", "ffmpeg"], timeout=300)
        if result and result.returncode == 0 and shutil.which("ffmpeg"):
            print("  FFmpeg installed via pkg_add.")
            return 0
        print("  pkg_add installation failed.", file=sys.stderr)

    # Method 3: ports (FreeBSD)
    ports_makefile = "/usr/ports/multimedia/ffmpeg"
    if os.path.isfile(os.path.join(ports_makefile, "Makefile")):
        print("  Trying FreeBSD ports...")
        result = _run_cmd(["make", "-C", ports_makefile, "install", "clean"], timeout=3600)
        if result and result.returncode == 0 and shutil.which("ffmpeg"):
            print("  FFmpeg installed via ports.")
            return 0
        print("  ports installation failed.", file=sys.stderr)

    return -1 if not _suggest_manual_install() else -1


# ===================================================================
# Main entry point
# ===================================================================

def install_ffmpeg_if_needed():
    """Check for FFmpeg and install it if not found.

    Returns 0 on success (ffmpeg is available), -1 on failure.
    """
    print("Checking for FFmpeg...")
    _ensure_system_proxy()

    # Step 1: Check if FFmpeg is already in PATH
    if shutil.which("ffmpeg"):
        if verify_ffmpeg():
            print("FFmpeg is already installed and working.")
            return 0
        else:
            print("FFmpeg found in PATH but failed verification.", file=sys.stderr)

    # Step 1.5: Check common locations that may not be in PATH
    extra_dir = _try_find_ffmpeg_in_common_locations()
    if extra_dir:
        _prepend_to_path(extra_dir)
        if shutil.which("ffmpeg") and verify_ffmpeg():
            print(f"FFmpeg found at {extra_dir} and added to PATH.")
            return 0

    # Step 2: Install based on OS
    os_name = platform.system()

    if os_name == "Windows":
        return install_on_windows()
    elif os_name == "Linux":
        return install_on_linux()
    elif os_name == "Darwin":
        return install_on_macos()
    elif os_name in ("FreeBSD", "OpenBSD", "NetBSD"):
        return install_on_bsd()
    else:
        print(f"Unsupported OS: {os_name}", file=sys.stderr)
        return -1


if __name__ == "__main__":
    sys.exit(install_ffmpeg_if_needed())