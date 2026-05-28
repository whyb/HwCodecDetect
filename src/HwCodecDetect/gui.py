"""
GUI Module for HwCodecDetect
Provides a graphical interface for hardware codec detection.
Fluent Design + macOS-inspired modern dark theme.
"""
import os
import sys
import shutil
import tempfile
import threading
import tkinter as tk
import tkinter.messagebox as messagebox
from collections import defaultdict
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import webbrowser
import subprocess
import time
from packaging import version
from .install_ffmpeg_if_needed import install_ffmpeg_if_needed
from .utils import get_local_version, check_codec_support, get_ffmpeg_supported_codecs
from .bitdepth_chroma_detect import (
    run_bitdepth_chroma_tests,
    PIXEL_FORMATS,
    BITDEPTH_CHROMA_RESOLUTION,
    ENCODER_TITLES as BD_ENCODER_TITLES,
    DECODER_TITLES as BD_DECODER_TITLES,
    ENCODERS as BD_ENCODERS,
    DECODERS as BD_DECODERS,
)

# Resolution definitions
RESOLUTIONS = {
    "240p": "426x240",
    "360p": "640x360",
    "480p": "854x480",
    "720p": "1280x720",
    "1080p": "1920x1080",
    "2K": "2560x1440",
    "4K": "3840x2160",
    "8K": "7680x4320",
}

# Decoder titles
DECODER_TITLES = {
    ("h264_cuvid", "h264"): "NVIDIA CUDA H264 Decoder(NVDEC)",
    ("h264_qsv", "h264"): "Intel Quick Sync Video H264 Decoder(QSV)",
    ("hevc_cuvid", "h265"): "NVIDIA CUDA H265 Decoder(NVDEC)",
    ("hevc_qsv", "h265"): "Intel Quick Sync Video H265 Decoder(QSV)",
    ("av1_cuvid", "av1"): "NVIDIA CUDA AV1 Decoder(NVDEC)",
    ("av1_qsv", "av1"): "Intel Quick Sync Video AV1 Decoder(QSV)",
    ("mjpeg_cuvid", "mjpeg"): "NVIDIA CUDA MJPEG Decoder(NVDEC)",
    ("mjpeg_qsv", "mjpeg"): "Intel Quick Sync Video MJPEG Decoder(QSV)",
    ("mpeg1_cuvid", "mpeg1"): "NVIDIA CUDA MPEG-1 Decoder(NVDEC)",
    ("mpeg2_cuvid", "mpeg2"): "NVIDIA CUDA MPEG-2 Decoder(NVDEC)",
    ("mpeg2_qsv", "mpeg2"): "Intel Quick Sync Video MPEG-2 Decoder(QSV)",
    ("mpeg4_cuvid", "mpeg4"): "NVIDIA CUDA MPEG-4 Decoder(NVDEC)",
    ("vp8_cuvid", "vp8"): "NVIDIA CUDA VP8 Decoder(NVDEC)",
    ("vp8_qsv", "vp8"): "Intel Quick Sync Video VP8 Decoder(QSV)",
    ("vp9_cuvid", "vp9"): "NVIDIA CUDA VP9 Decoder(NVDEC)",
    ("vp9_qsv", "vp9"): "Intel Quick Sync Video VP9 Decoder(QSV)",
    ("dxva2", "h264"): "Microsoft DirectX Video Acceleration H264 Decoder(DXVA2)",
    ("dxva2", "h265"): "Microsoft DirectX Video Acceleration H265 Decoder(DXVA2)",
    ("dxva2", "av1"): "Microsoft DirectX Video Acceleration AV1 Decoder(DXVA2)",
    ("dxva2", "mjpeg"): "Microsoft DirectX Video Acceleration MJPEG Decoder(DXVA2)",
    ("dxva2", "mpeg1"): "Microsoft DirectX Video Acceleration MPEG-1 Decoder(DXVA2)",
    ("dxva2", "mpeg2"): "Microsoft DirectX Video Acceleration MPEG-2 Decoder(DXVA2)",
    ("dxva2", "mpeg4"): "Microsoft DirectX Video Acceleration MPEG-4 Decoder(DXVA2)",
    ("dxva2", "vp8"): "Microsoft DirectX Video Acceleration VP8 Decoder(DXVA2)",
    ("dxva2", "vp9"): "Microsoft DirectX Video Acceleration VP9 Decoder(DXVA2)",
    ("d3d11va", "h264"): "Microsoft Direct3D 11 Video Acceleration H264 Decoder(D3D11VA)",
    ("d3d11va", "h265"): "Microsoft Direct3D 11 Video Acceleration H265 Decoder(D3D11VA)",
    ("d3d11va", "av1"): "Microsoft Direct3D 11 Video Acceleration AV1 Decoder(D3D11VA)",
    ("d3d11va", "mjpeg"): "Microsoft Direct3D 11 Video Acceleration MJPEG Decoder(D3D11VA)",
    ("d3d11va", "mpeg1"): "Microsoft Direct3D 11 Video Acceleration MPEG-1 Decoder(D3D11VA)",
    ("d3d11va", "mpeg2"): "Microsoft Direct3D 11 Video Acceleration MPEG-2 Decoder(D3D11VA)",
    ("d3d11va", "mpeg4"): "Microsoft Direct3D 11 Video Acceleration MPEG-4 Decoder(D3D11VA)",
    ("d3d11va", "vp8"): "Microsoft Direct3D 11 Video Acceleration VP8 Decoder(D3D11VA)",
    ("d3d11va", "vp9"): "Microsoft Direct3D 11 Video Acceleration VP9 Decoder(D3D11VA)",
    ("d3d12va", "h264"): "Microsoft Direct3D 12 Video Acceleration H264 Decoder(D3D12VA)",
    ("d3d12va", "h265"): "Microsoft Direct3D 12 Video Acceleration H265 Decoder(D3D12VA)",
    ("d3d12va", "av1"): "Microsoft Direct3D 12 Video Acceleration AV1 Decoder(D3D12VA)",
    ("d3d12va", "mjpeg"): "Microsoft Direct3D 12 Video Acceleration MJPEG Decoder(D3D12VA)",
    ("d3d12va", "mpeg1"): "Microsoft Direct3D 12 Video Acceleration MPEG-1 Decoder(D3D12VA)",
    ("d3d12va", "mpeg2"): "Microsoft Direct3D 12 Video Acceleration MPEG-2 Decoder(D3D12VA)",
    ("d3d12va", "mpeg4"): "Microsoft Direct3D 12 Video Acceleration MPEG-4 Decoder(D3D12VA)",
    ("d3d12va", "vp8"): "Microsoft Direct3D 12 Video Acceleration VP8 Decoder(D3D12VA)",
    ("d3d12va", "vp9"): "Microsoft Direct3D 12 Video Acceleration VP9 Decoder(D3D12VA)",
    ("vulkan", "h264"): "Vulkan Hardware H264 Decoder(Vulkan)",
    ("vulkan", "h265"): "Vulkan Hardware H265 Decoder(Vulkan)",
    ("vulkan", "av1"): "Vulkan Hardware AV1 Decoder(Vulkan)",
    ("videotoolbox", "h264"): "Apple macOS Hardware H264 Decoder(VideoToolbox)",
    ("videotoolbox", "h265"): "Apple macOS Hardware H265 Decoder(VideoToolbox)",
    ("videotoolbox", "mpeg2"): "Apple macOS Hardware MPEG-2 Decoder(VideoToolbox)",
    ("videotoolbox", "mpeg4"): "Apple macOS Hardware MPEG-4 Decoder(VideoToolbox)",
    ("videotoolbox", "prores"): "Apple macOS Hardware ProRes Decoder(VideoToolbox)",
    ("videotoolbox", "vp9"): "Apple macOS Hardware VP9 Decoder(VideoToolbox)",
}

DECODERS = {
    "h264": {"lib": "libx264", "hw_decoders": ["h264_cuvid", "h264_qsv", "dxva2", "d3d11va", "vulkan", "d3d12va", "videotoolbox"]},
    "h265": {"lib": "libx265", "hw_decoders": ["hevc_cuvid", "hevc_qsv", "d3d11va", "d3d12va", "vulkan", "videotoolbox"]},
    "av1": {"lib": "librav1e", "hw_decoders": ["av1_cuvid", "av1_qsv", "dxva2", "d3d11va", "d3d12va", "vulkan"]},
    "mjpeg": {"lib": "mjpeg", "hw_decoders": ["mjpeg_cuvid", "mjpeg_qsv", "dxva2", "d3d11va", "d3d12va"]},
    "mpeg1": {"lib": "mpeg1video", "hw_decoders": ["mpeg1_cuvid", "dxva2", "d3d11va", "d3d12va"]},
    "mpeg2": {"lib": "mpeg2video", "hw_decoders": ["mpeg2_cuvid", "mpeg2_qsv", "dxva2", "d3d11va", "d3d12va", "videotoolbox"]},
    "mpeg4": {"lib": "mpeg4", "hw_decoders": ["mpeg4_cuvid", "dxva2", "d3d11va", "d3d12va", "videotoolbox"]},
    "vp8": {"lib": "libvpx", "hw_decoders": ["vp8_cuvid", "vp8_qsv", "dxva2", "d3d11va", "d3d12va"]},
    "vp9": {"lib": "libvpx-vp9", "hw_decoders": ["vp9_cuvid", "vp9_qsv", "dxva2", "d3d11va", "d3d12va", "videotoolbox"]},
    "prores": {"lib": "prores", "hw_decoders": ["videotoolbox"]},
}

# Encoder titles
ENCODER_TITLES = {
    ("h264_nvenc", "h264"): "NVIDIA Hardware H264 Encoder(NVEnc)",
    ("hevc_nvenc", "h265"): "NVIDIA Hardware H265 Encoder(NVEnc)",
    ("av1_nvenc", "av1"): "NVIDIA Hardware AV1 Encoder(NVEnc)",
    ("h264_qsv", "h264"): "Intel Hardware H264 Encoder(QSV)",
    ("hevc_qsv", "h265"): "Intel Hardware H265 Encoder(QSV)",
    ("av1_qsv", "av1"): "Intel Hardware AV1 Encoder(QSV)",
    ("mjpeg_qsv", "mjpeg"): "Intel Hardware MJPEG Encoder(QSV)",
    ("mpeg2_qsv", "mpeg2"): "Intel Hardware MPEG-2 Encoder(QSV)",
    ("vp9_qsv", "vp9"): "Intel Hardware VP9 Encoder(QSV)",
    ("h264_amf", "h264"): "AMD Hardware H264 Encoder(AMF)",
    ("hevc_amf", "h265"): "AMD Hardware H265 Encoder(AMF)",
    ("av1_amf", "av1"): "AMD Hardware AV1 Encoder(AMF)",
    ("h264_mf", "h264"): "Microsoft Hardware H264 Encoder(MediaFoundation)",
    ("hevc_mf", "h265"): "Microsoft Hardware H265 Encoder(MediaFoundation)",
    ("av1_mf", "av1"): "Microsoft Hardware AV1 Encoder(MediaFoundation)",
    ("h264_d3d12va", "h264"): "Microsoft Direct3D 12 Video Acceleration H264 Encoder(D3D12VA)",
    ("hevc_d3d12va", "h265"): "Microsoft Direct3D 12 Video Acceleration H265 Encoder(D3D12VA)",
    ("av1_d3d12va", "av1"): "Microsoft Direct3D 12 Video Acceleration AV1 Encoder(D3D12VA)",
    ("h264_vaapi", "h264"): "Video Acceleration H264 Encoder(VAAPI)",
    ("hevc_vaapi", "h265"): "Video Acceleration H265 Encoder(VAAPI)",
    ("av1_vaapi", "av1"): "Video Acceleration AV1 Encoder(VAAPI)",
    ("mjpeg_vaapi", "mjpeg"): "Video Acceleration MJPEG Encoder(VAAPI)",
    ("mpeg2_vaapi", "mpeg2"): "Video Acceleration MPEG-2 Encoder(VAAPI)",
    ("vp8_vaapi", "vp8"): "Video Acceleration VP8 Encoder(VAAPI)",
    ("vp9_vaapi", "vp9"): "Video Acceleration VP9 Encoder(VAAPI)",
    ("h264_vulkan", "h264"): "Vulkan Hardware H264 Encoder(Vulkan)",
    ("hevc_vulkan", "h265"): "Vulkan Hardware H265 Encoder(Vulkan)",
    ("av1_vulkan", "av1"): "Vulkan Hardware AV1 Encoder(Vulkan)",
    ("h264_videotoolbox", "h264"): "Apple macOS Hardware H264 Encoder(VideoToolbox)",
    ("hevc_videotoolbox", "h265"): "Apple macOS Hardware H265 Encoder(VideoToolbox)",
    ("prores_videotoolbox", "prores"): "Apple macOS Hardware ProRes Encoder(VideoToolbox)",
}

