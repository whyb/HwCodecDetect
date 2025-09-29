import os
import sys
import platform
import subprocess
import shutil
import urllib.request
import zipfile
import tempfile

def install_ffmpeg_if_needed():
    """
    Checks for FFmpeg and installs it if not found.
    """
    print("Checking for FFmpeg...")

    # Step 1: Check if FFmpeg is already in PATH
    if shutil.which("ffmpeg"):
        print("FFmpeg is already installed and in PATH.")
        return 0

    # Step 2: Install based on OS
    os_name = platform.system()

    if os_name == "Windows":
        return install_on_windows()
    elif os_name == "Linux":
        return install_on_linux()
    elif os_name == "Darwin":  # 'Darwin' is the system name for macOS
        return install_on_macos()
    else:
        print(f"Unsupported OS: {os_name}", file=sys.stderr)
        return -1

def install_on_windows():
    """
    Tries to install FFmpeg on Windows using a cascade of package managers,
    falling back to a manual download if all else fails.
    """
    print("FFmpeg not found. Attempting to install for Windows...")

    # Method 1: Try Winget (Windows Package Manager)
    if shutil.which("winget"):
        print("Trying to install FFmpeg using Winget...")
        try:
            # Use the official ID for FFmpeg from Winget
            subprocess.run(["winget", "install", "--id", "Gyan.FFmpeg", "-e", "--accept-package-agreements", "--accept-source-agreements"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("FFmpeg installation complete via Winget.")
            return 0
        except subprocess.CalledProcessError:
            print("Winget installation failed. Trying next method.", file=sys.stderr)
            pass
    
    # Method 2: Try Chocolatey
    if shutil.which("choco"):
        print("Trying to install FFmpeg using Chocolatey...")
        try:
            subprocess.run(["choco", "install", "ffmpeg", "-y"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("FFmpeg installation complete via Chocolatey.")
            return 0
        except subprocess.CalledProcessError:
            print("Chocolatey installation failed. Trying next method.", file=sys.stderr)
            pass

    # Method 3: Try Scoop
    if shutil.which("scoop"):
        print("Trying to install FFmpeg using Scoop...")
        try:
            subprocess.run(["scoop", "install", "ffmpeg"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("FFmpeg installation complete via Scoop.")
            return 0
        except subprocess.CalledProcessError:
            print("Scoop installation failed. Trying next method.", file=sys.stderr)
            pass

    # Method 4: Manual Download (Fallback)
    print("All package manager installations failed. Falling back to manual download.")
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip"
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_file_path = os.path.join(temp_dir, "ffmpeg_temp.zip")
            
            urllib.request.urlretrieve(ffmpeg_url, zip_file_path)
            print("Download complete. Extracting...")
            
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            bin_source_path = os.path.join(temp_dir, "ffmpeg-master-latest-win64-gpl-shared", "bin")
            
            try:
                for item in os.listdir(bin_source_path):
                    shutil.move(os.path.join(bin_source_path, item), os.getcwd())
                print("FFmpeg files moved to the current directory.")
            except Exception as e:
                print(f"Error moving files to the current directory: {e}", file=sys.stderr)
                print("Adding FFmpeg's bin directory to PATH instead.")
                os.environ["PATH"] += os.pathsep + bin_source_path
                print(f"Added {bin_source_path} to PATH.")
            
            return 0

    except Exception as e:
        print(f"An unexpected error occurred during manual installation: {e}", file=sys.stderr)
        return -1

def install_on_linux():
    """
    Installs FFmpeg using package managers for various Linux distributions.
    """
    print("FFmpeg not found. Attempting to install via package manager...")
    
    distro = get_linux_distro()
    
    if "arch" in distro:
        command = ["sudo", "pacman", "-S", "--noconfirm", "ffmpeg"]
        package_manager_name = "pacman"
    elif "ubuntu" in distro or "debian" in distro:
        command = ["sudo", "apt-get", "install", "-y", "ffmpeg"]
        package_manager_name = "apt-get"
    elif "centos" in distro or "redhat" in distro or "fedora" in distro:
        command = ["sudo", "yum", "install", "-y", "ffmpeg"]
        package_manager_name = "yum"
    else:
        print("Unsupported Linux distribution. Please install FFmpeg manually.", file=sys.stderr)
        return -1
    
    try:
        print(f"Attempting to install FFmpeg using {package_manager_name}...")
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("FFmpeg installation complete.")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error installing FFmpeg with {package_manager_name}: {e}", file=sys.stderr)
        return -1
    except FileNotFoundError:
        print(f"Package manager '{package_manager_name}' not found. Please install FFmpeg manually.", file=sys.stderr)
        return -1

def install_on_macos():
    print("FFmpeg not found. Attempting to install for macOS...")

    # Try Homebrew
    if shutil.which("brew"):
        try:
            subprocess.run(["brew", "install", "ffmpeg"], check=True)
            print("FFmpeg installation complete via Homebrew.")
            return 0
        except subprocess.CalledProcessError:
            print("Homebrew installation failed. Trying next method.", file=sys.stderr)

    # Try MacPorts
    if shutil.which("port"):
        try:
            subprocess.run(["sudo", "port", "install", "ffmpeg"], check=True)
            print("FFmpeg installation complete via MacPorts.")
            return 0
        except subprocess.CalledProcessError:
            print("MacPorts installation failed. Trying next method.", file=sys.stderr)

    # Try Conda
    if shutil.which("conda"):
        try:
            subprocess.run(["conda", "install", "-c", "conda-forge", "ffmpeg", "-y"], check=True)
            print("FFmpeg installation complete via Conda.")
            return 0
        except subprocess.CalledProcessError:
            print("Conda installation failed. Trying next method.", file=sys.stderr)

    # Try Nix
    if shutil.which("nix-env"):
        try:
            subprocess.run(["nix-env", "-iA", "nixpkgs.ffmpeg"], check=True)
            print("FFmpeg installation complete via Nix.")
            return 0
        except subprocess.CalledProcessError:
            print("Nix installation failed. Trying next method.", file=sys.stderr)

    # Manual fallback
    print("All package manager installations failed. Please install FFmpeg manually from https://ffmpeg.org/download.html", file=sys.stderr)
    return -1


def get_linux_distro():
    """
    A simplified way to detect Linux distributions.
    """
    if os.path.exists('/etc/os-release'):
        with open('/etc/os-release') as f:
            content = f.read()
            if "ID=arch" in content:
                return "arch"
            elif "ID=ubuntu" in content:
                return "ubuntu"
            elif "ID=debian" in content:
                return "debian"
            elif "ID_LIKE=centos" in content or "ID=centos" in content:
                return "centos"
            elif "ID=fedora" in content:
                return "fedora"
    
    if os.path.exists('/etc/arch-release'):
        return "arch"
    if os.path.exists('/etc/debian_version'):
        return "debian"
    if os.path.exists('/etc/redhat-release'):
        return "redhat"
        
    return "unknown"

if __name__ == "__main__":
    exit_code = install_ffmpeg_if_needed()
    sys.exit(exit_code)