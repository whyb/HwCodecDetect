# HwCodecDetect/__init__.py
import os
from .install_ffmpeg_if_needed import install_ffmpeg_if_needed

def _read_version():
    try:
        version_path = os.path.join(os.path.dirname(__file__), '..', '..', 'VERSION')
        with open(version_path, encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return "0.0.0"

__version__ = _read_version()
__author__ = "whyb"
__email__ = "whyber@outlook.com"
__license__ = "BSD-3-Clause"
__url__ = "https://github.com/whyb/HwCodecDetect"