ENCODERS = {
    "h264": {"lib": "libx264", "hw_encoders": ["h264_nvenc", "h264_qsv", "h264_amf", "h264_mf", "h264_d3d12va", "h264_vaapi", "h264_vulkan", "h264_videotoolbox"]},
    "h265": {"lib": "libx265", "hw_encoders": ["hevc_nvenc", "hevc_qsv", "hevc_amf", "hevc_mf", "hevc_d3d12va", "hevc_vaapi", "hevc_vulkan", "hevc_videotoolbox"]},
    "av1": {"lib": "librav1e", "hw_encoders": ["av1_nvenc", "av1_qsv", "av1_amf", "av1_mf", "av1_d3d12va", "av1_vaapi", "av1_vulkan"]},
    "mjpeg": {"lib": "mjpeg", "hw_encoders": ["mjpeg_qsv", "mjpeg_vaapi"]},
    "mpeg2": {"lib": "mpeg2video", "hw_encoders": ["mpeg2_qsv", "mpeg2_vaapi"]},
    "vp8": {"lib": "libvpx", "hw_encoders": ["vp8_vaapi"]},
    "vp9": {"lib": "libvpx-vp9", "hw_encoders": ["vp9_qsv", "vp9_vaapi"]},
    "prores": {"lib": "prores", "hw_encoders": ["prores_videotoolbox"]},
}

# Combine both decoder and encoder data
ALL_CODECS = {
    **DECODERS,
    **{k: v for k, v in ENCODERS.items() if k not in DECODERS}
}

# ─── Theme Constants (Fluent + macOS inspired) ─────────────────────────────
BG_ROOT       = "#1b1d23"     # deepest background
BG_SIDEBAR    = "#20222a"     # sidebar
BG_SURFACE    = "#272a33"     # card / surface
BG_ELEVATED   = "#2f3240"     # elevated surface
BG_INPUT      = "#353845"     # input fields
BG_HOVER      = "#3a3e50"     # hover state
BORDER        = "#3a3d48"     # subtle border
BORDER_LIGHT  = "#4a4e5c"     # lighter border
TEXT_PRIMARY   = "#ecedf2"    # primary text
TEXT_SECONDARY = "#9197a8"    # secondary text
TEXT_DIM       = "#626878"    # dim text
ACCENT        = "#6b8aff"     # accent blue (softer)
ACCENT_HOVER  = "#839dff"     # accent hover
ACCENT_SUBTLE = "#2a3158"     # accent subtle bg
GREEN         = "#4ade80"     # success green
GREEN_BG      = "#14291a"     # green background
GREEN_BORDER  = "#22543d"     # green border
RED           = "#f87171"     # error red
RED_BG        = "#2d1518"     # red background
RED_BORDER    = "#7f1d1d"     # red border
ORANGE        = "#fbbf24"     # warning orange
ORANGE_BG     = "#2d2510"     # orange background
ORANGE_BORDER = "#785815"     # orange border
PURPLE        = "#c084fc"     # purple accent
CYAN          = "#67e8f9"     # cyan accent
PROGRESS_BG   = "#2a2d38"     # progress bar background
PROGRESS_FG   = "#6b8aff"     # progress bar fill
SEPARATOR     = "#2a2d38"     # separator
NAV_ACTIVE    = "#2f3240"     # active nav bg
NAV_HOVER     = "#2a2d38"     # nav hover bg
BADGE_BG      = "#6b8aff22"   # badge background

FAMILY = "Segoe UI"
FAMILY_MONO = "Cascadia Code"
if sys.platform != "win32":
    FAMILY = "Helvetica Neue"
    FAMILY_MONO = "Menlo"

# Nav items definition
NAV_ITEMS = [
    ("detect", "🔍", "Codec Detection"),
    ("ffmpeg", "🛠", "FFmpeg Environment"),
    ("update", "🔄", "Check Updates"),
    ("settings", "⚙", "Settings"),
    ("about", "ℹ", "About"),
]


# ─── FFmpeg / Test Helpers ──────────────────────────────────────────────────

def _run_ffmpeg_command(command, verbose):
    """Executes an FFmpeg command and returns True on success, False on failure."""
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
            text=True
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except subprocess.CalledProcessError as e:
        return (False, e.stdout, e.stderr)
    except FileNotFoundError:
        return (False, "", "FFmpeg executable not found")


def _run_encoder_test_single(test_data):
    """Runs a single encoder test and returns the result."""
    import shlex

    codec, encoder, res_name, res_size, test_dir, verbose = test_data
    if codec == "prores":
        file_ext = ".mov"
    else:
        file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
    output_file = os.path.join(test_dir, f"{encoder}_{res_name}{file_ext}")

    if "vulkan" in encoder:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-init_hw_device", "vulkan=vk:0",
            "-f", "lavfi", "-i", f"color=white:s={res_size}:d=1",
            "-frames:v", "1",
            "-vf", "format=nv12,hwupload,format=vulkan",
            "-c:v", encoder, output_file,
        ]
    elif "d3d12va" in encoder:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-init_hw_device", "d3d12va:0",
            "-f", "lavfi", "-i", f"color=white:s={res_size}:d=1",
            "-frames:v", "1",
            "-vf", "format=nv12,hwupload",
            "-c:v", encoder, output_file,
        ]
    else:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-f", "lavfi", "-i", f"color=white:s={res_size}:d=1",
            "-frames:v", "1",
            "-c:v", encoder, "-pixel_format", "yuv420p", output_file,
        ]

    if "qsv" in encoder:
        command.insert(9, "-dual_gfx")
        command.insert(10, "0")

    if verbose:
        command[2] = "error"

    success, stdout, stderr = _run_ffmpeg_command(command, verbose)
    status = "succeeded" if success else "failed"

    if not success and os.path.exists(output_file):
        try:
            os.remove(output_file)
        except OSError:
            pass

    if verbose:
        info_str = f"codec: {codec}, encoder: {encoder}, resolution: {res_size}, status: {status}"
        command_str = " ".join(shlex.quote(arg) for arg in command)
        if stdout.strip() and stderr.strip():
            command_log = f"{stdout.strip()}\n{stderr.strip()}"
        elif stdout.strip():
            command_log = stdout.strip()
        elif stderr.strip():
            command_log = stderr.strip()
        else:
            command_log = "(none)"
        log_message = f"""
==================================================
[Encoder Detect Info]
{info_str}

[FFmpeg Command]
{command_str}

[Command Log]
{command_log}

""".strip()
        print(log_message)

    title = ENCODER_TITLES.get((encoder, codec), f"{encoder.upper()} Encoder:")
    command_str = " ".join(shlex.quote(arg) for arg in command)
    error_detail = stderr if stderr else stdout if stdout else "Unknown error"
    error_msg = f"{command_str}\n\n{error_detail}"
    return title, res_name, status, error_msg


def _run_decoder_test_single(test_data):
    """Runs a single decoder test and returns the result."""
    import shlex

    codec, hw_decoder, res_name, res_size, test_dir, verbose = test_data
    if codec == "prores":
        file_ext = ".mov"
    else:
        file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
    test_file_path = os.path.join(test_dir, f"{codec}_{res_name}{file_ext}")

    found_file = False
    for filename in os.listdir(test_dir):
        if filename.startswith(f"{codec}_") and f"_{res_name}" in filename:
            candidate_path = os.path.join(test_dir, filename)
            if os.path.exists(candidate_path) and os.path.getsize(candidate_path) > 0:
                test_file_path = candidate_path
                found_file = True
                break

    if not found_file:
        cpu_lib = ALL_CODECS[codec]["lib"]
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-f", "lavfi", "-i", f"color=white:s={res_size}:d=1",
            "-frames:v", "1", "-c:v", cpu_lib, "-pixel_format", "yuv420p",
            test_file_path,
        ]
        if not _run_ffmpeg_command(command, verbose)[0]:
            title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
            return title, res_name, "skipped", "Failed to create test file"

    if "vulkan" in hw_decoder:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-init_hw_device", "vulkan=vk:0",
            "-hwaccel", "vulkan", "-hwaccel_output_format", "vulkan",
            "-i", test_file_path, "-f", "null", "null",
        ]
    elif "videotoolbox" in hw_decoder:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-hwaccel", "videotoolbox",
            "-i", test_file_path, "-f", "null", "null",
        ]
    elif hw_decoder in ["dxva2", "d3d11va", "d3d12va"] and codec in ["h264", "h265", "vp8", "vp9", "av1", "mjpeg", "mpeg1", "mpeg2", "mpeg4"]:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-hwaccel", hw_decoder, "-i", test_file_path,
            "-c:v", "libx264", "-preset", "ultrafast",
            "-f", "null", "null",
        ]
    else:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-c:v", hw_decoder, "-i", test_file_path,
            "-c:v", "libx264", "-preset", "ultrafast",
            "-f", "null", "null",
        ]

    if verbose:
        command[2] = "error"

    success, stdout, stderr = _run_ffmpeg_command(command, verbose)
    status = "succeeded" if success else "failed"

    if verbose:
        info_str = f"codec: {codec}, decoder: {hw_decoder}, resolution: {res_size}, status: {status}"
        command_str = " ".join(shlex.quote(arg) for arg in command)
        if stdout.strip() and stderr.strip():
            command_log = f"{stdout.strip()}\n{stderr.strip()}"
        elif stdout.strip():
            command_log = stdout.strip()
        elif stderr.strip():
            command_log = stderr.strip()
        else:
            command_log = "(none)"
        log_message = f"""
==================================================
[Decoder Detect Info]
{info_str}

[FFmpeg Command]
{command_str}

[Command Log]
{command_log}

""".strip()
        print(log_message)

    title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
    command_str = " ".join(shlex.quote(arg) for arg in command)
    error_detail = stderr if stderr else stdout if stdout else "Unknown error"
    error_msg = f"{command_str}\n\n{error_detail}"
    return title, res_name, status, error_msg


def _run_encoder_bitdepth_test(test_data):
    """Tests encoder support for a specific pixel format."""
    import shlex

    codec, encoder, pix_fmt, bit_depth, chroma, test_dir, verbose = test_data
    if codec == "prores":
        file_ext = ".mov"
    else:
        file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
    output_file = os.path.join(test_dir, f"{encoder}_{pix_fmt}{file_ext}")

    if bit_depth == 8:
        if chroma == "4:2:0":
            out_pix_fmt = "yuv420p"
        elif chroma == "4:2:2":
            out_pix_fmt = "yuv422p"
        else:
            out_pix_fmt = "yuv444p"
    elif bit_depth == 10:
        if chroma == "4:2:0":
            out_pix_fmt = "p010le"
        elif chroma == "4:2:2":
            out_pix_fmt = "yuv422p10le"
        else:
            out_pix_fmt = "yuv444p10le"
    else:
        if chroma == "4:2:0":
            out_pix_fmt = "yuv420p12le"
        elif chroma == "4:2:2":
            out_pix_fmt = "yuv422p12le"
        else:
            out_pix_fmt = "yuv444p12le"

    if "vulkan" in encoder:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-init_hw_device", "vulkan=vk:0",
            "-f", "lavfi", "-i", f"color=white:s={BITDEPTH_CHROMA_RESOLUTION}:d=1",
            "-frames:v", "1",
            "-vf", f"format={pix_fmt},hwupload,format=vulkan",
            "-c:v", encoder, output_file,
        ]
    elif "d3d12va" in encoder:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-init_hw_device", "d3d12va:0",
            "-f", "lavfi", "-i", f"color=white:s={BITDEPTH_CHROMA_RESOLUTION}:d=1",
            "-frames:v", "1",
            "-vf", f"format={pix_fmt},hwupload",
            "-c:v", encoder, output_file,
        ]
    else:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-f", "lavfi", "-i", f"color=white:s={BITDEPTH_CHROMA_RESOLUTION}:d=1",
            "-frames:v", "1",
            "-c:v", encoder, "-pix_fmt", pix_fmt, output_file,
        ]

    if "qsv" in encoder:
        command.insert(9, "-dual_gfx")
        command.insert(10, "0")

    if verbose:
        command[2] = "error"

    success, stdout, stderr = _run_ffmpeg_command(command, verbose)
    status = "succeeded" if success else "failed"

    if not success and os.path.exists(output_file):
        try:
            os.remove(output_file)
        except OSError:
            pass

    if verbose:
        info_str = f"codec: {codec}, encoder: {encoder}, format: {pix_fmt}, status: {status}"
        command_str = " ".join(shlex.quote(arg) for arg in command)
        if stdout.strip() and stderr.strip():
            command_log = f"{stdout.strip()}\n{stderr.strip()}"
        elif stdout.strip():
            command_log = stdout.strip()
        elif stderr.strip():
            command_log = stderr.strip()
        else:
            command_log = "(none)"
        log_message = f"""
==================================================
[Bit-depth/Chroma Encoder Test]
{info_str}

[FFmpeg Command]
{command_str}

[Command Log]
{command_log}

""".strip()
        print(log_message)

    title = BD_ENCODER_TITLES.get((encoder, codec), f"{encoder.upper()} Encoder:")
    key = f"{bit_depth}-bit {chroma}"
    command_str = " ".join(shlex.quote(arg) for arg in command)
    error_detail = stderr if stderr else stdout if stdout else "Unknown error"
    error_msg = f"{command_str}\n\n{error_detail}"
    return title, key, status, error_msg


