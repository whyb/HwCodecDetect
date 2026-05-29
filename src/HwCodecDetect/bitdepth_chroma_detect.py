"""
Bit-depth and Chroma Subsampling Detection Module
This module tests hardware codec support for different pixel formats.
"""
import os
import sys
from collections import defaultdict
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from .codec_defs import (
    BITDEPTH_CHROMA_RESOLUTION,
    PIXEL_FORMATS,
    ENCODER_TITLES,
    DECODER_TITLES,
    ENCODERS,
    DECODERS,
)
from .utils import (
    check_codec_support,
    get_stty_cfg,
    set_stty_cfg,
    run_ffmpeg_command,
    get_display_width,
    get_file_extension,
    get_out_pix_fmt,
    prepare_temp_dir,
    print_codec_support_report,
    format_verbose_log,
)

init(autoreset=True)


def _run_encoder_bitdepth_test(test_data):
    """Tests encoder support for a specific pixel format."""
    codec, encoder, pix_fmt, bit_depth, chroma, test_dir, verbose, unsupported_encoders = test_data

    # Skip unsupported encoders
    if encoder in unsupported_encoders:
        title = ENCODER_TITLES.get((encoder, codec), f"{encoder.upper()} Encoder:")
        return title, pix_fmt, bit_depth, chroma, "skipped"

    file_ext = get_file_extension(codec)
    output_file = os.path.join(test_dir, f"{encoder}_{pix_fmt}{file_ext}")

    out_pix_fmt = get_out_pix_fmt(bit_depth, chroma)

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

    success, stdout, stderr = run_ffmpeg_command(command, verbose)
    status = "succeeded" if success else "failed"

    # Clean up on failure
    if not success and os.path.exists(output_file):
        try:
            os.remove(output_file)
        except OSError:
            pass

    if verbose:
        format_verbose_log("Bit-depth/Chroma Encoder Test", codec, f"encoder: {encoder}", pix_fmt, status, stdout, stderr, command)

    title = ENCODER_TITLES.get((encoder, codec), f"{encoder.upper()} Encoder:")
    return title, pix_fmt, bit_depth, chroma, status


def _run_encoder_bitdepth_tests(test_dir, max_workers, verbose, unsupported_encoders=None):
    """Tests encoder support for various pixel formats."""
    results = defaultdict(dict)

    if unsupported_encoders is None:
        unsupported_encoders = set()

    print("\n--- Running Bit-depth/Chroma Encoder Tests ---")

    tasks = []
    for codec, info in ENCODERS.items():
        for encoder in info['hw_encoders']:
            for pix_fmt, bit_depth, chroma, desc in PIXEL_FORMATS:
                tasks.append((codec, encoder, pix_fmt, bit_depth, chroma, test_dir, verbose, unsupported_encoders))

    stty_cfg = get_stty_cfg()
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_run_encoder_bitdepth_test, task) for task in tasks]

            for future in tqdm(as_completed(futures), total=len(tasks), desc="Running encoder bit-depth tests"):
                title, pix_fmt, bit_depth, chroma, status = future.result()
                key = f"{bit_depth}-bit {chroma}"
                if title not in results:
                    results[title] = {}
                results[title][key] = status
    finally:
        set_stty_cfg(stty_cfg)

    return results


def _run_decoder_bitdepth_test(test_data):
    """Tests decoder support for a specific pixel format."""
    codec, hw_decoder, pix_fmt, bit_depth, chroma, test_dir, verbose, unsupported_decoders = test_data

    # Skip unsupported decoders
    if hw_decoder in unsupported_decoders:
        title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
        return title, pix_fmt, bit_depth, chroma, "skipped"

    file_ext = get_file_extension(codec)
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
        if not run_ffmpeg_command(command, verbose)[0]:
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
    elif hw_decoder in ["dxva2", "d3d11va", "d3d12va"]:
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

    success, stdout, stderr = run_ffmpeg_command(command, verbose)
    status = "succeeded" if success else "failed"

    if verbose:
        format_verbose_log("Bit-depth/Chroma Decoder Test", codec, f"decoder: {hw_decoder}", pix_fmt, status, stdout, stderr, command)

    title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
    return title, pix_fmt, bit_depth, chroma, status


