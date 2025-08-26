import os
import re
import sys
import subprocess
import shutil
import tempfile
from collections import defaultdict
from .install_ffmpeg_if_needed import install_ffmpeg_if_needed

# Step 0: Define the data for codecs and resolutions
# This approach avoids massive code duplication.
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

# Mapping of a decoder's ffmpeg name and codec to its descriptive title
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
    ("d3d11va", "h264"): "Direct3D 11 Video Acceleration H264 Decoder(D3D11VA)",
    ("d3d11va", "h265"): "Direct3D 11 Video Acceleration H265 Decoder(D3D11VA)",
    ("d3d11va", "av1"): "Direct3D 11 Video Acceleration AV1 Decoder(D3D11VA)",
    ("d3d11va", "mjpeg"): "Direct3D 11 Video Acceleration MJPEG Decoder(D3D11VA)",
    ("d3d11va", "mpeg1"): "Direct3D 11 Video Acceleration MPEG-1 Decoder(D3D11VA)",
    ("d3d11va", "mpeg2"): "Direct3D 11 Video Acceleration MPEG-2 Decoder(D3D11VA)",
    ("d3d11va", "mpeg4"): "Direct3D 11 Video Acceleration MPEG-4 Decoder(D3D11VA)",
    ("d3d11va", "vp8"): "Direct3D 11 Video Acceleration VP8 Decoder(D3D11VA)",
    ("d3d11va", "vp9"): "Direct3D 11 Video Acceleration VP9 Decoder(D3D11VA)",
}

DECODERS = {
    "h264": {"lib": "libx264", "hw_decoders": ["h264_cuvid", "h264_qsv", "dxva2", "d3d11va"], "type": "decoder"},
    "h265": {"lib": "libx265", "hw_decoders": ["hevc_cuvid", "hevc_qsv", "d3d11va"], "type": "decoder"},
    "av1": {"lib": "librav1e", "hw_decoders": ["av1_cuvid", "av1_qsv", "dxva2", "d3d11va"], "type": "decoder"},
    "mjpeg": {"lib": "mjpeg", "hw_decoders": ["mjpeg_cuvid", "mjpeg_qsv", "dxva2", "d3d11va"], "type": "decoder"},
    "mpeg1": {"lib": "mpeg1video", "hw_decoders": ["mpeg1_cuvid", "dxva2", "d3d11va"], "type": "decoder"},
    "mpeg2": {"lib": "mpeg2video", "hw_decoders": ["mpeg2_cuvid", "mpeg2_qsv", "dxva2", "d3d11va"], "type": "decoder"},
    "mpeg4": {"lib": "mpeg4", "hw_decoders": ["mpeg4_cuvid", "dxva2", "d3d11va"], "type": "decoder"},
    "vp8": {"lib": "libvpx", "hw_decoders": ["vp8_cuvid", "vp8_qsv", "dxva2", "d3d11va"], "type": "decoder"},
    "vp9": {"lib": "libvpx-vp9", "hw_decoders": ["vp9_cuvid", "vp9_qsv", "dxva2", "d3d11va"], "type": "decoder"},
}

# --- Encoder Definitions ---
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
    ("h264_vaapi", "h264"): "Video Acceleration H264 Encoder(VAAPI)",
    ("hevc_vaapi", "h265"): "Video Acceleration H265 Encoder(VAAPI)",
    ("av1_vaapi", "av1"): "Video Acceleration AV1 Encoder(VAAPI)",
    ("mjpeg_vaapi", "mjpeg"): "Video Acceleration MJPEG Encoder(VAAPI)",
    ("mpeg2_vaapi", "mpeg2"): "Video Acceleration MPEG-2 Encoder(VAAPI)",
    ("vp8_vaapi", "vp8"): "Video Acceleration VP8 Encoder(VAAPI)",
    ("vp9_vaapi", "vp9"): "Video Acceleration VP9 Encoder(VAAPI)",
    ("h264_vulkan", "h264"): "Vulkan Hardware H264 Encoder",
    ("hevc_vulkan", "h265"): "Vulkan Hardware H265 Encoder",
}

