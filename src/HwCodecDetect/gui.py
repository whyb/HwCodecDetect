"""
GUI Module for HwCodecDetect
Provides a graphical interface for hardware codec detection.
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

from .install_ffmpeg_if_needed import install_ffmpeg_if_needed
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
    ("vulkan", "h264"): "Vulkan Hardware H264 Decoder(Vulkan)",
    ("vulkan", "h265"): "Vulkan Hardware H265 Decoder(Vulkan)",
    ("vulkan", "av1"): "Vulkan Hardware AV1 Decoder(Vulkan)",
    ("videotoolbox", "h264"): "MacOS Hardware H264 Decoder(VideoToolbox)",
    ("videotoolbox", "h265"): "MacOS Hardware H265 Decoder(VideoToolbox)",
    ("videotoolbox", "mpeg2"): "MacOS Hardware MPEG-2 Decoder(VideoToolbox)",
    ("videotoolbox", "mpeg4"): "MacOS Hardware MPEG-4 Decoder(VideoToolbox)",
}

DECODERS = {
    "h264": {"lib": "libx264", "hw_decoders": ["h264_cuvid", "h264_qsv", "dxva2", "d3d11va", "vulkan", "videotoolbox"]},
    "h265": {"lib": "libx265", "hw_decoders": ["hevc_cuvid", "hevc_qsv", "d3d11va", "vulkan", "videotoolbox"]},
    "av1": {"lib": "librav1e", "hw_decoders": ["av1_cuvid", "av1_qsv", "dxva2", "d3d11va", "vulkan"]},
    "mjpeg": {"lib": "mjpeg", "hw_decoders": ["mjpeg_cuvid", "mjpeg_qsv", "dxva2", "d3d11va"]},
    "mpeg1": {"lib": "mpeg1video", "hw_decoders": ["mpeg1_cuvid", "dxva2", "d3d11va"]},
    "mpeg2": {"lib": "mpeg2video", "hw_decoders": ["mpeg2_cuvid", "mpeg2_qsv", "dxva2", "d3d11va", "videotoolbox"]},
    "mpeg4": {"lib": "mpeg4", "hw_decoders": ["mpeg4_cuvid", "dxva2", "d3d11va", "videotoolbox"]},
    "vp8": {"lib": "libvpx", "hw_decoders": ["vp8_cuvid", "vp8_qsv", "dxva2", "d3d11va"]},
    "vp9": {"lib": "libvpx-vp9", "hw_decoders": ["vp9_cuvid", "vp9_qsv", "dxva2", "d3d11va"]},
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
    ("h264_videotoolbox", "h264"): "MacOS Hardware H264 Encoder(VideoToolbox)",
    ("hevc_videotoolbox", "h265"): "MacOS Hardware H265 Encoder(VideoToolbox)",
}

ENCODERS = {
    "h264": {"lib": "libx264", "hw_encoders": ["h264_nvenc", "h264_qsv", "h264_amf", "h264_mf", "h264_d3d12va", "h264_vaapi", "h264_vulkan", "h264_videotoolbox"]},
    "h265": {"lib": "libx265", "hw_encoders": ["hevc_nvenc", "hevc_qsv", "hevc_amf", "hevc_mf", "hevc_d3d12va", "hevc_vaapi", "hevc_vulkan", "hevc_videotoolbox"]},
    "av1": {"lib": "librav1e", "hw_encoders": ["av1_nvenc", "av1_qsv", "av1_amf", "av1_mf", "av1_d3d12va", "av1_vaapi"]},
    "mjpeg": {"lib": "mjpeg", "hw_encoders": ["mjpeg_qsv", "mjpeg_vaapi"]},
    "mpeg2": {"lib": "mpeg2video", "hw_encoders": ["mpeg2_qsv", "mpeg2_vaapi"]},
    "vp8": {"lib": "libvpx", "hw_encoders": ["vp8_vaapi"]},
    "vp9": {"lib": "libvpx-vp9", "hw_encoders": ["vp9_qsv", "vp9_vaapi"]},
}

# Combine both decoder and encoder data
ALL_CODECS = {
    **DECODERS,
    **{k: v for k, v in ENCODERS.items() if k not in DECODERS}
}


def _run_ffmpeg_command(command, verbose):
    """Executes an FFmpeg command and returns True on success, False on failure."""
    import subprocess
    try:
        stdout = subprocess.PIPE if verbose else subprocess.DEVNULL
        stderr = subprocess.PIPE if verbose else subprocess.DEVNULL
        result = subprocess.run(
            command,
            check=True,
            stdout=stdout,
            stderr=stderr,
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
    import subprocess
    
    codec, encoder, res_name, res_size, test_dir, verbose = test_data
    file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
    output_file = os.path.join(test_dir, f"{encoder}_{res_name}{file_ext}")
    
    if "vulkan" in encoder:
        command = [
            "ffmpeg",
            "-loglevel", "quiet",
            "-hide_banner",
            "-y",
            "-init_hw_device", "vulkan=vk:0",
            "-f", "lavfi",
            "-i", f"color=white:s={res_size}:d=1",
            "-frames:v", "1",
            "-vf", "format=nv12,hwupload,format=vulkan",
            "-c:v", encoder,
            output_file,
        ]
    elif "d3d12va" in encoder:
        command = [
            "ffmpeg",
            "-loglevel", "quiet",
            "-hide_banner",
            "-y",
            "-init_hw_device", "d3d12va:0",
            "-f", "lavfi",
            "-i", f"color=white:s={res_size}:d=1",
            "-frames:v", "1",
            "-vf", "format=nv12,hwupload",
            "-c:v", encoder,
            output_file,
        ]
    else:
        command = [
            "ffmpeg",
            "-loglevel", "quiet",
            "-hide_banner",
            "-y",
            "-f", "lavfi",
            "-i", f"color=white:s={res_size}:d=1",
            "-frames:v", "1",
            "-c:v", encoder,
            "-pixel_format", "yuv420p",
            output_file,
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
    return title, res_name, status


def _run_decoder_test_single(test_data):
    """Runs a single decoder test and returns the result."""
    import shlex
    import subprocess
    
    codec, hw_decoder, res_name, res_size, test_dir, verbose = test_data
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
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
            "-f", "lavfi", "-i", f"color=white:s={res_size}:d=1",
            "-frames:v", "1", "-c:v", cpu_lib, "-pixel_format", "yuv420p",
            test_file_path,
        ]
        if not _run_ffmpeg_command(command, verbose)[0]:
            title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
            return title, res_name, "skipped"

    if "vulkan" in hw_decoder:
        command = [
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
            "-init_hw_device", "vulkan=vk:0",
            "-hwaccel", "vulkan",
            "-hwaccel_output_format", "vulkan",
            "-i", test_file_path,
            "-f", "null", "null",
        ]
    elif "videotoolbox" in hw_decoder:
        command = [
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
            "-hwaccel", "videotoolbox",
            "-i", test_file_path,
            "-f", "null", "null",
        ]
    elif hw_decoder in ["dxva2", "d3d11va"] and codec in ["h264", "h265", "vp8", "vp9", "av1", "mjpeg", "mpeg1", "mpeg2", "mpeg4"]:
        command = [
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
            "-hwaccel", hw_decoder, "-i", test_file_path,
            "-c:v", "libx264", "-preset", "ultrafast",
            "-f", "null", "null",
        ]
    else:
        command = [
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
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
    return title, res_name, status


def _run_encoder_bitdepth_test(test_data):
    """Tests encoder support for a specific pixel format."""
    import shlex
    
    codec, encoder, pix_fmt, bit_depth, chroma, test_dir, verbose = test_data
    
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
    else:  # 12-bit
        if chroma == "4:2:0":
            out_pix_fmt = "yuv420p12le"
        elif chroma == "4:2:2":
            out_pix_fmt = "yuv422p12le"
        else:
            out_pix_fmt = "yuv444p12le"

    if "vulkan" in encoder:
        command = [
            "ffmpeg",
            "-loglevel", "quiet",
            "-hide_banner",
            "-y",
            "-init_hw_device", "vulkan=vk:0",
            "-f", "lavfi",
            "-i", f"color=white:s={BITDEPTH_CHROMA_RESOLUTION}:d=1",
            "-frames:v", "1",
            "-vf", f"format={pix_fmt},hwupload,format=vulkan",
            "-c:v", encoder,
            output_file,
        ]
    elif "d3d12va" in encoder:
        command = [
            "ffmpeg",
            "-loglevel", "quiet",
            "-hide_banner",
            "-y",
            "-init_hw_device", "d3d12va:0",
            "-f", "lavfi",
            "-i", f"color=white:s={BITDEPTH_CHROMA_RESOLUTION}:d=1",
            "-frames:v", "1",
            "-vf", f"format={pix_fmt},hwupload",
            "-c:v", encoder,
            output_file,
        ]
    else:
        command = [
            "ffmpeg",
            "-loglevel", "quiet",
            "-hide_banner",
            "-y",
            "-f", "lavfi",
            "-i", f"color=white:s={BITDEPTH_CHROMA_RESOLUTION}:d=1",
            "-frames:v", "1",
            "-c:v", encoder,
            "-pix_fmt", pix_fmt,
            output_file,
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
    return title, key, status


def _run_decoder_bitdepth_test(test_data):
    """Tests decoder support for a specific pixel format."""
    import shlex
    
    codec, hw_decoder, pix_fmt, bit_depth, chroma, test_dir, verbose = test_data

    file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
    test_file = os.path.join(test_dir, f"{codec}_{pix_fmt}{file_ext}")

    if not os.path.exists(test_file) or os.path.getsize(test_file) == 0:
        cpu_lib = BD_DECODERS[codec]["lib"]
        command = [
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
            "-f", "lavfi", "-i", f"color=white:s={BITDEPTH_CHROMA_RESOLUTION}:d=1",
            "-frames:v", "1", "-c:v", cpu_lib, "-pix_fmt", pix_fmt,
            test_file,
        ]
        if not _run_ffmpeg_command(command, verbose)[0]:
            title = BD_DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
            key = f"{bit_depth}-bit {chroma}"
            return title, key, "skipped"

    if "vulkan" in hw_decoder:
        command = [
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
            "-init_hw_device", "vulkan=vk:0",
            "-hwaccel", "vulkan",
            "-hwaccel_output_format", "vulkan",
            "-i", test_file,
            "-f", "null", "null",
        ]
    elif "videotoolbox" in hw_decoder:
        command = [
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
            "-hwaccel", "videotoolbox",
            "-i", test_file,
            "-f", "null", "null",
        ]
    elif hw_decoder in ["dxva2", "d3d11va"]:
        command = [
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
            "-hwaccel", hw_decoder, "-i", test_file,
            "-c:v", "libx264", "-preset", "ultrafast",
            "-f", "null", "null",
        ]
    else:
        command = [
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
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
    return title, key, status


class HwCodecGUI:
    def __init__(self, root, args):
        self.root = root
        self.args = args
        self.stop_requested = False
        self.running = False

        frame = ttk.LabelFrame(root, text="Settings")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Encoder Multi-process Count (1-8):").grid(row=0, column=0, padx=5, pady=5)
        self.encoder_var = tk.StringVar(value=str(args.encoder_count))
        ttk.Entry(frame, textvariable=self.encoder_var, width=10).grid(row=0, column=1)

        ttk.Label(frame, text="Decoder Multi-process Count (1-8):").grid(row=0, column=2, padx=5, pady=5)
        self.decoder_var = tk.StringVar(value=str(args.decoder_count))
        ttk.Entry(frame, textvariable=self.decoder_var, width=10).grid(row=0, column=3)

        self.start_button = ttk.Button(frame, text="Start Test", command=self.start_or_stop)
        self.start_button.grid(row=0, column=4, columnspan=4, pady=10)

        self.progress = ttk.Progressbar(root, mode="determinate", maximum=100)
        self.progress.pack(fill="x", padx=10, pady=10)

        self.notebook = ttk.Notebook(root)
        
        # Resolution-based tabs
        self.tab_dec_res = ttk.Frame(self.notebook)
        self.tab_enc_res = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_dec_res, text="Decoders (Resolution)")
        self.notebook.add(self.tab_enc_res, text="Encoders (Resolution)")
        
        # Bit-depth/Chroma tabs
        self.tab_dec_bd = ttk.Frame(self.notebook)
        self.tab_enc_bd = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_dec_bd, text="Decoders (Bit-depth/Chroma)")
        self.notebook.add(self.tab_enc_bd, text="Encoders (Bit-depth/Chroma)")
        
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10, ipady=200)

        # Create resolution tables
        self.table_dec_res = self._create_resolution_table(self.tab_dec_res)
        self.table_enc_res = self._create_resolution_table(self.tab_enc_res)
        
        # Create bit-depth/chroma tables
        self.table_dec_bd = self._create_bitdepth_table(self.tab_dec_bd)
        self.table_enc_bd = self._create_bitdepth_table(self.tab_enc_bd)

    def _create_resolution_table(self, parent):
        """Creates a Treeview table for resolution-based results."""
        container = ttk.Frame(parent, height=500)
        container.pack(expand=True, fill="both")
        container.pack_propagate(False)

        columns = ["Codec"] + list(RESOLUTIONS.keys())

        tree = ttk.Treeview(container, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            width = 380 if col == "Codec" else 80
            tree.column(col, width=width, anchor="center")

        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        return tree

    def _create_bitdepth_table(self, parent):
        """Creates a Treeview table for bit-depth/chroma results."""
        container = ttk.Frame(parent, height=500)
        container.pack(expand=True, fill="both")
        container.pack_propagate(False)

        format_columns = [
            "8-bit 4:2:0",
            "8-bit 4:2:2",
            "8-bit 4:4:4",
            "10-bit 4:2:0",
            "10-bit 4:2:2",
            "10-bit 4:4:4",
            "12-bit 4:2:0",
            "12-bit 4:2:2",
            "12-bit 4:4:4",
        ]
        
        columns = ["Codec"] + format_columns

        tree = ttk.Treeview(container, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            width = 380 if col == "Codec" else 100
            tree.column(col, width=width, anchor="center")

        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        return tree

    def start_or_stop(self):
        if not self.running:
            self.start_test()
        else:
            self.stop_requested = True
            self.start_button.config(text="Start Test")
            self._clear_tables()

    def start_test(self):
        if not shutil.which("ffmpeg"):
            self.prompt_install_ffmpeg()
            return
        self._execute_test_flow()

    def prompt_install_ffmpeg(self):
        title = "Missing Component: FFmpeg Not Found"
        msg = (
            "The application requires the FFmpeg core component to access hardware acceleration, "
            "but it was not detected in your system PATH.\n\n"
            "Would you like to attempt an automatic download and configuration?\n"
            "(Supports Windows, Linux, and macOS)\n\n"
            "If you prefer to install it manually, please visit:\n"
            "https://ffmpeg.org/download.html"
        )

        if messagebox.askyesno(title, msg):
            self.start_button.config(state="disabled")
            self.progress["mode"] = "indeterminate"
            self.progress.start()

            t = threading.Thread(target=self.run_install_thread, daemon=True)
            t.start()

    def run_install_thread(self):
        def update_ui_after_install(success):
            self.progress.stop()
            self.progress["mode"] = "determinate"
            self.start_button.config(state="normal")

            if success:
                messagebox.showinfo(
                    "Installation Complete",
                    "FFmpeg environment is now ready! You can click 'Start Test' to detect hardware codec performance."
                )
            else:
                messagebox.showerror(
                    "Auto-Installation Failed",
                    "We were unable to complete the automatic installation. This is usually caused by network timeouts or insufficient permissions.\n\n"
                    "Suggested steps:\n"
                    "1. Download FFmpeg manually from: https://ffmpeg.org/download.html\n"
                    "2. Extract and add the 'bin' folder to your system environment variable (PATH)."
                )

        try:
            result = install_ffmpeg_if_needed()
            if result == 0 and shutil.which("ffmpeg"):
                self.root.after(0, lambda: update_ui_after_install(True))
            else:
                self.root.after(0, lambda: update_ui_after_install(False))
        except Exception as e:
            print(f"Installation error: {e}")
            self.root.after(0, lambda: update_ui_after_install(False))

    def _execute_test_flow(self):
        enc = self._safe_count(self.encoder_var, default=self.args.encoder_count)
        dec = self._safe_count(self.decoder_var, default=self.args.decoder_count)
        self.args.encoder_count = enc
        self.args.decoder_count = dec

        self.stop_requested = False
        self.running = True
        self.start_button.config(text="Stop")
        self.progress["value"] = 0
        self._clear_tables()

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

    def run_tests_thread(self):
        temp_dir = os.path.join(tempfile.gettempdir(), "HwCodecDetect_GUI")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)

        encoder_results = defaultdict(dict)
        decoder_results = defaultdict(dict)
        bd_encoder_results = defaultdict(dict)
        bd_decoder_results = defaultdict(dict)

        # Calculate total tasks
        total_enc_tasks = sum(
            len(info["hw_encoders"]) * len(RESOLUTIONS)
            for info in ENCODERS.values()
        )
        total_dec_tasks = sum(
            len(info["hw_decoders"]) * len(RESOLUTIONS)
            for info in DECODERS.values()
        )
        total_bd_enc_tasks = sum(
            len(info["hw_encoders"]) * len(PIXEL_FORMATS)
            for info in BD_ENCODERS.values()
        )
        total_bd_dec_tasks = sum(
            len(info["hw_decoders"]) * len(PIXEL_FORMATS)
            for info in BD_DECODERS.values()
        )
        total_tasks = total_enc_tasks + total_dec_tasks + total_bd_enc_tasks + total_bd_dec_tasks
        done_tasks = 0

        # Run resolution encoder tests
        enc_tasks = []
        for codec, info in ENCODERS.items():
            for encoder in info["hw_encoders"]:
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
                title, res_name, status = f.result()
                encoder_results[title][res_name] = status
                done_tasks += 1
                self._update_progress(int(done_tasks * 100 / total_tasks))

        # Run resolution decoder tests
        dec_tasks = []
        for codec, info in DECODERS.items():
            for hw_decoder in info["hw_decoders"]:
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
                title, res_name, status = f.result()
                decoder_results[title][res_name] = status
                done_tasks += 1
                self._update_progress(int(done_tasks * 100 / total_tasks))

        # Run bit-depth/chroma encoder tests
        bd_enc_tasks = []
        for codec, info in BD_ENCODERS.items():
            for encoder in info["hw_encoders"]:
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
                title, key, status = f.result()
                bd_encoder_results[title][key] = status
                done_tasks += 1
                self._update_progress(int(done_tasks * 100 / total_tasks))

        # Run bit-depth/chroma decoder tests
        bd_dec_tasks = []
        for codec, info in BD_DECODERS.items():
            for hw_decoder in info["hw_decoders"]:
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
                title, key, status = f.result()
                bd_decoder_results[title][key] = status
                done_tasks += 1
                self._update_progress(int(done_tasks * 100 / total_tasks))

        shutil.rmtree(temp_dir, ignore_errors=True)

        if not self.stop_requested:
            self._update_resolution_table(self.table_enc_res, encoder_results, kind="Encoder")
            self._update_resolution_table(self.table_dec_res, decoder_results, kind="Decoder")
            self._update_bitdepth_table(self.table_enc_bd, bd_encoder_results, kind="Encoder")
            self._update_bitdepth_table(self.table_dec_bd, bd_decoder_results, kind="Decoder")
            self._update_progress(100)

        self._finish_run(cancelled=self.stop_requested)

    def _finish_run(self, cancelled=False):
        def _inner():
            self.running = False
            self.start_button.config(text="Start Test")
            if cancelled:
                self.progress["value"] = 0
                self._clear_tables()
        self.root.after(0, _inner)

    def _update_progress(self, value):
        def _inner():
            self.progress["value"] = value
        self.root.after(0, _inner)

    def _clear_tables(self):
        for table in (self.table_dec_res, self.table_enc_res, self.table_dec_bd, self.table_enc_bd):
            for row in table.get_children():
                table.delete(row)

    def _update_resolution_table(self, table, results, kind):
        resolutions = list(RESOLUTIONS.keys())

        def _inner():
            for row in table.get_children():
                table.delete(row)

            filtered_titles = sorted(
                [t for t in results.keys() if kind in t]
            ) or sorted(results.keys())

            for title in filtered_titles:
                row = [title]
                for res in resolutions:
                    status = results.get(title, {}).get(res, "skipped")
                    if status == "succeeded":
                        symbol = "✅"
                    elif status == "failed":
                        symbol = "❌"
                    else:
                        symbol = "-"
                    row.append(symbol)
                table.insert("", "end", values=row)

        self.root.after(0, _inner)

    def _update_bitdepth_table(self, table, results, kind):
        format_columns = [
            "8-bit 4:2:0",
            "8-bit 4:2:2",
            "8-bit 4:4:4",
            "10-bit 4:2:0",
            "10-bit 4:2:2",
            "10-bit 4:4:4",
            "12-bit 4:2:0",
            "12-bit 4:2:2",
            "12-bit 4:4:4",
        ]

        def _inner():
            for row in table.get_children():
                table.delete(row)

            filtered_titles = sorted(
                [t for t in results.keys() if kind in t]
            ) or sorted(results.keys())

            for title in filtered_titles:
                row = [title]
                for col in format_columns:
                    status = results.get(title, {}).get(col, "skipped")
                    if status == "succeeded":
                        symbol = "✅"
                    elif status == "failed":
                        symbol = "❌"
                    else:
                        symbol = "-"
                    row.append(symbol)
                table.insert("", "end", values=row)

        self.root.after(0, _inner)


def launch_gui(args):
    """Launch the GUI application."""
    root = tk.Tk()
    root.title("HwCodecDetect - Hardware Video Codec Detection Tool")
    app = HwCodecGUI(root, args)
    root.mainloop()