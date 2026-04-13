"""
Bit-depth and Chroma Subsampling Detection Module
This module tests hardware codec support for different pixel formats.
"""
import os
import re
import sys
import shlex
import subprocess
import tempfile
from collections import defaultdict
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

init(autoreset=True)

# Fixed resolution for bit-depth and chroma tests
BITDEPTH_CHROMA_RESOLUTION = "1280x720"

# Pixel format definitions: (pix_fmt_name, bit_depth, chroma_sampling, description)
PIXEL_FORMATS = [
    ("yuv420p", 8, "4:2:0", "8-bit YUV 4:2:0"),
    ("yuv422p", 8, "4:2:2", "8-bit YUV 4:2:2"),
    ("yuv444p", 8, "4:4:4", "8-bit YUV 4:4:4"),
    ("yuv420p10le", 10, "4:2:0", "10-bit YUV 4:2:0"),
    ("yuv422p10le", 10, "4:2:2", "10-bit YUV 4:2:2"),
    ("yuv444p10le", 10, "4:4:4", "10-bit YUV 4:4:4"),
    ("yuv420p12le", 12, "4:2:0", "12-bit YUV 4:2:0"),
    ("yuv422p12le", 12, "4:2:2", "12-bit YUV 4:2:2"),
    ("yuv444p12le", 12, "4:4:4", "12-bit YUV 4:4:4"),
]

# Encoder titles (same as main module)
ENCODER_TITLES = {
    ("h264_nvenc", "h264"): "NVIDIA Hardware H264 Encoder(NVEnc)",
    ("hevc_nvenc", "h265"): "NVIDIA Hardware H265 Encoder(NVEnc)",
    ("av1_nvenc", "av1"): "NVIDIA Hardware AV1 Encoder(NVEnc)",
    ("h264_qsv", "h264"): "Intel Hardware H264 Encoder(QSV)",
    ("hevc_qsv", "h265"): "Intel Hardware H265 Encoder(QSV)",
    ("av1_qsv", "av1"): "Intel Hardware AV1 Encoder(QSV)",
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
    ("mpeg2_vaapi", "mpeg2"): "Video Acceleration MPEG-2 Encoder(VAAPI)",
    ("vp8_vaapi", "vp8"): "Video Acceleration VP8 Encoder(VAAPI)",
    ("vp9_vaapi", "vp9"): "Video Acceleration VP9 Encoder(VAAPI)",
    ("h264_vulkan", "h264"): "Vulkan Hardware H264 Encoder(Vulkan)",
    ("hevc_vulkan", "h265"): "Vulkan Hardware H265 Encoder(Vulkan)",
    ("av1_vulkan", "av1"): "Vulkan Hardware AV1 Encoder(Vulkan)",
    ("h264_videotoolbox", "h264"): "MacOS Hardware H264 Encoder(VideoToolbox)",
    ("hevc_videotoolbox", "h265"): "MacOS Hardware H265 Encoder(VideoToolbox)",
    ("prores_videotoolbox", "prores"): "MacOS Hardware ProRes Encoder(VideoToolbox)",
}

# Decoder titles (same as main module)
DECODER_TITLES = {
    ("h264_cuvid", "h264"): "NVIDIA CUDA H264 Decoder(NVDEC)",
    ("h264_qsv", "h264"): "Intel Quick Sync Video H264 Decoder(QSV)",
    ("hevc_cuvid", "h265"): "NVIDIA CUDA H265 Decoder(NVDEC)",
    ("hevc_qsv", "h265"): "Intel Quick Sync Video H265 Decoder(QSV)",
    ("av1_cuvid", "av1"): "NVIDIA CUDA AV1 Decoder(NVDEC)",
    ("av1_qsv", "av1"): "Intel Quick Sync Video AV1 Decoder(QSV)",
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
    ("dxva2", "mpeg1"): "Microsoft DirectX Video Acceleration MPEG-1 Decoder(DXVA2)",
    ("dxva2", "mpeg2"): "Microsoft DirectX Video Acceleration MPEG-2 Decoder(DXVA2)",
    ("dxva2", "mpeg4"): "Microsoft DirectX Video Acceleration MPEG-4 Decoder(DXVA2)",
    ("dxva2", "vp8"): "Microsoft DirectX Video Acceleration VP8 Decoder(DXVA2)",
    ("dxva2", "vp9"): "Microsoft DirectX Video Acceleration VP9 Decoder(DXVA2)",
    ("d3d11va", "h264"): "Microsoft Direct3D 11 Video Acceleration H264 Decoder(D3D11VA)",
    ("d3d11va", "h265"): "Microsoft Direct3D 11 Video Acceleration H265 Decoder(D3D11VA)",
    ("d3d11va", "av1"): "Microsoft Direct3D 11 Video Acceleration AV1 Decoder(D3D11VA)",
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
    ("videotoolbox", "prores"): "MacOS Hardware ProRes Decoder(VideoToolbox)",
}