def _run_decoder_bitdepth_test(test_data):
    """Tests decoder support for a specific pixel format."""
    import shlex

    codec, hw_decoder, pix_fmt, bit_depth, chroma, test_dir, verbose = test_data
    if codec == "prores":
        file_ext = ".mov"
    else:
        file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
    test_file = os.path.join(test_dir, f"{codec}_{pix_fmt}{file_ext}")

    if not os.path.exists(test_file) or os.path.getsize(test_file) == 0:
        cpu_lib = BD_DECODERS[codec]["lib"]
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-f", "lavfi", "-i", f"color=white:s={BITDEPTH_CHROMA_RESOLUTION}:d=1",
            "-frames:v", "1", "-c:v", cpu_lib, "-pix_fmt", pix_fmt,
            test_file,
        ]
        if not _run_ffmpeg_command(command, verbose)[0]:
            title = BD_DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
            key = f"{bit_depth}-bit {chroma}"
            return title, key, "skipped", "Failed to create test file"

    if "vulkan" in hw_decoder:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-init_hw_device", "vulkan=vk:0",
            "-hwaccel", "vulkan", "-hwaccel_output_format", "vulkan",
            "-i", test_file, "-f", "null", "null",
        ]
    elif "videotoolbox" in hw_decoder:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-hwaccel", "videotoolbox",
            "-i", test_file, "-f", "null", "null",
        ]
    elif hw_decoder in ["dxva2", "d3d11va", "d3d12va"]:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-hwaccel", hw_decoder, "-i", test_file,
            "-c:v", "libx264", "-preset", "ultrafast",
            "-f", "null", "null",
        ]
    else:
        command = [
            "ffmpeg", "-loglevel", "error", "-hide_banner", "-y",
            "-c:v", hw_decoder, "-i", test_file,
            "-c:v", "libx264", "-preset", "ultrafast",
            "-f", "null", "null",
        ]

    if verbose:
        command[2] = "error"

    success, stdout, stderr = _run_ffmpeg_command(command, verbose)
    status = "succeeded" if success else "failed"

    if verbose:
        info_str = f"codec: {codec}, decoder: {hw_decoder}, format: {pix_fmt}, status: {status}"
        command_str = " ".join(shlex.quote(arg) for arg in command)
        if stdout.strip() and stderr.strip():
            command_log = f"{stdout.strip()}\n{stderr.strip()}"
        elif stdout.strip():
            command_log = stdout.strip()
        elif stderr.strip():
            command_log = stderr.strip()
        else:
            command_log = "(none)"
        log_message = f"""
==================================================
[Bit-depth/Chroma Decoder Test]
{info_str}

[FFmpeg Command]
{command_str}

[Command Log]
{command_log}

""".strip()
        print(log_message)

    title = BD_DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
    key = f"{bit_depth}-bit {chroma}"
    command_str = " ".join(shlex.quote(arg) for arg in command)
    error_detail = stderr if stderr else stdout if stdout else "Unknown error"
    error_msg = f"{command_str}\n\n{error_detail}"
    return title, key, status, error_msg


# ─── Custom Widgets ─────────────────────────────────────────────────────────

class _AccentProgressBar(tk.Canvas):
    """Smooth animated progress bar drawn on Canvas."""

    def __init__(self, parent, height=6, **kw):
        super().__init__(parent, height=height, highlightthickness=0, bd=0, **kw)
        self.configure(bg=BG_ROOT)
        self._pct = 0.0
        self._target_pct = 0.0
        self._bar_height = height
        self.bind("<Configure>", self._on_resize)

    def set_progress(self, pct, phase=""):
        self._target_pct = max(0.0, min(100.0, pct))
        self._animate()

    def _animate(self):
        diff = self._target_pct - self._pct
        if abs(diff) < 0.5:
            self._pct = self._target_pct
            self._draw()
            return
        self._pct += diff * 0.25
        self._draw()
        self.after(16, self._animate)

    def _draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self._bar_height
        if w < 2:
            return
        # Background
        self.create_rectangle(0, 0, w, h, fill=PROGRESS_BG, outline="")
        # Fill with rounded effect
        fill_w = int(w * self._pct / 100.0)
        if fill_w > 0:
            r = h // 2
            if fill_w < h:
                r = fill_w // 2
            self.create_rectangle(0, 0, fill_w, h, fill=PROGRESS_FG, outline="", width=0)

    def _on_resize(self, event):
        self._draw()


class _NavButton(tk.Frame):
    """Navigation button for the sidebar - Metro/Fluent style."""

    def __init__(self, parent, icon, text, command=None, active=False, **kw):
        super().__init__(parent, bg=BG_SIDEBAR, cursor="hand2", **kw)
        self._command = command
        self._active = active
        self._icon_text = icon
        self._label_text = text

        self._indicator = tk.Frame(self, bg=ACCENT, width=3)
        self._indicator.pack(side="left", fill="y")
        if not active:
            self._indicator.configure(bg=BG_SIDEBAR)

        self._inner = tk.Frame(self, bg=BG_SIDEBAR)
        self._inner.pack(side="left", fill="both", expand=True, padx=(4, 12), pady=10)

        self._icon_lbl = tk.Label(self._inner, text=icon, font=(FAMILY, 14),
                                  fg=TEXT_SECONDARY if not active else ACCENT,
                                  bg=BG_SIDEBAR)
        self._icon_lbl.pack(side="left", padx=(8, 12))

        self._text_lbl = tk.Label(self._inner, text=text, font=(FAMILY, 10),
                                  fg=TEXT_PRIMARY if not active else TEXT_PRIMARY,
                                  bg=BG_SIDEBAR)
        self._text_lbl.pack(side="left")

        self._update_style()
        self._bind_events(self)
        self._bind_events(self._inner)
        self._bind_events(self._icon_lbl)
        self._bind_events(self._text_lbl)

    def _bind_events(self, widget):
        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        widget.bind("<Button-1>", self._on_click)

    def set_active(self, active):
        self._active = active
        self._update_style()

    def _update_style(self):
        if self._active:
            self.configure(bg=NAV_ACTIVE)
            self._inner.configure(bg=NAV_ACTIVE)
            self._indicator.configure(bg=ACCENT)
            self._icon_lbl.configure(bg=NAV_ACTIVE, fg=ACCENT)
            self._text_lbl.configure(bg=NAV_ACTIVE, fg=TEXT_PRIMARY)
        else:
            bg = NAV_HOVER if hasattr(self, '_hovering') and self._hovering else BG_SIDEBAR
            self.configure(bg=bg)
            self._inner.configure(bg=bg)
            self._indicator.configure(bg=bg)
            self._icon_lbl.configure(bg=bg, fg=TEXT_SECONDARY)
            self._text_lbl.configure(bg=bg, fg=TEXT_SECONDARY)

    def _on_enter(self, e):
        self._hovering = True
        if not self._active:
            self.configure(bg=NAV_HOVER)
            self._inner.configure(bg=NAV_HOVER)
            self._icon_lbl.configure(bg=NAV_HOVER)
            self._text_lbl.configure(bg=NAV_HOVER)

    def _on_leave(self, e):
        self._hovering = False
        if not self._active:
            self.configure(bg=BG_SIDEBAR)
            self._inner.configure(bg=BG_SIDEBAR)
            self._icon_lbl.configure(bg=BG_SIDEBAR)
            self._text_lbl.configure(bg=BG_SIDEBAR)

    def _on_click(self, e):
        if self._command:
            self._command()


class _FlatButton(tk.Label):
    """Flat styled button with hover effect."""

    def __init__(self, parent, text="Button", command=None,
                 bg_color=BG_ELEVATED, hover_color=BG_HOVER, press_color=BORDER,
                 text_color=TEXT_PRIMARY, accent=False, font=None, padx=16, pady=8, **kw):
        self._bg = bg_color
        self._hover = hover_color
        self._press = press_color
        self._command = command
        self._enabled = True
        if accent:
            self._bg = ACCENT
            self._hover = ACCENT_HOVER
            self._press = "#5070d4"
            text_color = "#ffffff"
        _font = font or (FAMILY, 10)
        super().__init__(parent, text=text, bg=self._bg, fg=text_color,
                         font=_font, cursor="hand2", padx=padx, pady=pady, **kw)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def set_text(self, text):
        self.configure(text=text)

    def set_enabled(self, enabled):
        self._enabled = enabled
        if enabled:
            self.configure(bg=self._bg, fg=TEXT_PRIMARY, cursor="hand2")
        else:
            self.configure(bg=BG_INPUT, fg=TEXT_DIM, cursor="arrow")

    def _on_enter(self, e):
        if self._enabled:
            self.configure(bg=self._hover)

    def _on_leave(self, e):
        if self._enabled:
            self.configure(bg=self._bg)

    def _on_press(self, e):
        if self._enabled:
            self.configure(bg=self._press)

    def _on_release(self, e):
        if self._enabled:
            self.configure(bg=self._hover)
            if self._command:
                self._command()


class _PillTabBar(tk.Frame):
    """Pill-style tab switcher (like macOS segmented control)."""

    def __init__(self, parent, tabs, on_change=None, **kw):
        super().__init__(parent, bg=BG_ROOT, **kw)
        self._tabs = tabs  # list of (key, label)
        self._on_change = on_change
        self._active = None
        self._buttons = {}

        container = tk.Frame(self, bg=BG_SURFACE, highlightbackground=BORDER,
                             highlightthickness=1)
        container.pack()

        for key, label in self._tabs:
            btn = tk.Label(container, text=label, font=(FAMILY, 9),
                           fg=TEXT_SECONDARY, bg=BG_SURFACE,
                           padx=16, pady=8, cursor="hand2")
            btn.pack(side="left")
            btn.bind("<Enter>", lambda e, b=btn, k=key: self._hover(b, k))
            btn.bind("<Leave>", lambda e, b=btn, k=key: self._unhover(b, k))
            btn.bind("<Button-1>", lambda e, k=key: self._click(k))
            self._buttons[key] = btn

        self._indicator_frame = tk.Frame(self, height=3, bg=ACCENT)

        if self._tabs:
            self._activate(self._tabs[0][0])

    def _hover(self, btn, key):
        if self._active != key:
            btn.configure(fg=TEXT_PRIMARY, bg=BG_ELEVATED)

    def _unhover(self, btn, key):
        if self._active != key:
            btn.configure(fg=TEXT_SECONDARY, bg=BG_SURFACE)

    def _click(self, key):
        if key != self._active:
            self._activate(key)
            if self._on_change:
                self._on_change(key)

    def _activate(self, key):
        if self._active:
            old_btn = self._buttons.get(self._active)
            if old_btn:
                old_btn.configure(fg=TEXT_SECONDARY, bg=BG_SURFACE)
        self._active = key
        btn = self._buttons[key]
        btn.configure(fg=TEXT_PRIMARY, bg=ACCENT_SUBTLE)
        # Place indicator under the active button
        self._indicator_frame.pack_forget()
        self._indicator_frame.configure(bg=ACCENT)
        self.update_idletasks()
        # Position indicator below
        self._indicator_frame.place(in_=btn, relx=0, rely=1.0, relwidth=1.0, height=3, y=-3)