def _run_decoder_bitdepth_tests(test_dir, max_workers, verbose, unsupported_decoders=None):
    """Tests decoder support for various pixel formats."""
    results = defaultdict(dict)

    if unsupported_decoders is None:
        unsupported_decoders = set()

    print("\n--- Running Bit-depth/Chroma Decoder Tests ---")

    tasks = []
    for codec, info in DECODERS.items():
        for hw_decoder in info['hw_decoders']:
            for pix_fmt, bit_depth, chroma, desc in PIXEL_FORMATS:
                tasks.append((codec, hw_decoder, pix_fmt, bit_depth, chroma, test_dir, verbose, unsupported_decoders))

    stty_cfg = get_stty_cfg()
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_run_decoder_bitdepth_test, task) for task in tasks]
            for future in tqdm(as_completed(futures), total=len(tasks), desc="Running decoder bit-depth tests"):
                title, pix_fmt, bit_depth, chroma, status = future.result()
                key = f"{bit_depth}-bit {chroma}"
                if title not in results:
                    results[title] = {}
                results[title][key] = status
    finally:
        set_stty_cfg(stty_cfg)

    return results


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
    row_header_width = max([get_display_width(t) for t in titles] + [20, get_display_width(table_type)])

    print("\n" + "=" * (row_header_width + 4 + (col_width + 3) * len(format_columns)))
    header_text = f"Bit-depth/Chroma {table_type} Support"
    padding_left = (row_header_width - get_display_width(header_text)) // 2
    padding_right = row_header_width - get_display_width(header_text) - padding_left
    header_row = f"| {' ' * padding_left}{header_text}{' ' * padding_right} |"
    line_row = f"|-{'-' * row_header_width}-|"
    for col in format_columns:
        header_row += f" {col.center(col_width)} |"
        line_row += f"-{'-' * col_width}-|"
    print(header_row)
    print(line_row)

    for title in titles:
        padding_needed = row_header_width - get_display_width(title)
        row_string = f"| {title}{' ' * padding_needed} |"
        for col in format_columns:
            status = results.get(title, {}).get(col, "skipped")
            symbol = GREEN_CHECK if status == "succeeded" else RED_X if status == "failed" else GRAY_DASH
            symbol_width = get_display_width(symbol)
            padding_left = (col_width - symbol_width) // 2
            padding_right = col_width - symbol_width - padding_left
            row_string += f" {' ' * padding_left}{symbol}{' ' * padding_right} |"
        print(row_string)
    print("=" * (row_header_width + 4 + (col_width + 3) * len(format_columns)))


def run_bitdepth_chroma_tests(encoder_count, decoder_count, verbose):
    """Run all bit-depth and chroma tests and return results."""
    import shutil
    temp_dir = prepare_temp_dir("BitDepth")

    # Check codec support before running tests
    print("\nChecking FFmpeg codec support for bit-depth/chroma tests...")
    unsupported_encoders, unsupported_decoders = check_codec_support(ENCODERS, DECODERS)
    print_codec_support_report(unsupported_encoders, unsupported_decoders)

    encoder_results = _run_encoder_bitdepth_tests(temp_dir, encoder_count, verbose, unsupported_encoders)
    decoder_results = _run_decoder_bitdepth_tests(temp_dir, decoder_count, verbose, unsupported_decoders)

    # Clean up
    shutil.rmtree(temp_dir)

    return encoder_results, decoder_results


def print_bitdepth_chroma_results(encoder_results, decoder_results):
    """Print bit-depth and chroma test results."""
    if decoder_results:
        _print_bitdepth_chroma_table(decoder_results, "Decoder")
    if encoder_results:
        _print_bitdepth_chroma_table(encoder_results, "Encoder")