# Encoder definitions (same as main module)
ENCODERS = {
    "h264": {"lib": "libx264", "hw_encoders": ["h264_nvenc", "h264_qsv", "h264_amf", "h264_mf", "h264_d3d12va", "h264_vaapi", "h264_vulkan", "h264_videotoolbox"]},
    "h265": {"lib": "libx265", "hw_encoders": ["hevc_nvenc", "hevc_qsv", "hevc_amf", "hevc_mf", "hevc_d3d12va", "hevc_vaapi", "hevc_vulkan", "hevc_videotoolbox"]},
    "av1": {"lib": "librav1e", "hw_encoders": ["av1_nvenc", "av1_qsv", "av1_amf", "av1_mf", "av1_d3d12va", "av1_vaapi", "av1_vulkan"]},
    "mpeg2": {"lib": "mpeg2video", "hw_encoders": ["mpeg2_qsv", "mpeg2_vaapi"]},
    "vp8": {"lib": "libvpx", "hw_encoders": ["vp8_vaapi"]},
    "vp9": {"lib": "libvpx-vp9", "hw_encoders": ["vp9_qsv", "vp9_vaapi"]},
    "prores": {"lib": "prores", "hw_encoders": ["prores_videotoolbox"]},
}

# Decoder definitions (same as main module)
DECODERS = {
    "h264": {"lib": "libx264", "hw_decoders": ["h264_cuvid", "h264_qsv", "dxva2", "d3d11va", "vulkan", "videotoolbox"]},
    "h265": {"lib": "libx265", "hw_decoders": ["hevc_cuvid", "hevc_qsv", "d3d11va", "vulkan", "videotoolbox"]},
    "av1": {"lib": "librav1e", "hw_decoders": ["av1_cuvid", "av1_qsv", "dxva2", "d3d11va", "vulkan"]},
    "mpeg1": {"lib": "mpeg1video", "hw_decoders": ["mpeg1_cuvid", "dxva2", "d3d11va"]},
    "mpeg2": {"lib": "mpeg2video", "hw_decoders": ["mpeg2_cuvid", "mpeg2_qsv", "dxva2", "d3d11va", "videotoolbox"]},
    "mpeg4": {"lib": "mpeg4", "hw_decoders": ["mpeg4_cuvid", "dxva2", "d3d11va", "videotoolbox"]},
    "vp8": {"lib": "libvpx", "hw_decoders": ["vp8_cuvid", "vp8_qsv", "dxva2", "d3d11va"]},
    "vp9": {"lib": "libvpx-vp9", "hw_decoders": ["vp9_cuvid", "vp9_qsv", "dxva2", "d3d11va"]},
    "prores": {"lib": "prores", "hw_decoders": ["videotoolbox"]},
}


def _run_ffmpeg_command(command, verbose):
    """Executes an FFmpeg command and returns True on success, False on failure."""
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


def _run_encoder_bitdepth_test(test_data):
    """Tests encoder support for a specific pixel format."""
    codec, encoder, pix_fmt, bit_depth, chroma, test_dir, verbose = test_data
    
    file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
    output_file = os.path.join(test_dir, f"{encoder}_{pix_fmt}{file_ext}")
    
    # Determine pixel format for output based on input format
    if bit_depth == 8:
        if chroma == "4:2:0":
            out_pix_fmt = "yuv420p"
        elif chroma == "4:2:2":
            out_pix_fmt = "yuv422p"
        else:  # 4:4:4
            out_pix_fmt = "yuv444p"
    elif bit_depth == 10:
        if chroma == "4:2:0":
            out_pix_fmt = "p010le"
        elif chroma == "4:2:2":
            out_pix_fmt = "yuv422p10le"
        else:  # 4:4:4
            out_pix_fmt = "yuv444p10le"
    else:  # 12-bit
        if chroma == "4:2:0":
            out_pix_fmt = "yuv420p12le"
        elif chroma == "4:2:2":
            out_pix_fmt = "yuv422p12le"
        else:  # 4:4:4
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

    # Clean up on failure
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

    title = ENCODER_TITLES.get((encoder, codec), f"{encoder.upper()} Encoder:")
    return title, pix_fmt, bit_depth, chroma, status


def _run_encoder_bitdepth_tests(test_dir, max_workers, verbose):
    """Tests encoder support for various pixel formats."""
    results = defaultdict(dict)

    print("\n--- Running Bit-depth/Chroma Encoder Tests ---")

    tasks = []
    for codec, info in ENCODERS.items():
        for encoder in info['hw_encoders']:
            for pix_fmt, bit_depth, chroma, desc in PIXEL_FORMATS:
                tasks.append((codec, encoder, pix_fmt, bit_depth, chroma, test_dir, verbose))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_run_encoder_bitdepth_test, task) for task in tasks]

        for future in tqdm(as_completed(futures), total=len(tasks), desc="Running encoder bit-depth tests"):
            title, pix_fmt, bit_depth, chroma, status = future.result()
            key = f"{bit_depth}-bit {chroma}"
            if title not in results:
                results[title] = {}
            results[title][key] = status

    return results