class _InfoCard(tk.Frame):
    """A styled information card."""

    def __init__(self, parent, title="", **kw):
        super().__init__(parent, bg=BG_SURFACE, highlightbackground=BORDER,
                         highlightthickness=1, **kw)
        if title:
            hdr = tk.Label(self, text=title, font=(FAMILY, 9, "bold"),
                           fg=TEXT_DIM, bg=BG_SURFACE, anchor="w")
            hdr.pack(fill="x", padx=16, pady=(12, 6))

        self._body = tk.Frame(self, bg=BG_SURFACE)
        self._body.pack(fill="both", expand=True, padx=16, pady=(0, 12))


class _StatusDot(tk.Canvas):
    """Animated status dot."""

    def __init__(self, parent, size=10, **kw):
        super().__init__(parent, width=size, height=size,
                         highlightthickness=0, bd=0, bg=BG_SURFACE, **kw)
        self._size = size
        self._color = TEXT_DIM
        self._draw()

    def set_status(self, color):
        self._color = color
        self._draw()

    def _draw(self):
        self.delete("all")
        s = self._size
        pad = 1
        self.create_oval(pad, pad, s - pad, s - pad, fill=self._color, outline="")


# ─── Main GUI Class ─────────────────────────────────────────────────────────

class HwCodecGUI:
    def __init__(self, root, args):
        self.root = root
        self.args = args
        self.stop_requested = False
        self.running = False
        self.tooltip_data = {}
        self._start_time = None
        self._current_page = None
        self._nav_buttons = {}

        self._setup_window()
        self._build_ui()
        self._check_for_updates_async()

    def _setup_window(self):
        self.root.configure(bg=BG_ROOT)
        self.root.minsize(1060, 720)
        try:
            self.root.option_add("*TCombobox*Listbox.background", BG_INPUT)
            self.root.option_add("*TCombobox*Listbox.foreground", TEXT_PRIMARY)
            self.root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
        except Exception:
            pass

    def _build_ui(self):
        # ── Header Bar ──
        header = tk.Frame(self.root, bg=BG_SIDEBAR, height=52)
        header.pack(fill="x")
        header.pack_propagate(False)

        hdr_inner = tk.Frame(header, bg=BG_SIDEBAR)
        hdr_inner.pack(fill="both", expand=True, padx=20)

        # App branding
        brand = tk.Frame(hdr_inner, bg=BG_SIDEBAR)
        brand.pack(side="left", pady=10)

        tk.Label(brand, text="◈", font=(FAMILY, 18), fg=ACCENT,
                 bg=BG_SIDEBAR).pack(side="left")
        tk.Label(brand, text=" HwCodecDetect", font=(FAMILY, 14, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_SIDEBAR).pack(side="left", padx=(6, 0))
        tk.Label(brand, text="v" + get_local_version(),
                 font=(FAMILY_MONO, 8), fg=TEXT_DIM,
                 bg=BG_SIDEBAR).pack(side="left", padx=(8, 0))

        # Header action buttons
        hdr_actions = tk.Frame(hdr_inner, bg=BG_SIDEBAR)
        hdr_actions.pack(side="right", pady=10)

        self._btn_check_update = _FlatButton(
            hdr_actions, text="↻  Check Updates", command=self._navigate_to_update,
            bg_color=BG_ELEVATED, hover_color=BG_HOVER, text_color=TEXT_SECONDARY,
            font=(FAMILY, 9), padx=12, pady=5)
        self._btn_check_update.pack(side="right", padx=(6, 0))

        self._btn_check_ffmpeg = _FlatButton(
            hdr_actions, text="🛠  FFmpeg Status", command=self._navigate_to_ffmpeg,
            bg_color=BG_ELEVATED, hover_color=BG_HOVER, text_color=TEXT_SECONDARY,
            font=(FAMILY, 9), padx=12, pady=5)
        self._btn_check_ffmpeg.pack(side="right", padx=(6, 0))

        # Thin separator
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

        # ── Main Body ──
        body = tk.Frame(self.root, bg=BG_ROOT)
        body.pack(fill="both", expand=True)

        # Left sidebar
        sidebar = tk.Frame(body, bg=BG_SIDEBAR, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self._build_sidebar(sidebar)

        # Thin vertical separator
        tk.Frame(body, bg=BORDER, width=1).pack(side="left", fill="y")

        # Right content area
        self._content = tk.Frame(body, bg=BG_ROOT)
        self._content.pack(side="left", fill="both", expand=True)

        # Build all pages (but only show the active one)
        self._pages = {}
        self._build_page_detect()
        self._build_page_ffmpeg()
        self._build_page_update()
        self._build_page_settings()
        self._build_page_about()

        self._show_page("detect")

        # ── Status Bar ──
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")
        status_bar = tk.Frame(self.root, bg=BG_SIDEBAR, height=28)
        status_bar.pack(fill="x")
        status_bar.pack_propagate(False)

        sb_inner = tk.Frame(status_bar, bg=BG_SIDEBAR)
        sb_inner.pack(fill="both", expand=True, padx=16)

        self.status_dot = _StatusDot(sb_inner, size=8)
        self.status_dot.pack(side="left", pady=8)
        self.status_dot.set_status(TEXT_DIM)

        self.status_lbl = tk.Label(sb_inner, text="Ready",
                                   font=(FAMILY, 9), fg=TEXT_SECONDARY, bg=BG_SIDEBAR)
        self.status_lbl.pack(side="left", padx=(6, 0), pady=8)

        self.timer_lbl = tk.Label(sb_inner, text="",
                                  font=(FAMILY_MONO, 9), fg=TEXT_DIM, bg=BG_SIDEBAR)
        self.timer_lbl.pack(side="right", pady=8)

    # ─── Sidebar ─────────────────────────────────────────────────────────────

    def _build_sidebar(self, parent):
        # Nav section label
        pad = tk.Frame(parent, bg=BG_SIDEBAR)
        pad.pack(fill="both", expand=True, padx=0, pady=(16, 0))

        tk.Label(pad, text="  NAVIGATION", font=(FAMILY, 8, "bold"),
                 fg=TEXT_DIM, bg=BG_SIDEBAR, anchor="w").pack(fill="x", padx=12, pady=(0, 8))

        for key, icon, label in NAV_ITEMS:
            btn = _NavButton(pad, icon, label,
                             command=lambda k=key: self._show_page(k),
                             active=(key == "detect"))
            btn.pack(fill="x", padx=0, pady=1)
            self._nav_buttons[key] = btn

        # Spacer
        tk.Frame(pad, bg=BG_SIDEBAR).pack(fill="both", expand=True)

        # Legend at bottom
        legend_card = tk.Frame(pad, bg=BG_SURFACE, highlightbackground=BORDER,
                               highlightthickness=1)
        legend_card.pack(fill="x", padx=12, pady=(0, 16))

        tk.Label(legend_card, text="  LEGEND", font=(FAMILY, 8, "bold"),
                 fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=12, pady=(10, 6))

        for symbol, color, desc in [
            ("●", GREEN, "Supported"),
            ("●", RED, "Not supported"),
            ("●", TEXT_DIM, "Skipped / Unavailable"),
        ]:
            row = tk.Frame(legend_card, bg=BG_SURFACE)
            row.pack(fill="x", padx=12, pady=1)
            tk.Label(row, text=symbol, font=(FAMILY, 8), fg=color,
                     bg=BG_SURFACE, width=2).pack(side="left")
            tk.Label(row, text=desc, font=(FAMILY, 9),
                     fg=TEXT_SECONDARY, bg=BG_SURFACE).pack(side="left")

        tk.Label(legend_card, text="", bg=BG_SURFACE).pack(pady=4)

    # ─── Page Navigation ─────────────────────────────────────────────────────

    def _show_page(self, key):
        if self._current_page == key:
            return
        self._current_page = key
        for k, btn in self._nav_buttons.items():
            btn.set_active(k == key)
        for k, frame in self._pages.items():
            if k == key:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    def _navigate_to_update(self):
        self._show_page("update")

    def _navigate_to_ffmpeg(self):
        self._show_page("ffmpeg")

    # ─── Page: Codec Detection ───────────────────────────────────────────────

    def _build_page_detect(self):
        page = tk.Frame(self._content, bg=BG_ROOT)
        self._pages["detect"] = page

        # Page header
        ph = tk.Frame(page, bg=BG_ROOT)
        ph.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(ph, text="Codec Detection", font=(FAMILY, 18, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_ROOT).pack(side="left")
        tk.Label(ph, text="Test hardware encoder & decoder capabilities",
                 font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_ROOT).pack(side="left", padx=(16, 0))

        # Progress area
        prog_frame = tk.Frame(page, bg=BG_ROOT)
        prog_frame.pack(fill="x", padx=24, pady=(16, 0))

        prog_top = tk.Frame(prog_frame, bg=BG_ROOT)
        prog_top.pack(fill="x")

        self.progress_phase = tk.Label(prog_top, text="", font=(FAMILY, 9),
                                       fg=TEXT_SECONDARY, bg=BG_ROOT, anchor="w")
        self.progress_phase.pack(side="left")

        self.progress_pct = tk.Label(prog_top, text="", font=(FAMILY_MONO, 10, "bold"),
                                     fg=ACCENT, bg=BG_ROOT, anchor="e")
        self.progress_pct.pack(side="right")

        self.progress = _AccentProgressBar(prog_frame, height=4)
        self.progress.pack(fill="x", pady=(6, 8))

        # Start/Stop button bar
        btn_bar = tk.Frame(page, bg=BG_ROOT)
        btn_bar.pack(fill="x", padx=24, pady=(0, 12))

        self.start_button = _FlatButton(
            btn_bar, text="▶  Start Detection", command=self.start_or_stop,
            accent=True, font=(FAMILY, 10, "bold"), padx=24, pady=10)
        self.start_button.pack(side="left")

        # Tab bar
        self._codec_tabs = _PillTabBar(page, [
            ("dec_res", "Decoders · Resolution"),
            ("enc_res", "Encoders · Resolution"),
            ("dec_bd",  "Decoders · Bit-depth"),
            ("enc_bd",  "Encoders · Bit-depth"),
        ], on_change=self._switch_codec_tab)
        self._codec_tabs.pack(fill="x", padx=24, pady=(0, 8))

        # Table container
        self._table_container = tk.Frame(page, bg=BG_ROOT)
        self._table_container.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        # Create tables
        self.table_dec_res = self._create_table(self._table_container)
        self.table_enc_res = self._create_table(self._table_container)
        self.table_dec_bd  = self._create_table(self._table_container)
        self.table_enc_bd  = self._create_table(self._table_container)

        self._table_frames = {
            "dec_res": self.table_dec_res[0],
            "enc_res": self.table_enc_res[0],
            "dec_bd":  self.table_dec_bd[0],
            "enc_bd":  self.table_enc_bd[0],
        }

        # Show first tab
        self._current_codec_tab = None
        self._switch_codec_tab("dec_res")

    def _switch_codec_tab(self, key):
        if self._current_codec_tab == key:
            return
        self._current_codec_tab = key
        for k, frame in self._table_frames.items():
            if k == key:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    # ─── Page: FFmpeg Environment ────────────────────────────────────────────

    def _build_page_ffmpeg(self):
        page = tk.Frame(self._content, bg=BG_ROOT)
        self._pages["ffmpeg"] = page

        # Page header
        ph = tk.Frame(page, bg=BG_ROOT)
        ph.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(ph, text="FFmpeg Environment", font=(FAMILY, 18, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_ROOT).pack(side="left")
        tk.Label(ph, text="Verify FFmpeg installation and hardware acceleration",
                 font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_ROOT).pack(side="left", padx=(16, 0))

        # Refresh button
        self._ffmpeg_refresh_btn = _FlatButton(
            ph, text="↻  Refresh", command=self._refresh_ffmpeg_env,
            font=(FAMILY, 9), padx=12, pady=5)
        self._ffmpeg_refresh_btn.pack(side="right")

        # Scrollable content
        scroll_canvas = tk.Canvas(page, bg=BG_ROOT, highlightthickness=0, bd=0)
        scroll_bar = tk.Scrollbar(page, orient="vertical", command=scroll_canvas.yview)
        self._ffmpeg_scroll_frame = tk.Frame(scroll_canvas, bg=BG_ROOT)

        self._ffmpeg_scroll_frame.bind(
            "<Configure>",
            lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))

        scroll_canvas.create_window((0, 0), window=self._ffmpeg_scroll_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scroll_bar.set)

        scroll_canvas.pack(side="left", fill="both", expand=True, padx=(24, 0), pady=16)
        scroll_bar.pack(side="right", fill="y", padx=(0, 24), pady=16)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        scroll_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self._ffmpeg_content = self._ffmpeg_scroll_frame

        # Build ffmpeg environment info cards (will be populated on refresh)
        self._ffmpeg_cards_frame = tk.Frame(self._ffmpeg_content, bg=BG_ROOT)
        self._ffmpeg_cards_frame.pack(fill="x")

        self._refresh_ffmpeg_env()

    def _refresh_ffmpeg_env(self):
        """Check and display FFmpeg environment information."""
        for widget in self._ffmpeg_cards_frame.winfo_children():
            widget.destroy()

        # Card 1: FFmpeg Installation Status
        card1 = tk.Frame(self._ffmpeg_cards_frame, bg=BG_SURFACE,
                         highlightbackground=BORDER, highlightthickness=1)
        card1.pack(fill="x", pady=(0, 12))

        tk.Label(card1, text="  INSTALLATION", font=(FAMILY, 9, "bold"),
                 fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            # FFmpeg found
            row = tk.Frame(card1, bg=BG_SURFACE)
            row.pack(fill="x", padx=16, pady=2)
            tk.Label(row, text="●", font=(FAMILY, 8), fg=GREEN,
                     bg=BG_SURFACE).pack(side="left")
            tk.Label(row, text="  FFmpeg Found", font=(FAMILY, 10, "bold"),
                     fg=GREEN, bg=BG_SURFACE).pack(side="left")

            row2 = tk.Frame(card1, bg=BG_SURFACE)
            row2.pack(fill="x", padx=16, pady=(4, 2))
            tk.Label(row2, text="Path", font=(FAMILY, 9),
                     fg=TEXT_DIM, bg=BG_SURFACE, width=12, anchor="w").pack(side="left")
            tk.Label(row2, text=ffmpeg_path, font=(FAMILY_MONO, 9),
                     fg=TEXT_PRIMARY, bg=BG_SURFACE, anchor="w").pack(side="left")

            # Get version
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW
            try:
                result = subprocess.run(
                    ["ffmpeg", "-version"], capture_output=True, text=True,
                    encoding='utf-8', errors='ignore', creationflags=creation_flags)
                version_line = result.stdout.split('\n')[0] if result.stdout else "Unknown"
            except Exception:
                version_line = "Unable to retrieve"

            row3 = tk.Frame(card1, bg=BG_SURFACE)
            row3.pack(fill="x", padx=16, pady=(2, 2))
            tk.Label(row3, text="Version", font=(FAMILY, 9),
                     fg=TEXT_DIM, bg=BG_SURFACE, width=12, anchor="w").pack(side="left")
            tk.Label(row3, text=version_line, font=(FAMILY_MONO, 9),
                     fg=TEXT_PRIMARY, bg=BG_SURFACE, anchor="w").pack(side="left")

            tk.Label(card1, text="", bg=BG_SURFACE).pack(pady=6)
        else:
            row = tk.Frame(card1, bg=BG_SURFACE)
            row.pack(fill="x", padx=16, pady=2)
            tk.Label(row, text="●", font=(FAMILY, 8), fg=RED,
                     bg=BG_SURFACE).pack(side="left")
            tk.Label(row, text="  FFmpeg Not Found", font=(FAMILY, 10, "bold"),
                     fg=RED, bg=BG_SURFACE).pack(side="left")

            row2 = tk.Frame(card1, bg=BG_SURFACE)
            row2.pack(fill="x", padx=16, pady=(4, 2))
            tk.Label(row2, text="FFmpeg is required for codec detection. Install it and add to PATH.",
                     font=(FAMILY, 9), fg=TEXT_SECONDARY, bg=BG_SURFACE, anchor="w").pack(fill="x")

            install_btn_frame = tk.Frame(card1, bg=BG_SURFACE)
            install_btn_frame.pack(fill="x", padx=16, pady=(8, 12))
            _FlatButton(install_btn_frame, text="⬇  Auto Install FFmpeg",
                        command=self._auto_install_ffmpeg_from_env,
                        accent=True, font=(FAMILY, 9), padx=16, pady=6).pack(side="left")

        # Card 2: Hardware Acceleration APIs
        card2 = tk.Frame(self._ffmpeg_cards_frame, bg=BG_SURFACE,
                         highlightbackground=BORDER, highlightthickness=1)
        card2.pack(fill="x", pady=(0, 12))

        tk.Label(card2, text="  HARDWARE ACCELERATION APIs", font=(FAMILY, 9, "bold"),
                 fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

        if ffmpeg_path:
            creation_flags = 0
            if sys.platform == "win32":
                creation_flags = subprocess.CREATE_NO_WINDOW
            try:
                result = subprocess.run(
                    ["ffmpeg", "-hide_banner", "-hwaccels"],
                    capture_output=True, text=True, encoding='utf-8',
                    errors='ignore', creationflags=creation_flags)
                hwaccels = [l.strip() for l in result.stdout.split('\n')
                            if l.strip() and not l.strip().startswith('Hardware acceleration')]
            except Exception:
                hwaccels = []

            if hwaccels:
                grid_frame = tk.Frame(card2, bg=BG_SURFACE)
                grid_frame.pack(fill="x", padx=16, pady=(0, 12))
                for i, hw in enumerate(hwaccels):
                    row_idx = i // 4
                    col_idx = i % 4
                    chip = tk.Label(grid_frame, text=f"  {hw}  ", font=(FAMILY_MONO, 9),
                                    fg=ACCENT, bg=ACCENT_SUBTLE, padx=8, pady=4)
                    chip.grid(row=row_idx, column=col_idx, padx=(0, 8), pady=4, sticky="w")
            else:
                tk.Label(card2, text="No hardware acceleration APIs detected.",
                         font=(FAMILY, 9), fg=TEXT_DIM, bg=BG_SURFACE).pack(fill="x", padx=16, pady=(0, 12))
        else:
            tk.Label(card2, text="FFmpeg not available — cannot query hardware APIs.",
                     font=(FAMILY, 9), fg=TEXT_DIM, bg=BG_SURFACE).pack(fill="x", padx=16, pady=(0, 12))

        # Card 3: Codec Summary
        if ffmpeg_path:
            card3 = tk.Frame(self._ffmpeg_cards_frame, bg=BG_SURFACE,
                             highlightbackground=BORDER, highlightthickness=1)
            card3.pack(fill="x", pady=(0, 12))

            tk.Label(card3, text="  CODEC SUPPORT SUMMARY", font=(FAMILY, 9, "bold"),
                     fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

            supported_enc, supported_dec = get_ffmpeg_supported_codecs()

            # Count support
            enc_total = sum(len(info["hw_encoders"]) for info in ENCODERS.values())
            dec_total = sum(len(info["hw_decoders"]) for info in DECODERS.values())
            enc_supported = 0
            dec_supported = 0
            for codec, info in ENCODERS.items():
                for e in info["hw_encoders"]:
                    if e in supported_enc:
                        enc_supported += 1
            for codec, info in DECODERS.items():
                for d in info["hw_decoders"]:
                    if d in supported_dec:
                        dec_supported += 1

            stats_frame = tk.Frame(card3, bg=BG_SURFACE)
            stats_frame.pack(fill="x", padx=16, pady=(0, 12))

            for label_text, value, total, color in [
                ("Encoders", enc_supported, enc_total, GREEN if enc_supported > 0 else TEXT_DIM),
                ("Decoders", dec_supported, dec_total, GREEN if dec_supported > 0 else TEXT_DIM),
                ("HW APIs", len(hwaccels) if 'hwaccels' in dir() else 0, "—", ACCENT),
            ]:
                col = tk.Frame(stats_frame, bg=BG_SURFACE)
                col.pack(side="left", padx=(0, 32))
                tk.Label(col, text=label_text, font=(FAMILY, 9),
                         fg=TEXT_DIM, bg=BG_SURFACE).pack(anchor="w")
                tk.Label(col, text=f"{value} / {total}", font=(FAMILY_MONO, 16, "bold"),
                         fg=color, bg=BG_SURFACE).pack(anchor="w")

    def _auto_install_ffmpeg_from_env(self):
        """Trigger FFmpeg auto-installation from the environment page."""
        if not messagebox.askyesno(
            "Install FFmpeg",
            "This will attempt to automatically download and install FFmpeg.\n\n"
            "Continue?"):
            return

        self._ffmpeg_refresh_btn.set_enabled(False)
        self._set_status("Installing FFmpeg...", ACCENT)

        def _install_thread():
            try:
                result = install_ffmpeg_if_needed()
                success = (result == 0 and shutil.which("ffmpeg"))
                self.root.after(0, lambda: self._on_ffmpeg_install_done(success))
            except Exception as e:
                print(f"Installation error: {e}")
                self.root.after(0, lambda: self._on_ffmpeg_install_done(False))

        t = threading.Thread(target=_install_thread, daemon=True)
        t.start()

    def _on_ffmpeg_install_done(self, success):
        self._ffmpeg_refresh_btn.set_enabled(True)
        if success:
            self._set_status("FFmpeg installed successfully", GREEN)
            messagebox.showinfo("Success", "FFmpeg has been installed successfully!")
        else:
            self._set_status("FFmpeg installation failed", RED)
            messagebox.showerror("Failed",
                                 "Automatic installation failed.\n\n"
                                 "Please install FFmpeg manually:\nhttps://ffmpeg.org/download.html")
        self._refresh_ffmpeg_env()

    # ─── Page: Check Updates ─────────────────────────────────────────────────

    def _build_page_update(self):
        page = tk.Frame(self._content, bg=BG_ROOT)
        self._pages["update"] = page

        # Page header
        ph = tk.Frame(page, bg=BG_ROOT)
        ph.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(ph, text="Check Updates", font=(FAMILY, 18, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_ROOT).pack(side="left")
        tk.Label(ph, text="Keep HwCodecDetect up to date",
                 font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_ROOT).pack(side="left", padx=(16, 0))

        # Content area
        center_frame = tk.Frame(page, bg=BG_ROOT)
        center_frame.pack(fill="both", expand=True, padx=24, pady=24)

        # Current version card
        ver_card = tk.Frame(center_frame, bg=BG_SURFACE,
                            highlightbackground=BORDER, highlightthickness=1)
        ver_card.pack(fill="x", pady=(0, 16))

        tk.Label(ver_card, text="  CURRENT VERSION", font=(FAMILY, 9, "bold"),
                 fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

        ver_row = tk.Frame(ver_card, bg=BG_SURFACE)
        ver_row.pack(fill="x", padx=16, pady=(0, 12))
        tk.Label(ver_row, text="◈", font=(FAMILY, 24), fg=ACCENT,
                 bg=BG_SURFACE).pack(side="left")
        ver_info = tk.Frame(ver_row, bg=BG_SURFACE)
        ver_info.pack(side="left", padx=(12, 0))
        tk.Label(ver_info, text=f"v{get_local_version()}", font=(FAMILY_MONO, 16, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_SURFACE).pack(anchor="w")
        tk.Label(ver_info, text="HwCodecDetect — Hardware Video Codec Detection Tool",
                 font=(FAMILY, 9), fg=TEXT_SECONDARY, bg=BG_SURFACE).pack(anchor="w")

        # Check button
        action_card = tk.Frame(center_frame, bg=BG_SURFACE,
                               highlightbackground=BORDER, highlightthickness=1)
        action_card.pack(fill="x", pady=(0, 16))

        tk.Label(action_card, text="  ACTIONS", font=(FAMILY, 9, "bold"),
                 fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

        btn_row = tk.Frame(action_card, bg=BG_SURFACE)
        btn_row.pack(fill="x", padx=16, pady=(0, 12))

        self._update_check_btn = _FlatButton(
            btn_row, text="🔍  Check for Updates Now",
            command=self._manual_check_update, accent=True,
            font=(FAMILY, 10, "bold"), padx=20, pady=8)
        self._update_check_btn.pack(side="left")

        _FlatButton(
            btn_row, text="↗  View on GitHub",
            command=lambda: webbrowser.open("https://github.com/whyb/HwCodecDetect/releases"),
            font=(FAMILY, 10), padx=16, pady=8).pack(side="left", padx=(12, 0))

        # Result area
        self._update_result_frame = tk.Frame(center_frame, bg=BG_ROOT)
        self._update_result_frame.pack(fill="x")

        # Initial result: checking indicator
        self._update_status_lbl = tk.Label(
            self._update_result_frame, text="",
            font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_ROOT)
        self._update_status_lbl.pack(fill="x")

    def _manual_check_update(self):
        """Manual update check triggered from the update page."""
        self._update_check_btn.set_enabled(False)
        try:
            if self._update_status_lbl.winfo_exists():
                self._update_status_lbl.configure(text="⏳  Checking for updates...", fg=TEXT_SECONDARY)
            else:
                self._update_status_lbl = tk.Label(
                    self._update_result_frame, text="⏳  Checking for updates...",
                    font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_ROOT)
                self._update_status_lbl.pack(fill="x")
        except tk.TclError:
            self._update_status_lbl = tk.Label(
                self._update_result_frame, text="⏳  Checking for updates...",
                font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_ROOT)
            self._update_status_lbl.pack(fill="x")

        def _check_thread():
            version_url = "https://raw.githubusercontent.com/whyb/HwCodecDetect/main/VERSION"
            try:
                response = requests.get(version_url, timeout=10)
                response.raise_for_status()
                latest = response.text.strip()
                current = get_local_version()
                if version.parse(latest) > version.parse(current):
                    self.root.after(0, lambda: self._show_update_result(
                        "update_available", current, latest))
                else:
                    self.root.after(0, lambda: self._show_update_result("up_to_date", current))
            except Exception as e:
                self.root.after(0, lambda: self._show_update_result("error", str(e)))

        t = threading.Thread(target=_check_thread, daemon=True)
        t.start()

    def _show_update_result(self, status, current="", latest=""):
        self._update_check_btn.set_enabled(True)
        for w in self._update_result_frame.winfo_children():
            w.destroy()

        card = tk.Frame(self._update_result_frame, bg=BG_SURFACE,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", pady=(12, 0))

        if status == "update_available":
            card.configure(highlightbackground=ACCENT)
            tk.Label(card, text="  UPDATE AVAILABLE", font=(FAMILY, 9, "bold"),
                     fg=ACCENT, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

            info_row = tk.Frame(card, bg=BG_SURFACE)
            info_row.pack(fill="x", padx=16, pady=4)
            tk.Label(info_row, text=f"Current: v{current}", font=(FAMILY_MONO, 10),
                     fg=TEXT_SECONDARY, bg=BG_SURFACE).pack(side="left")
            tk.Label(info_row, text="  →  ", font=(FAMILY, 10),
                     fg=TEXT_DIM, bg=BG_SURFACE).pack(side="left")
            tk.Label(info_row, text=f"Latest: v{latest}", font=(FAMILY_MONO, 10, "bold"),
                     fg=GREEN, bg=BG_SURFACE).pack(side="left")

            btn_row = tk.Frame(card, bg=BG_SURFACE)
            btn_row.pack(fill="x", padx=16, pady=(8, 12))
            release_url = f"https://github.com/whyb/HwCodecDetect/releases/tag/v{latest}"
            _FlatButton(btn_row, text="⬇  Download Update",
                        command=lambda: webbrowser.open(release_url),
                        accent=True, font=(FAMILY, 10, "bold"),
                        padx=16, pady=6).pack(side="left")
            _FlatButton(btn_row, text="View Changelog",
                        command=lambda: webbrowser.open("https://github.com/whyb/HwCodecDetect/releases"),
                        font=(FAMILY, 10), padx=16, pady=6).pack(side="left", padx=(8, 0))

        elif status == "up_to_date":
            card.configure(highlightbackground=GREEN_BORDER)
            tk.Label(card, text="  YOU ARE UP TO DATE", font=(FAMILY, 9, "bold"),
                     fg=GREEN, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))
            tk.Label(card, text=f"v{current} is the latest version.",
                     font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_SURFACE).pack(fill="x", padx=16, pady=(0, 12))

        elif status == "error":
            card.configure(highlightbackground=RED_BORDER)
            tk.Label(card, text="  CHECK FAILED", font=(FAMILY, 9, "bold"),
                     fg=RED, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))
            tk.Label(card, text=f"Could not check for updates: {current}",
                     font=(FAMILY, 9), fg=TEXT_SECONDARY, bg=BG_SURFACE,
                     wraplength=500, anchor="w").pack(fill="x", padx=16, pady=(0, 12))

    # ─── Page: Settings ──────────────────────────────────────────────────────

    def _build_page_settings(self):
        page = tk.Frame(self._content, bg=BG_ROOT)
        self._pages["settings"] = page

        # Page header
        ph = tk.Frame(page, bg=BG_ROOT)
        ph.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(ph, text="Settings", font=(FAMILY, 18, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_ROOT).pack(side="left")
        tk.Label(ph, text="Configure detection parameters",
                 font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_ROOT).pack(side="left", padx=(16, 0))

        # Settings cards
        settings_area = tk.Frame(page, bg=BG_ROOT)
        settings_area.pack(fill="both", expand=True, padx=24, pady=20)

        # Encoder workers card
        enc_card = tk.Frame(settings_area, bg=BG_SURFACE,
                            highlightbackground=BORDER, highlightthickness=1)
        enc_card.pack(fill="x", pady=(0, 12))

        tk.Label(enc_card, text="  ENCODER WORKERS", font=(FAMILY, 9, "bold"),
                 fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

        enc_inner = tk.Frame(enc_card, bg=BG_SURFACE)
        enc_inner.pack(fill="x", padx=16, pady=(0, 12))

        tk.Label(enc_inner, text="Number of parallel encoder test threads",
                 font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_SURFACE).pack(anchor="w")
        tk.Label(enc_inner, text="Higher values speed up testing but increase system load",
                 font=(FAMILY, 9), fg=TEXT_DIM, bg=BG_SURFACE).pack(anchor="w")

        spin_frame1 = tk.Frame(enc_inner, bg=BG_SURFACE)
        spin_frame1.pack(anchor="w", pady=(8, 0))
        self.encoder_var = tk.StringVar(value=str(self.args.encoder_count))
        enc_spin = tk.Spinbox(spin_frame1, from_=1, to=8, textvariable=self.encoder_var,
                              width=6, font=(FAMILY_MONO, 12), bg=BG_INPUT, fg=TEXT_PRIMARY,
                              buttonbackground=BG_ELEVATED, relief="flat",
                              highlightthickness=1, highlightbackground=BORDER,
                              highlightcolor=ACCENT, insertbackground=TEXT_PRIMARY)
        enc_spin.pack(side="left")
        tk.Label(spin_frame1, text="  (1 – 8)", font=(FAMILY, 9),
                 fg=TEXT_DIM, bg=BG_SURFACE).pack(side="left")

        # Decoder workers card
        dec_card = tk.Frame(settings_area, bg=BG_SURFACE,
                            highlightbackground=BORDER, highlightthickness=1)
        dec_card.pack(fill="x", pady=(0, 12))

        tk.Label(dec_card, text="  DECODER WORKERS", font=(FAMILY, 9, "bold"),
                 fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

        dec_inner = tk.Frame(dec_card, bg=BG_SURFACE)
        dec_inner.pack(fill="x", padx=16, pady=(0, 12))

        tk.Label(dec_inner, text="Number of parallel decoder test threads",
                 font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_SURFACE).pack(anchor="w")
        tk.Label(dec_inner, text="Higher values speed up testing but increase system load",
                 font=(FAMILY, 9), fg=TEXT_DIM, bg=BG_SURFACE).pack(anchor="w")

        spin_frame2 = tk.Frame(dec_inner, bg=BG_SURFACE)
        spin_frame2.pack(anchor="w", pady=(8, 0))
        self.decoder_var = tk.StringVar(value=str(self.args.decoder_count))
        dec_spin = tk.Spinbox(spin_frame2, from_=1, to=8, textvariable=self.decoder_var,
                              width=6, font=(FAMILY_MONO, 12), bg=BG_INPUT, fg=TEXT_PRIMARY,
                              buttonbackground=BG_ELEVATED, relief="flat",
                              highlightthickness=1, highlightbackground=BORDER,
                              highlightcolor=ACCENT, insertbackground=TEXT_PRIMARY)
        dec_spin.pack(side="left")
        tk.Label(spin_frame2, text="  (1 – 8)", font=(FAMILY, 9),
                 fg=TEXT_DIM, bg=BG_SURFACE).pack(side="left")

    # ─── Page: About ────────────────────────────────────────────────────────

    def _build_page_about(self):
        page = tk.Frame(self._content, bg=BG_ROOT)
        self._pages["about"] = page

        # Page header
        ph = tk.Frame(page, bg=BG_ROOT)
        ph.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(ph, text="About", font=(FAMILY, 18, "bold"),
                 fg=TEXT_PRIMARY, bg=BG_ROOT).pack(side="left")
        tk.Label(ph, text="Application information",
                 font=(FAMILY, 10), fg=TEXT_SECONDARY, bg=BG_ROOT).pack(side="left", padx=(16, 0))

        # Content area
        about_area = tk.Frame(page, bg=BG_ROOT)
        about_area.pack(fill="both", expand=True, padx=24, pady=20)

        # Description card
        desc_card = tk.Frame(about_area, bg=BG_SURFACE,
                             highlightbackground=BORDER, highlightthickness=1)
        desc_card.pack(fill="x", pady=(0, 12))

        tk.Label(desc_card, text="  DESCRIPTION", font=(FAMILY, 9, "bold"),
                 fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

        description = (
            "This tool automatically detects the hardware video codec capabilities of your system.\n"
            "Using FFmpeg, it tests various hardware codecs (like NVEnc, QSV, and VAAPI etc.)\n"
            "by generating and processing video files at different resolutions (from 240p to 8K).\n\n"
            "The result is a convenient summary table showing which hardware codecs are\n"
            "available on your system and what resolutions they support."
        )
        tk.Label(desc_card, text=description, font=(FAMILY, 10),
                 fg=TEXT_SECONDARY, bg=BG_SURFACE, anchor="w", justify="left",
                 wraplength=600).pack(fill="x", padx=16, pady=(0, 12))

        # App info card
        info_card = tk.Frame(about_area, bg=BG_SURFACE,
                             highlightbackground=BORDER, highlightthickness=1)
        info_card.pack(fill="x", pady=(0, 12))

        tk.Label(info_card, text="  INFO", font=(FAMILY, 9, "bold"),
                 fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

        about_frame = tk.Frame(info_card, bg=BG_SURFACE)
        about_frame.pack(fill="x", padx=16, pady=(0, 12))

        for label, value in [
            ("Application", "HwCodecDetect"),
            ("Version", "v" + get_local_version()),
            ("License", "BSD-3-Clause"),
            ("Author", "whyb"),
            ("Contact", "whyber@outlook.com"),
            ("Repository", "github.com/whyb/HwCodecDetect"),
        ]:
            row = tk.Frame(about_frame, bg=BG_SURFACE)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=label, font=(FAMILY, 9), fg=TEXT_DIM,
                     bg=BG_SURFACE, width=14, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=(FAMILY_MONO, 9), fg=TEXT_PRIMARY,
                     bg=BG_SURFACE, anchor="w").pack(side="left")

        # Links card
        links_card = tk.Frame(about_area, bg=BG_SURFACE,
                              highlightbackground=BORDER, highlightthickness=1)
        links_card.pack(fill="x", pady=(0, 12))

        tk.Label(links_card, text="  LINKS", font=(FAMILY, 9, "bold"),
                 fg=TEXT_DIM, bg=BG_SURFACE, anchor="w").pack(fill="x", padx=16, pady=(12, 6))

        links_frame = tk.Frame(links_card, bg=BG_SURFACE)
        links_frame.pack(fill="x", padx=16, pady=(0, 12))

        _FlatButton(links_frame, text="↗  GitHub Repository",
                    command=lambda: webbrowser.open("https://github.com/whyb/HwCodecDetect"),
                    font=(FAMILY, 10), padx=16, pady=6).pack(side="left")

        _FlatButton(links_frame, text="↗  Releases",
                    command=lambda: webbrowser.open("https://github.com/whyb/HwCodecDetect/releases"),
                    font=(FAMILY, 10), padx=16, pady=6).pack(side="left", padx=(8, 0))

    # ─── Treeview Table ──────────────────────────────────────────────────────

    def _create_table(self, parent):
        """Returns (container_frame, treeview) for a table."""
        container = tk.Frame(parent, bg=BG_ROOT)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Fluent.Treeview",
                         background=BG_SURFACE, foreground=TEXT_PRIMARY,
                         fieldbackground=BG_SURFACE, borderwidth=0,
                         font=(FAMILY, 9), rowheight=30)
        style.configure("Fluent.Treeview.Heading",
                         background=BG_ELEVATED, foreground=TEXT_SECONDARY,
                         borderwidth=0, font=(FAMILY, 9, "bold"), relief="flat",
                         padding=(8, 4))
        style.map("Fluent.Treeview",
                   background=[("selected", ACCENT_SUBTLE)],
                   foreground=[("selected", TEXT_PRIMARY)])
        style.map("Fluent.Treeview.Heading",
                   background=[("active", BG_HOVER)])
        style.layout("Fluent.Treeview",
                     [("Fluent.Treeview.treearea", {"sticky": "nswe"})])

        # Scrollbar styles (clam theme supports full color customization)
        style.configure("Fluent.Vertical.TScrollbar",
                         troughcolor=BG_SURFACE, background=BG_ELEVATED,
                         bordercolor=BG_SURFACE, arrowcolor=BG_SURFACE,
                         relief="flat", width=8)
        style.map("Fluent.Vertical.TScrollbar",
                   background=[("active", BG_HOVER), ("!active", BG_ELEVATED),
                               ("disabled", BG_SURFACE)],
                   arrowcolor=[("active", BG_HOVER), ("disabled", BG_SURFACE)])
        style.configure("Fluent.Horizontal.TScrollbar",
                         troughcolor=BG_SURFACE, background=BG_ELEVATED,
                         bordercolor=BG_SURFACE, arrowcolor=BG_SURFACE,
                         relief="flat", width=8)
        style.map("Fluent.Horizontal.TScrollbar",
                   background=[("active", BG_HOVER), ("!active", BG_ELEVATED),
                               ("disabled", BG_SURFACE)],
                   arrowcolor=[("active", BG_HOVER), ("disabled", BG_SURFACE)])
        # Remove scrollbar arrows by setting arrow size to 0 via layout
        style.layout("Fluent.Vertical.TScrollbar",
                     [("Fluent.Vertical.Scrollbar.trough",
                       {"sticky": "ns",
                        "children": [("Fluent.Vertical.Scrollbar.thumb",
                                      {"expand": "1", "sticky": "nswe"})]})])
        style.layout("Fluent.Horizontal.TScrollbar",
                     [("Fluent.Horizontal.Scrollbar.trough",
                       {"sticky": "ew",
                        "children": [("Fluent.Horizontal.Scrollbar.thumb",
                                      {"expand": "1", "sticky": "nswe"})]})])

        tree = ttk.Treeview(container, show="headings", style="Fluent.Treeview")
        tree.tag_configure("row_even", background=BG_SURFACE)
        tree.tag_configure("row_odd", background=BG_ELEVATED)
        # Status color tags
        tree.tag_configure("succeeded", foreground=GREEN)
        tree.tag_configure("failed", foreground=RED)
        tree.tag_configure("skipped", foreground=TEXT_DIM)
        # Combined row + status tags
        for row_tag in ("row_even", "row_odd"):
            for status in ("succeeded", "failed", "skipped"):
                bg = BG_SURFACE if row_tag == "row_even" else BG_ELEVATED
                fg = {"succeeded": GREEN, "failed": RED, "skipped": TEXT_DIM}[status]
                tree.tag_configure(f"{row_tag}_{status}", background=bg, foreground=fg)

        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview,
                            style="Fluent.Vertical.TScrollbar")
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview,
                            style="Fluent.Horizontal.TScrollbar")
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.grid_propagate(False)

        tree.bind("<ButtonRelease-1>", lambda e: self._on_cell_click(e, tree))

        return (container, tree)

    def _configure_resolution_columns(self, tree):
        columns = ["Codec"] + list(RESOLUTIONS.keys())
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            if col == "Codec":
                tree.column(col, width=220, minwidth=200, anchor="w", stretch=True)
            else:
                tree.column(col, width=60, minwidth=50, anchor="center", stretch=False)

    def _configure_bitdepth_columns(self, tree):
        format_columns = [
            "8-bit 4:2:0", "8-bit 4:2:2", "8-bit 4:4:4",
            "10-bit 4:2:0", "10-bit 4:2:2", "10-bit 4:4:4",
            "12-bit 4:2:0", "12-bit 4:2:2", "12-bit 4:4:4",
        ]
        columns = ["Codec"] + format_columns
        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            if col == "Codec":
                tree.column(col, width=220, minwidth=200, anchor="w", stretch=True)
            else:
                tree.column(col, width=80, minwidth=60, anchor="center", stretch=False)

    # ─── Async Update Check ──────────────────────────────────────────────────

    def _check_for_updates_async(self):
        version_str = get_local_version()
        t = threading.Thread(target=self._update_check_thread, args=(version_str,), daemon=True)
        t.start()

    def _update_check_thread(self, current_version):
        version_url = "https://raw.githubusercontent.com/whyb/HwCodecDetect/main/VERSION"
        release_url_base = "https://github.com/whyb/HwCodecDetect/releases/tag/v"
        try:
            response = requests.get(version_url, timeout=10)
            response.raise_for_status()
            latest_version = response.text.strip()
            if version.parse(latest_version) > version.parse(current_version):
                self.root.after(0, lambda: self._show_update_dialog(
                    current_version, latest_version, release_url_base + latest_version))
        except Exception as e:
            print(f"Update check failed: {e}")

    def _show_update_dialog(self, current, latest, url):
        title = "Update Available"
        message = (
            f"A new version is available!\n\n"
            f"Current: v{current}\n"
            f"Latest:  v{latest}\n\n"
            f"Would you like to visit the release page?"
        )
        if messagebox.askyesno(title, message):
            webbrowser.open(url)

    # ─── Start / Stop ────────────────────────────────────────────────────────

    def start_or_stop(self):
        if not self.running:
            self.start_test()
        else:
            self.stop_requested = True
            self.start_button.set_text("▶  Start Detection")
            self._clear_tables()

    def start_test(self):
        if not shutil.which("ffmpeg"):
            self.prompt_install_ffmpeg()
            return
        self._execute_test_flow()

    def prompt_install_ffmpeg(self):
        title = "FFmpeg Not Found"
        msg = (
            "FFmpeg is required but was not detected in your system PATH.\n\n"
            "Would you like to attempt automatic installation?\n"
            "(Supports Windows, Linux, and macOS)\n\n"
            "Or install manually: https://ffmpeg.org/download.html"
        )
        if messagebox.askyesno(title, msg):
            self.start_button.set_enabled(False)
            self._set_status("Installing FFmpeg...", ACCENT)
            self.progress.set_progress(0, "Installing FFmpeg...")

            t = threading.Thread(target=self.run_install_thread, daemon=True)
            t.start()

    def run_install_thread(self):
        def update_ui_after_install(success):
            self.progress.set_progress(0)
            self.start_button.set_enabled(True)
            if success:
                self._set_status("FFmpeg installed successfully", GREEN)
                messagebox.showinfo(
                    "Installation Complete",
                    "FFmpeg is ready! Click 'Start Detection' to begin.")
            else:
                self._set_status("FFmpeg installation failed", RED)
                messagebox.showerror(
                    "Installation Failed",
                    "Automatic installation failed.\n\n"
                    "Please install FFmpeg manually:\nhttps://ffmpeg.org/download.html")
        try:
            result = install_ffmpeg_if_needed()
            if result == 0 and shutil.which("ffmpeg"):
                self.root.after(0, lambda: update_ui_after_install(True))
            else:
                self.root.after(0, lambda: update_ui_after_install(False))
        except Exception as e:
            print(f"Installation error: {e}")
            self.root.after(0, lambda: update_ui_after_install(False))

    # ─── Test Flow ───────────────────────────────────────────────────────────

    def _execute_test_flow(self):
        enc = self._safe_count(self.encoder_var, default=self.args.encoder_count)
        dec = self._safe_count(self.decoder_var, default=self.args.decoder_count)
        self.args.encoder_count = enc
        self.args.decoder_count = dec

        self.stop_requested = False
        self.running = True
        self.start_button.set_text("■  Stop")
        self._clear_tables()
        self._set_status("Initializing detection...", ACCENT)

        self._start_time = time.monotonic()
        self._update_timer()

        t = threading.Thread(target=self.run_tests_thread, daemon=True)
        t.start()

    def _safe_count(self, var, default):
        try:
            v = int(var.get())
        except Exception:
            v = default
        if v < 1:
            v = 1
        if v > 8:
            v = 8
        var.set(str(v))
        return v

    def _update_timer(self):
        if not self.running or not self._start_time:
            return
        elapsed = time.monotonic() - self._start_time
        m, s = divmod(int(elapsed), 60)
        self.timer_lbl.configure(text=f"{m:02d}:{s:02d}")
        self.root.after(1000, self._update_timer)

    def _set_status(self, text, color=TEXT_SECONDARY):
        def _inner():
            self.status_lbl.configure(text=text)
            self.status_dot.set_status(color)
        self.root.after(0, _inner)

    def run_tests_thread(self):
        from .utils import get_temp_path
        temp_dir = os.path.join(get_temp_path(), "HwCodecDetect_GUI")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)

        self._set_status("Checking FFmpeg codec support...", ACCENT)
        print("\nChecking FFmpeg codec support...")
        unsupported_encoders, unsupported_decoders = check_codec_support(ENCODERS, DECODERS)
        if unsupported_encoders or unsupported_decoders:
            print(f"\nFound {len(unsupported_encoders)} unsupported encoder(s) and {len(unsupported_decoders)} unsupported decoder(s).")
            print("These codecs will be marked as unavailable '-' in the results.\n")
        else:
            print("All defined hardware codecs are supported.\n")

        encoder_results = defaultdict(dict)
        decoder_results = defaultdict(dict)
        bd_encoder_results = defaultdict(dict)
        bd_decoder_results = defaultdict(dict)

        total_enc_tasks = sum(
            len([e for e in info["hw_encoders"] if e not in unsupported_encoders]) * len(RESOLUTIONS)
            for info in ENCODERS.values()
        )
        total_dec_tasks = sum(
            len([d for d in info["hw_decoders"] if d not in unsupported_decoders]) * len(RESOLUTIONS)
            for info in DECODERS.values()
        )
        total_bd_enc_tasks = sum(
            len([e for e in info["hw_encoders"] if e not in unsupported_encoders]) * len(PIXEL_FORMATS)
            for info in BD_ENCODERS.values()
        )
        total_bd_dec_tasks = sum(
            len([d for d in info["hw_decoders"] if d not in unsupported_decoders]) * len(PIXEL_FORMATS)
            for info in BD_DECODERS.values()
        )
        total_tasks = total_enc_tasks + total_dec_tasks + total_bd_enc_tasks + total_bd_dec_tasks
        done_tasks = 0

        # ── Phase 1: Resolution Encoder Tests ──
        self._set_status("Testing encoders (resolution)...", ACCENT)
        enc_tasks = []
        for codec, info in ENCODERS.items():
            for encoder in info["hw_encoders"]:
                if encoder in unsupported_encoders:
                    title = ENCODER_TITLES.get((encoder, codec), f"{encoder.upper()} Encoder:")
                    for res_name in RESOLUTIONS.keys():
                        encoder_results[title][res_name] = ("skipped", "This codec is not supported by current FFmpeg version")
                    continue
                for res_name, res_size in RESOLUTIONS.items():
                    enc_tasks.append((codec, encoder, res_name, res_size, temp_dir, False))

        with ThreadPoolExecutor(max_workers=self.args.encoder_count) as executor:
            futures = [executor.submit(_run_encoder_test_single, t) for t in enc_tasks]
            for f in as_completed(futures):
                if self.stop_requested:
                    executor.shutdown(wait=False, cancel_futures=True)
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    self._finish_run(cancelled=True)
                    return
                title, res_name, status, error_msg = f.result()
                encoder_results[title][res_name] = (status, error_msg)
                done_tasks += 1
                pct = int(done_tasks * 100 / total_tasks)
                self._update_progress(pct, "Encoder Resolution")

        # ── Phase 2: Resolution Decoder Tests ──
        self._set_status("Testing decoders (resolution)...", ACCENT)
        dec_tasks = []
        for codec, info in DECODERS.items():
            for hw_decoder in info["hw_decoders"]:
                if hw_decoder in unsupported_decoders:
                    title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
                    for res_name in RESOLUTIONS.keys():
                        decoder_results[title][res_name] = "skipped"
                    continue
                for res_name, res_size in RESOLUTIONS.items():
                    dec_tasks.append((codec, hw_decoder, res_name, res_size, temp_dir, False))

        with ThreadPoolExecutor(max_workers=self.args.decoder_count) as executor:
            futures = [executor.submit(_run_decoder_test_single, t) for t in dec_tasks]
            for f in as_completed(futures):
                if self.stop_requested:
                    executor.shutdown(wait=False, cancel_futures=True)
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    self._finish_run(cancelled=True)
                    return
                title, res_name, status, error_msg = f.result()
                decoder_results[title][res_name] = (status, error_msg)
                done_tasks += 1
                pct = int(done_tasks * 100 / total_tasks)
                self._update_progress(pct, "Decoder Resolution")

        # ── Phase 3: Bit-depth Encoder Tests ──
        self._set_status("Testing encoders (bit-depth)...", ACCENT)
        bd_enc_tasks = []
        for codec, info in BD_ENCODERS.items():
            for encoder in info["hw_encoders"]:
                if encoder in unsupported_encoders:
                    title = BD_ENCODER_TITLES.get((encoder, codec), f"{encoder.upper()} Encoder:")
                    for pix_fmt, bit_depth, chroma, desc in PIXEL_FORMATS:
                        key = f"{bit_depth}-bit {chroma}"
                        bd_encoder_results[title][key] = "skipped"
                    continue
                for pix_fmt, bit_depth, chroma, desc in PIXEL_FORMATS:
                    bd_enc_tasks.append((codec, encoder, pix_fmt, bit_depth, chroma, temp_dir, False))

        with ThreadPoolExecutor(max_workers=self.args.encoder_count) as executor:
            futures = [executor.submit(_run_encoder_bitdepth_test, t) for t in bd_enc_tasks]
            for f in as_completed(futures):
                if self.stop_requested:
                    executor.shutdown(wait=False, cancel_futures=True)
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    self._finish_run(cancelled=True)
                    return
                title, key, status, error_msg = f.result()
                bd_encoder_results[title][key] = (status, error_msg)
                done_tasks += 1
                pct = int(done_tasks * 100 / total_tasks)
                self._update_progress(pct, "Encoder Bit-depth")

        # ── Phase 4: Bit-depth Decoder Tests ──
        self._set_status("Testing decoders (bit-depth)...", ACCENT)
        bd_dec_tasks = []
        for codec, info in BD_DECODERS.items():
            for hw_decoder in info["hw_decoders"]:
                if hw_decoder in unsupported_decoders:
                    title = BD_DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
                    for pix_fmt, bit_depth, chroma, desc in PIXEL_FORMATS:
                        key = f"{bit_depth}-bit {chroma}"
                        bd_decoder_results[title][key] = ("skipped", "This codec is not supported by current FFmpeg version")
                    continue
                for pix_fmt, bit_depth, chroma, desc in PIXEL_FORMATS:
                    bd_dec_tasks.append((codec, hw_decoder, pix_fmt, bit_depth, chroma, temp_dir, False))

        with ThreadPoolExecutor(max_workers=self.args.decoder_count) as executor:
            futures = [executor.submit(_run_decoder_bitdepth_test, t) for t in bd_dec_tasks]
            for f in as_completed(futures):
                if self.stop_requested:
                    executor.shutdown(wait=False, cancel_futures=True)
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    self._finish_run(cancelled=True)
                    return
                title, key, status, error_msg = f.result()
                bd_decoder_results[title][key] = (status, error_msg)
                done_tasks += 1
                pct = int(done_tasks * 100 / total_tasks)
                self._update_progress(pct, "Decoder Bit-depth")

        shutil.rmtree(temp_dir, ignore_errors=True)

        if not self.stop_requested:
            self._configure_resolution_columns(self.table_enc_res[1])
            self._configure_resolution_columns(self.table_dec_res[1])
            self._configure_bitdepth_columns(self.table_enc_bd[1])
            self._configure_bitdepth_columns(self.table_dec_bd[1])

            self._update_resolution_table(self.table_enc_res[1], encoder_results, kind="Encoder")
            self._update_resolution_table(self.table_dec_res[1], decoder_results, kind="Decoder")
            self._update_bitdepth_table(self.table_enc_bd[1], bd_encoder_results, kind="Encoder")
            self._update_bitdepth_table(self.table_dec_bd[1], bd_decoder_results, kind="Decoder")
            self._update_progress(100, "Complete")

        self._finish_run(cancelled=self.stop_requested)

    def _finish_run(self, cancelled=False):
        def _inner():
            self.running = False
            self.start_button.set_text("▶  Start Detection")
            if cancelled:
                self.progress.set_progress(0)
                self._clear_tables()
                self._set_status("Detection cancelled", ORANGE)
            else:
                elapsed = time.monotonic() - self._start_time if self._start_time else 0
                m, s = divmod(int(elapsed), 60)
                self._set_status(f"Detection complete  ·  {m}m {s}s elapsed", GREEN)
        self.root.after(0, _inner)

    def _update_progress(self, value, phase=""):
        def _inner():
            self.progress.set_progress(value, phase)
            self.progress_phase.configure(text=phase)
            self.progress_pct.configure(text=f"{value}%")
        self.root.after(0, _inner)

    def _clear_tables(self):
        for table in (self.table_dec_res[1], self.table_enc_res[1],
                      self.table_dec_bd[1], self.table_enc_bd[1]):
            for row in table.get_children():
                table.delete(row)

    # ─── Cell Click / Error Popup ────────────────────────────────────────────

    def _on_cell_click(self, event, table):
        region = table.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = table.identify_row(event.y)
        col = table.identify_column(event.x)
        if col == "#1":
            return
        item = table.item(row_id)
        values = item["values"]
        if not values:
            return
        codec_name = values[0]
        col_idx = int(col[1:]) - 2

        columns = list(table["columns"])
        if col_idx < 0 or col_idx >= len(columns) - 1:
            return
        col_name = columns[col_idx + 1]

        result = self.tooltip_data.get((table, codec_name, col_name))
        if result:
            status, error_msg = result
            if status in ("failed", "skipped"):
                self._show_error_popup(codec_name, col_name, error_msg, status)

    def _show_error_popup(self, codec_name, col_name, error_msg, status="failed"):
        popup = tk.Toplevel(self.root)
        popup.title("")
        popup.transient(self.root)
        popup.grab_set()
        popup.configure(bg=BG_ROOT)
        popup.overrideredirect(False)

        window_width = 640
        window_height = 440
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        center_x = main_x + (main_width - window_width) // 2
        center_y = main_y + (main_height - window_height) // 2
        popup.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Header
        hdr = tk.Frame(popup, bg=BG_SURFACE, height=48)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        hdr_inner = tk.Frame(hdr, bg=BG_SURFACE)
        hdr_inner.pack(fill="both", expand=True, padx=20)

        status_color = RED if status == "failed" else ORANGE
        status_text = "FAILED" if status == "failed" else "SKIPPED"
        tk.Label(hdr_inner, text="⚠", font=(FAMILY, 14), fg=status_color,
                 bg=BG_SURFACE).pack(side="left", pady=10)
        tk.Label(hdr_inner, text=f" {status_text}", font=(FAMILY, 12, "bold"),
                 fg=status_color, bg=BG_SURFACE).pack(side="left", pady=10)

        # Close button in header
        close_btn = tk.Label(hdr_inner, text="✕", font=(FAMILY, 12),
                             fg=TEXT_SECONDARY, bg=BG_SURFACE, cursor="hand2",
                             padx=8, pady=4)
        close_btn.pack(side="right", pady=10)
        close_btn.bind("<Button-1>", lambda e: popup.destroy())
        close_btn.bind("<Enter>", lambda e: close_btn.configure(fg=TEXT_PRIMARY))
        close_btn.bind("<Leave>", lambda e: close_btn.configure(fg=TEXT_SECONDARY))

        # Info
        info_frame = tk.Frame(popup, bg=BG_ROOT)
        info_frame.pack(fill="x", padx=20, pady=(16, 0))

        tk.Label(info_frame, text="Codec", font=(FAMILY, 8, "bold"), fg=TEXT_DIM,
                 bg=BG_ROOT, anchor="w").pack(fill="x")
        tk.Label(info_frame, text=codec_name, font=(FAMILY_MONO, 10), fg=TEXT_PRIMARY,
                 bg=BG_ROOT, anchor="w").pack(fill="x", pady=(2, 0))

        tk.Label(info_frame, text="Format", font=(FAMILY, 8, "bold"), fg=TEXT_DIM,
                 bg=BG_ROOT, anchor="w").pack(fill="x", pady=(10, 0))
        tk.Label(info_frame, text=col_name, font=(FAMILY_MONO, 10), fg=TEXT_PRIMARY,
                 bg=BG_ROOT, anchor="w").pack(fill="x", pady=(2, 0))

        # Separator
        tk.Frame(popup, bg=SEPARATOR, height=1).pack(fill="x", padx=20, pady=12)

        # Error detail
        detail_frame = tk.Frame(popup, bg=BG_ROOT)
        detail_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        tk.Label(detail_frame, text="DETAILS", font=(FAMILY, 8, "bold"),
                 fg=TEXT_DIM, bg=BG_ROOT, anchor="w").pack(fill="x", pady=(0, 6))

        text_frame = tk.Frame(detail_frame, bg=BG_SURFACE, highlightbackground=BORDER,
                              highlightthickness=1)
        text_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame, bg=BG_ELEVATED, troughcolor=BG_SURFACE,
                                 highlightthickness=0, bd=0, width=8)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set,
                              font=(FAMILY_MONO, 9), bg=BG_SURFACE, fg=TEXT_PRIMARY,
                              insertbackground=TEXT_PRIMARY, relief="flat",
                              highlightthickness=0, padx=10, pady=8,
                              selectbackground=ACCENT, selectforeground="#ffffff")
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        text_widget.insert("1.0", error_msg)
        text_widget.config(state="disabled")

        # Bottom button bar
        btn_frame = tk.Frame(popup, bg=BG_ROOT)
        btn_frame.pack(fill="x", padx=20, pady=(0, 16))
        _FlatButton(btn_frame, text="Close", command=popup.destroy,
                    bg_color=BG_ELEVATED, hover_color=BG_HOVER, press_color=BORDER_LIGHT,
                    text_color=TEXT_PRIMARY, padx=20, pady=6).pack(side="right")

    # ─── Table Update ────────────────────────────────────────────────────────

    def _update_resolution_table(self, table, results, kind):
        resolutions = list(RESOLUTIONS.keys())

        def _inner():
            for row in table.get_children():
                table.delete(row)

            filtered_titles = sorted(
                [t for t in results.keys() if kind in t]
            ) or sorted(results.keys())

            for idx, title in enumerate(filtered_titles):
                row = [title]
                for i, res in enumerate(resolutions):
                    result = results.get(title, {}).get(res, "skipped")
                    if isinstance(result, tuple):
                        status, error_msg = result
                    else:
                        status = result
                        error_msg = "This codec is not supported by current FFmpeg version" if status == "skipped" else "Unknown error"

                    self.tooltip_data[(table, title, res)] = (status, error_msg)

                    if status == "succeeded":
                        symbol = "✔"
                    elif status == "failed":
                        symbol = "✘"
                    else:
                        symbol = "—"
                    row.append(symbol)

                tag = "row_even" if idx % 2 == 0 else "row_odd"
                table.insert("", "end", values=row, tags=(tag,))

        self.root.after(0, _inner)

    def _update_bitdepth_table(self, table, results, kind):
        format_columns = [
            "8-bit 4:2:0", "8-bit 4:2:2", "8-bit 4:4:4",
            "10-bit 4:2:0", "10-bit 4:2:2", "10-bit 4:4:4",
            "12-bit 4:2:0", "12-bit 4:2:2", "12-bit 4:4:4",
        ]

        def _inner():
            for row in table.get_children():
                table.delete(row)

            filtered_titles = sorted(
                [t for t in results.keys() if kind in t]
            ) or sorted(results.keys())

            for idx, title in enumerate(filtered_titles):
                row = [title]
                for col_name in format_columns:
                    result = results.get(title, {}).get(col_name, "skipped")
                    if isinstance(result, tuple):
                        status, error_msg = result
                    else:
                        status = result
                        error_msg = "This codec is not supported by current FFmpeg version" if status == "skipped" else "Unknown error"

                    self.tooltip_data[(table, title, col_name)] = (status, error_msg)

                    if status == "succeeded":
                        symbol = "✔"
                    elif status == "failed":
                        symbol = "✘"
                    else:
                        symbol = "—"
                    row.append(symbol)

                tag = "row_even" if idx % 2 == 0 else "row_odd"
                table.insert("", "end", values=row, tags=(tag,))

        self.root.after(0, _inner)


def launch_gui(args):
    """Launch the GUI application."""
    root = tk.Tk()
    root.title("HwCodecDetect - Hardware Video Codec Detection Tool - v" + get_local_version())
    app = HwCodecGUI(root, args)
    root.mainloop()