ENCODERS = {
    "h264": ["h264_nvenc", "h264_qsv", "h264_amf", "h264_mf", "h264_vaapi", "h264_vulkan"],
    "h265": ["hevc_nvenc", "hevc_qsv", "hevc_amf", "hevc_mf", "hevc_vaapi", "hevc_vulkan"],
    "av1": ["av1_nvenc", "av1_qsv", "av1_amf", "av1_vaapi"],
    "mjpeg": ["mjpeg_qsv", "mjpeg_vaapi"],
    "mpeg2": ["mpeg2_qsv", "mpeg2_vaapi"],
    "vp8": ["vp8_vaapi"],
    "vp9": ["vp9_qsv", "vp9_vaapi"],
}

def _run_ffmpeg_command(command):
    """Executes an FFmpeg command and returns True on success, False on failure."""
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def _generate_test_files(test_dir):
    """Generates a series of test video files using CPU encoders."""
    print("Generating test video files...")
    for codec, info in DECODERS.items():
        for res_name, res_size in RESOLUTIONS.items():
            file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
            file_path = os.path.join(test_dir, f"{codec}_{res_name}{file_ext}")
            
            if os.path.exists(file_path):
                continue

            command = [
                "ffmpeg",
                "-loglevel", "quiet",
                "-hide_banner",
                "-y",
                "-f", "lavfi",
                "-i", f"color=white:s={res_size}:d=1",
                "-frames:v", "1",
                "-c:v", info['lib'],
                *([f"-preset", "ultrafast"] if codec in ["h264", "h265"] else []),
                "-pixel_format", "yuv420p",
                file_path,
            ]
            
            if not _run_ffmpeg_command(command):
                print(f"Error generating {codec}_{res_name}{file_ext}", file=sys.stderr)
    print("Test file generation complete.")

def _run_decoder_tests(test_dir):
    """Runs hardware decoder tests and returns a structured dictionary of results."""
    results = defaultdict(dict)
    
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    print("\n--- Running Decoder Tests ---")

    for codec, info in DECODERS.items():
        if info['type'] != 'decoder':
            continue
            
        for hw_decoder in info['hw_decoders']:
            title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
            print(f"\n{title}")

            for res_name in RESOLUTIONS:
                file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
                input_file = os.path.join(test_dir, f"{codec}_{res_name}{file_ext}")
                
                if not os.path.exists(input_file):
                    results[title][res_name] = "skipped"
                    print(f"  {res_name}: {RED}skipped (file not found){RESET}")
                    continue

                if hw_decoder in ["dxva2", "d3d11va"] and codec in ["h264", "h265", "vp8"]:
                    command = [
                        "ffmpeg",
                        "-loglevel", "quiet",
                        "-hide_banner",
                        "-y",
                        "-hwaccel", hw_decoder,
                        "-i", input_file,
                        "-c:v", "libx264",
                        "-preset", "ultrafast",
                        "-f", "null", "null",
                    ]
                else:
                    command = [
                        "ffmpeg",
                        "-loglevel", "quiet",
                        "-hide_banner",
                        "-y",
                        "-c:v", hw_decoder,
                        "-i", input_file,
                        "-c:v", "libx264",
                        "-preset", "ultrafast",
                        "-f", "null", "null",
                    ]
                
                status = "succeeded" if _run_ffmpeg_command(command) else "failed"
                results[title][res_name] = status
                
                color_code = GREEN if status == "succeeded" else RED
                print(f"  {res_name}: {color_code}{status}{RESET}")

    return results

def _run_encoder_tests(test_dir):
    """Runs hardware encoder tests and returns a structured dictionary of results."""
    results = defaultdict(dict)
    
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    
    print("\n--- Running Encoder Tests ---")

    for codec, encoder_list in ENCODERS.items():
        for encoder in encoder_list:
            title = ENCODER_TITLES.get((encoder, codec), f"{encoder.upper()} Encoder:")
            print(f"\n{title}")

            for res_name, res_size in RESOLUTIONS.items():
                file_ext = ".webm" if codec in ["vp8", "vp9"] else ".mp4"
                output_file = os.path.join(test_dir, f"{encoder}_{res_name}{file_ext}")

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

                # Specific flags for QSV encoders from the bat file
                if "qsv" in encoder:
                    command.insert(9, "-dual_gfx")
                    command.insert(10, "0")

                status = "succeeded" if _run_ffmpeg_command(command) else "failed"
                results[title][res_name] = status
                
                color_code = GREEN if status == "succeeded" else RED
                print(f"  {res_name}: {color_code}{status}{RESET}")

    return results