def _run_decoder_bitdepth_test(test_data):
    """Tests decoder support for a specific pixel format."""
    codec, hw_decoder, pix_fmt, bit_depth, chroma, test_dir, verbose = test_data

    file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
    test_file = os.path.join(test_dir, f"{codec}_{pix_fmt}{file_ext}")

    # Create test file with specific pixel format if it doesn't exist
    if not os.path.exists(test_file) or os.path.getsize(test_file) == 0:
        cpu_lib = DECODERS[codec]["lib"]
        command = [
            "ffmpeg", "-loglevel", "quiet", "-hide_banner", "-y",
            "-f", "lavfi", "-i", f"color=white:s={BITDEPTH_CHROMA_RESOLUTION}:d=1",
            "-frames:v", "1", "-c:v", cpu_lib, "-pix_fmt", pix_fmt,
            test_file,
        ]
        if not _run_ffmpeg_command(command, verbose)[0]:
            title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
            return title, pix_fmt, bit_depth, chroma, "skipped"

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

    title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
    return title, pix_fmt, bit_depth, chroma, status


def _run_decoder_bitdepth_tests(test_dir, max_workers, verbose):
    """Tests decoder support for various pixel formats."""
    results = defaultdict(dict)

    print("\n--- Running Bit-depth/Chroma Decoder Tests ---")

    tasks = []
    for codec, info in DECODERS.items():
        for hw_decoder in info['hw_decoders']:
            for pix_fmt, bit_depth, chroma, desc in PIXEL_FORMATS:
                tasks.append((codec, hw_decoder, pix_fmt, bit_depth, chroma, test_dir, verbose))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_run_decoder_bitdepth_test, task) for task in tasks]
        for future in tqdm(as_completed(futures), total=len(tasks), desc="Running decoder bit-depth tests"):
            title, pix_fmt, bit_depth, chroma, status = future.result()
            key = f"{bit_depth}-bit {chroma}"
            if title not in results:
                results[title] = {}
            results[title][key] = status
    return results


def _get_display_width(s):
    """Calculates the display width of a string, ignoring ANSI escape codes."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return len(ansi_escape.sub('', s))


def _print_bitdepth_chroma_table(results, table_type="Encoder"):
    """Prints a formatted summary table for bit-depth/chroma results."""
    GREEN_CHECK = Fore.GREEN + "✓" + Style.RESET_ALL
    RED_X = Fore.RED + "×" + Style.RESET_ALL
    GRAY_DASH = Fore.LIGHTBLACK_EX + "—" + Style.RESET_ALL

    # Define columns for the table
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

    titles = sorted(results.keys())

    col_width = max(len(col) for col in format_columns)
    row_header_width = max([_get_display_width(t) for t in titles] + [20, _get_display_width(table_type)])

    print("\n" + "=" * (row_header_width + 3 + (col_width + 3) * len(format_columns)))
    header_text = f"Bit-depth/Chroma {table_type} Support"
    padding_left = (row_header_width - _get_display_width(header_text)) // 2
    padding_right = row_header_width - _get_display_width(header_text) - padding_left
    header_row = f"| {' ' * padding_left}{header_text}{' ' * padding_right} |"
    for col in format_columns:
        header_row += f" {col.center(col_width)} |"
    print(header_row)
    print("-" * (row_header_width + 3 + (col_width + 3) * len(format_columns)))

    for title in titles:
        padding_needed = row_header_width - _get_display_width(title)
        row_string = f"| {title}{' ' * padding_needed} |"
        for col in format_columns:
            status = results.get(title, {}).get(col, "skipped")
            symbol = GREEN_CHECK if status == "succeeded" else RED_X if status == "failed" else GRAY_DASH
            symbol_width = _get_display_width(symbol)
            padding_left = (col_width - symbol_width) // 2
            padding_right = col_width - symbol_width - padding_left
            row_string += f" {' ' * padding_left}{symbol}{' ' * padding_right} |"
        print(row_string)
    print("=" * (row_header_width + 3 + (col_width + 3) * len(format_columns)))


def run_bitdepth_chroma_tests(encoder_count, decoder_count, verbose):
    """Run all bit-depth and chroma tests and return results."""
    import shutil
    temp_dir = os.path.join(tempfile.gettempdir(), "HwCodecDetect_BitDepth")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    encoder_results = _run_encoder_bitdepth_tests(temp_dir, encoder_count, verbose)
    decoder_results = _run_decoder_bitdepth_tests(temp_dir, decoder_count, verbose)

    # Clean up
    shutil.rmtree(temp_dir)

    return encoder_results, decoder_results


def print_bitdepth_chroma_results(encoder_results, decoder_results):
    """Print bit-depth and chroma test results."""
    if decoder_results:
        _print_bitdepth_chroma_table(decoder_results, "Decoder")
    if encoder_results:
        _print_bitdepth_chroma_table(encoder_results, "Encoder")