def _get_display_width(s):
    """
    Calculates the display width of a string, ignoring ANSI escape codes.
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return len(ansi_escape.sub('', s))

def _print_summary_table(results):
    """Prints a formatted summary table of all test results."""
    GREEN_CHECK = "\033[92m✓\033[0m"
    RED_X = "\033[91m×\033[0m"
    GRAY_DASH = "\033[90m—\033[0m"
    
    # Get column headers (resolutions) and row headers (decoder titles)
    resolutions = list(RESOLUTIONS.keys())
    
    # Use different headers for decoders and encoders
    decoder_titles = sorted([t for t in results.keys() if "Decoder" in t])
    encoder_titles = sorted([t for t in results.keys() if "Encoder" in t])

    # Calculate column widths based on display width
    res_width = max(len(res) for res in resolutions)
    row_header_width = max([_get_display_width(t) for t in results.keys()] + [20, _get_display_width("Decoder"), _get_display_width("Encoder")])
    
    # Print Decoder Table
    if decoder_titles:
        print("\n" + "-" * (row_header_width + 3 + (res_width + 3) * len(resolutions)))
        header_text = "Decoder"
        padding_left = (row_header_width - _get_display_width(header_text)) // 2
        padding_right = row_header_width - _get_display_width(header_text) - padding_left
        header_row = f"| {' ' * padding_left}{header_text}{' ' * padding_right} |"
        for res in resolutions:
            header_row += f" {res.center(res_width)} |"
        print(header_row)
        print("-" * (row_header_width + 3 + (res_width + 3) * len(resolutions)))
        
        for title in decoder_titles:
            padding_needed = row_header_width - _get_display_width(title)
            row_string = f"| {title}{' ' * padding_needed} |"
            for res in resolutions:
                status = results.get(title, {}).get(res, "skipped")
                symbol = GREEN_CHECK if status == "succeeded" else RED_X if status == "failed" else GRAY_DASH
                symbol_width = _get_display_width(symbol)
                padding_left = (res_width - symbol_width) // 2
                padding_right = res_width - symbol_width - padding_left
                row_string += f" {' ' * padding_left}{symbol}{' ' * padding_right} |"
            print(row_string)
        print("-" * (row_header_width + 3 + (res_width + 3) * len(resolutions)))

    # Print Encoder Table
    if encoder_titles:
        print("\n" + "-" * (row_header_width + 3 + (res_width + 3) * len(resolutions)))
        header_text = "Encoder"
        padding_left = (row_header_width - _get_display_width(header_text)) // 2
        padding_right = row_header_width - _get_display_width(header_text) - padding_left
        header_row = f"| {' ' * padding_left}{header_text}{' ' * padding_right} |"
        for res in resolutions:
            header_row += f" {res.center(res_width)} |"
        print(header_row)
        print("-" * (row_header_width + 3 + (res_width + 3) * len(resolutions)))
        
        for title in encoder_titles:
            padding_needed = row_header_width - _get_display_width(title)
            row_string = f"| {title}{' ' * padding_needed} |"
            for res in resolutions:
                status = results.get(title, {}).get(res, "skipped")
                symbol = GREEN_CHECK if status == "succeeded" else RED_X if status == "failed" else GRAY_DASH
                symbol_width = _get_display_width(symbol)
                padding_left = (res_width - symbol_width) // 2
                padding_right = res_width - symbol_width - padding_left
                row_string += f" {' ' * padding_left}{symbol}{' ' * padding_right} |"
            print(row_string)
        print("-" * (row_header_width + 3 + (res_width + 3) * len(resolutions)))


def run_all_tests():
    """Main function to run the entire test suite."""
    print("Starting hardware codec detection test suite...")

    if install_ffmpeg_if_needed() != 0:
        print("Error: FFmpeg dependency not met. Please check installation.", file=sys.stderr)
        return -1

    temp_dir = os.path.join(tempfile.gettempdir(), "HwCodecDetect")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    _generate_test_files(temp_dir)
    decoder_results = _run_decoder_tests(temp_dir)
    encoder_results = _run_encoder_tests(temp_dir)

    all_results = {}
    all_results.update(decoder_results)
    all_results.update(encoder_results)
    
    _print_summary_table(all_results)

    return all_results
    
if __name__ == "__main__":
    run_all_tests()