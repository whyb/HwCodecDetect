import os
import re
import sys
import platform
import shutil
import argparse
from collections import defaultdict
from .install_ffmpeg_if_needed import install_ffmpeg_if_needed
from .bitdepth_chroma_detect import run_bitdepth_chroma_tests, print_bitdepth_chroma_results
from .codec_defs import RESOLUTIONS, DECODER_TITLES, ENCODER_TITLES, DECODERS, ENCODERS, ALL_CODECS
from .utils import (
    check_codec_support, get_stty_cfg, set_stty_cfg,
    run_ffmpeg_command, get_display_width, get_file_extension,
    prepare_temp_dir, print_codec_support_report, format_verbose_log,
    get_ffmpeg_path, set_ffmpeg_path,
)
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil library not found. Falling back to OS-specific methods.", file=sys.stderr)

init(autoreset=True)


def get_available_memory():
    # --- plan A. use psutil ---
    if PSUTIL_AVAILABLE:
        try:
            return psutil.virtual_memory().available
        except Exception as e:
            print(f"Error using psutil: {e}. Falling back...", file=sys.stderr)
            pass

    # --- plan B. OS-specific Fallback ---
    system = platform.system()

    if system == "Linux":
        # /proc/meminfo in Linux
        try:
            with open('/proc/meminfo', 'r') as f:
                content = f.read()
            # find MemAvailable:
            # Or MemFree + Buffers + Cached
            match = re.search(r'MemAvailable:\s+(\d+)\s+kB', content)
            if match:
                # MemAvailable: KB unit
                # int(match.group(1)) * 1024 convert to bytes
                return int(match.group(1)) * 1024

            # if not found MemAvailable, try MemFree
            match_free = re.search(r'MemFree:\s+(\d+)\s+kB', content)
            if match_free:
                return int(match_free.group(1)) * 1024
            return -1
        except Exception as e:
            print(f"Linux fallback failed: {e}", file=sys.stderr)
            return -1

    elif system == "Windows":
        # use wmic command in Windows
        try:
            # wmic OS Get FreePhysicalMemory /Value get result: KB unit
            result = subprocess.run(
                ['wmic', 'OS', 'Get', 'FreePhysicalMemory', '/Value'],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            # 'FreePhysicalMemory=XXXXXX\r\n'
            match = re.search(r'FreePhysicalMemory=(\d+)', result.stdout)

            if match:
                # FreePhysicalMemory KB unit
                # int(match.group(1)) * 1024 convert to bytes
                return int(match.group(1)) * 1024
            return -1

        except Exception as e:
            print(f"Windows fallback failed: {e}", file=sys.stderr)
            return -1

    elif system in ["Darwin", "FreeBSD"]: # macOS (Darwin) or FreeBSD
        # use sysctl command in macOS/BSD
        try:
            # sysctl vm.stats.vm.v_free_count (page_size * v_free_count)
            page_size = os.sysconf('SC_PAGE_SIZE')

            result = subprocess.run(
                ['sysctl', '-n', 'vm.stats.vm.v_free_count'],
                capture_output=True,
                text=True,
                check=True
            )
            free_pages = int(result.stdout.strip())

            return free_pages * page_size
        except Exception as e:
            print(f"macOS/BSD fallback failed: {e}", file=sys.stderr)
            return -1
    else:
        # others OS(Solaris, AIX, etc...)
        print(f"Unsupported OS for fallback: {system}", file=sys.stderr)
        return -1


# Set the number of concurrent processes/threads for encoding and decoding
CONCURRENT_ENCODER_COUNT = 8
CONCURRENT_DECODER_COUNT = 16
available_memory = get_available_memory()
available_memory_mb = available_memory / (1024 * 1024)
#print(f"Current available system memory is {available_memory_mb:.2f} MB.")
if available_memory > 0:
    # Estimate based on available memory (assume each ffmpeg's process needs 256MB)
    CONCURRENT_ENCODER_COUNT = max(1, available_memory_mb // 256)
    CONCURRENT_DECODER_COUNT = max(1, available_memory_mb // 256)
    CONCURRENT_ENCODER_COUNT = min(CONCURRENT_ENCODER_COUNT, 8)
    CONCURRENT_DECODER_COUNT = min(CONCURRENT_DECODER_COUNT, 8)


def _run_encoder_test_single(test_data):
    """Runs a single encoder test and returns the result."""
    codec, encoder, res_name, res_size, test_dir, verbose, unsupported_encoders, colorful = test_data

    # Skip unsupported encoders
    if encoder in unsupported_encoders:
        title = ENCODER_TITLES.get((encoder, codec), f"{encoder.upper()} Encoder:")
        return title, res_name, "skipped"

    ffmpeg = get_ffmpeg_path()
    file_ext = get_file_extension(codec)
    output_file = os.path.join(test_dir, f"{encoder}_{res_name}{file_ext}")
    if "vulkan" in encoder:
        command = [
            ffmpeg,
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
            ffmpeg,
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
            ffmpeg,
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

    if verbose: # if verbose then replace loglevel to verbose
        command[2] = "error"

    success, stdout, stderr = run_ffmpeg_command(command, verbose)
    status = "succeeded" if success else "failed"

    # If encoding failed, clean up the output file so decoder tests don't try to use a corrupt file
    if not success and os.path.exists(output_file):
        try:
            os.remove(output_file)
        except OSError:
            pass

    if verbose:
        format_verbose_log("Encoder Detect Info", codec, f"encoder: {encoder}", res_size, status, stdout, stderr, command, colorful)

    title = ENCODER_TITLES.get((encoder, codec), f"{encoder.upper()} Encoder:")
    return title, res_name, status


def _run_encoder_tests(test_dir, max_workers, verbose, unsupported_encoders=None, colorful=False):
    """Runs hardware encoder tests using a thread pool."""
    results = defaultdict(dict)

    if unsupported_encoders is None:
        unsupported_encoders = set()

    if colorful:
        from .utils import COLORFUL as C
        print(f"\n{C.ACCENT}{C.BOLD}━━━ Running Encoder Tests ━━━{C.RESET}")
    else:
        print("\n--- Running Encoder Tests ---")

    tasks = []
    for codec, info in ENCODERS.items():
        for encoder in info['hw_encoders']:
            for res_name, res_size in RESOLUTIONS.items():
                tasks.append((codec, encoder, res_name, res_size, test_dir, verbose, unsupported_encoders, colorful))

    stty_cfg = get_stty_cfg()
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_run_encoder_test_single, task) for task in tasks]

            tqdm_kwargs = {"desc": "Running encoder tests"}
            if colorful:
                tqdm_kwargs["colour"] = "green"
            for future in tqdm(as_completed(futures), total=len(tasks), **tqdm_kwargs):
                title, res_name, status = future.result()
                results[title][res_name] = status
    finally:
        set_stty_cfg(stty_cfg)

    return results

def _run_decoder_test_single(test_data):
    """Runs a single decoder test and returns the result."""
    codec, hw_decoder, res_name, res_size, test_dir, verbose, unsupported_decoders, colorful = test_data

    # Skip unsupported decoders
    if hw_decoder in unsupported_decoders:
        title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
        return title, res_name, "skipped"

    ffmpeg = get_ffmpeg_path()
    file_ext = get_file_extension(codec)
    test_file_path = os.path.join(test_dir, f"{codec}_{res_name}{file_ext}")

    found_file = False
    for filename in os.listdir(test_dir):
        if filename.startswith(f"{codec}_") and f"_{res_name}" in filename:
            candidate_path = os.path.join(test_dir, filename)
            # Ensure the file is valid (at least has some content)
            if os.path.exists(candidate_path) and os.path.getsize(candidate_path) > 0:
                test_file_path = candidate_path
                found_file = True
                break

    if not found_file:
        cpu_lib = ALL_CODECS[codec]["lib"]
        command = [
            ffmpeg, "-loglevel", "quiet", "-hide_banner", "-y",
            "-f", "lavfi", "-i", f"color=white:s={res_size}:d=1",
            "-frames:v", "1", "-c:v", cpu_lib, "-pixel_format", "yuv420p",
            test_file_path,
        ]
        if not run_ffmpeg_command(command, verbose)[0]:
            title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
            return title, res_name, "skipped"

    if "vulkan" in hw_decoder:
        command = [
            ffmpeg, "-loglevel", "quiet", "-hide_banner", "-y",
            "-init_hw_device", "vulkan=vk:0",
            "-hwaccel", "vulkan",
            "-hwaccel_output_format", "vulkan",
            "-i", test_file_path,
            "-f", "null", "null",
        ]
    elif "videotoolbox" in hw_decoder:
        command = [
            ffmpeg, "-loglevel", "quiet", "-hide_banner", "-y",
            "-hwaccel", "videotoolbox",
            "-i", test_file_path,
            "-f", "null", "null",
        ]
    elif hw_decoder in ["dxva2", "d3d11va", "d3d12va"] and codec in ["h264", "h265", "vp8", "vp9", "av1", "mjpeg", "mpeg1", "mpeg2", "mpeg4"]:
        command = [
            ffmpeg, "-loglevel", "quiet", "-hide_banner", "-y",
            "-hwaccel", hw_decoder, "-i", test_file_path,
            "-c:v", "libx264", "-preset", "ultrafast",
            "-f", "null", "null",
        ]
    else:
        command = [
            ffmpeg, "-loglevel", "quiet", "-hide_banner", "-y",
            "-c:v", hw_decoder, "-i", test_file_path,
            "-c:v", "libx264", "-preset", "ultrafast",
            "-f", "null", "null",
        ]

    if verbose: # if verbose then replace loglevel to verbose
        command[2] = "error"

    success, stdout, stderr = run_ffmpeg_command(command, verbose)
    status = "succeeded" if success else "failed"

    if verbose:
        format_verbose_log("Decoder Detect Info", codec, f"decoder: {hw_decoder}", res_size, status, stdout, stderr, command, colorful)

    title = DECODER_TITLES.get((hw_decoder, codec), f"{hw_decoder.upper()} Decoder:")
    return title, res_name, status


def _run_decoder_tests(test_dir, max_workers, verbose, unsupported_decoders=None, colorful=False):
    """Runs hardware decoder tests using a thread pool."""
    results = defaultdict(dict)

    if unsupported_decoders is None:
        unsupported_decoders = set()

    if colorful:
        from .utils import COLORFUL as C
        print(f"\n{C.ACCENT}{C.BOLD}━━━ Running Decoder Tests ━━━{C.RESET}")
    else:
        print("\n--- Running Decoder Tests ---")

    tasks = []
    for codec, info in DECODERS.items():
        for hw_decoder in info['hw_decoders']:
            for res_name, res_size in RESOLUTIONS.items():
                tasks.append((codec, hw_decoder, res_name, res_size, test_dir, verbose, unsupported_decoders, colorful))

    stty_cfg = get_stty_cfg()
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(_run_decoder_test_single, task) for task in tasks]

            tqdm_kwargs = {"desc": "Running decoder tests"}
            if colorful:
                tqdm_kwargs["colour"] = "cyan"
            for future in tqdm(as_completed(futures), total=len(tasks), **tqdm_kwargs):
                title, res_name, status = future.result()
                results[title][res_name] = status
    finally:
        set_stty_cfg(stty_cfg)

    return results

def _print_summary_table(results, colorful=False):
    """Prints a formatted summary table of all test results."""
    if colorful:
        from .utils import COLORFUL as C

    GREEN_CHECK = Fore.GREEN + "✓" + Style.RESET_ALL
    RED_X = Fore.RED + "×" + Style.RESET_ALL
    GRAY_DASH = Fore.LIGHTBLACK_EX + "—" + Style.RESET_ALL

    resolutions = list(RESOLUTIONS.keys())

    decoder_titles = sorted([t for t in results.keys() if "Decoder" in t])
    encoder_titles = sorted([t for t in results.keys() if "Encoder" in t])

    res_width = max(len(res) for res in resolutions)
    row_header_width = max([get_display_width(t) for t in results.keys()] + [20, get_display_width("Decoder"), get_display_width("Encoder")])

    def _print_table(titles, header_text):
        if not titles:
            return
        if colorful:
            _print_colorful_table(results, titles, header_text, resolutions, res_width, row_header_width, C)
        else:
            _print_plain_table(results, titles, header_text, resolutions, res_width, row_header_width)

    _print_table(decoder_titles, "Decoder")
    _print_table(encoder_titles, "Encoder")


def _print_plain_table(results, titles, header_text, resolutions, res_width, row_header_width):
    """Prints the original plain ASCII table."""
    GREEN_CHECK = Fore.GREEN + "✓" + Style.RESET_ALL
    RED_X = Fore.RED + "×" + Style.RESET_ALL
    GRAY_DASH = Fore.LIGHTBLACK_EX + "—" + Style.RESET_ALL

    print("\n" + "=" * (row_header_width + 4 + (res_width + 3) * len(resolutions)))
    padding_left = (row_header_width - get_display_width(header_text)) // 2
    padding_right = row_header_width - get_display_width(header_text) - padding_left
    header_row = f"| {' ' * padding_left}{header_text}{' ' * padding_right} |"
    line_row = f"|-{'-' * row_header_width}-|"
    for res in resolutions:
        header_row += f" {res.center(res_width)} |"
        line_row += f"-{'-' * res_width}-|"
    print(header_row)
    print(line_row)

    for title in titles:
        padding_needed = row_header_width - get_display_width(title)
        row_string = f"| {title}{' ' * padding_needed} |"
        for res in resolutions:
            status = results.get(title, {}).get(res, "skipped")
            symbol = GREEN_CHECK if status == "succeeded" else RED_X if status == "failed" else GRAY_DASH
            symbol_width = get_display_width(symbol)
            padding_left = (res_width - symbol_width) // 2
            padding_right = res_width - symbol_width - padding_left
            row_string += f" {' ' * padding_left}{symbol}{' ' * padding_right} |"
        print(row_string)
    print("=" * (row_header_width + 4 + (res_width + 3) * len(resolutions)))


def _print_colorful_table(results, titles, header_text, resolutions, res_width, row_header_width, C):
    """Prints a colorful box-drawing table with GUI-like status colors."""
    # Status symbols (no emoji, GUI-like colored labels)
    def _status_cell(status):
        if status == "succeeded":
            return C.SUCCESS + C.BOLD + C.SYM_SUCCESS + C.RESET
        elif status == "failed":
            return C.ERROR + C.BOLD + C.SYM_ERROR + C.RESET
        else:
            return C.DIM + C.SYM_SKIP + C.RESET

    total_width = row_header_width + 4 + (res_width + 3) * len(resolutions)

    # Top border: ┌──────┬──────┐
    top = C.BORDER + C.TL + C.H * (row_header_width + 2)
    for res in resolutions:
        top += C.TT + C.H * (res_width + 2)
    top += C.TR + C.RESET
    print("\n" + top)

    # Header row
    padding_left = (row_header_width - get_display_width(header_text)) // 2
    padding_right = row_header_width - get_display_width(header_text) - padding_left
    header_row = f"{C.BORDER}{C.V}{C.RESET} {C.ACCENT}{C.BOLD}{' ' * padding_left}{header_text}{' ' * padding_right}{C.RESET} "
    for res in resolutions:
        header_row += f"{C.BORDER}{C.V}{C.RESET} {C.TEXT_SECONDARY}{res.center(res_width)}{C.RESET} "
    header_row += f"{C.BORDER}{C.V}{C.RESET}"
    print(header_row)

    # Separator: ├──────┼──────┤
    sep = C.BORDER + C.LT + C.H * (row_header_width + 2)
    for i, res in enumerate(resolutions):
        sep += C.XX + C.H * (res_width + 2)
    sep += C.RT + C.RESET
    print(sep)

    # Data rows
    for title in titles:
        padding_needed = row_header_width - get_display_width(title)
        row_string = f"{C.BORDER}{C.V}{C.RESET} {C.TEXT_PRIMARY}{title}{' ' * padding_needed} "
        for res in resolutions:
            status = results.get(title, {}).get(res, "skipped")
            cell = _status_cell(status)
            cell_width = get_display_width(cell)
            pad_l = (res_width - cell_width) // 2
            pad_r = res_width - cell_width - pad_l
            row_string += f"{C.BORDER}{C.V}{C.RESET} {' ' * pad_l}{cell}{' ' * pad_r} "
        row_string += f"{C.BORDER}{C.V}{C.RESET}"
        print(row_string)

    # Bottom border: └──────┴──────┘
    bot = C.BORDER + C.BL + C.H * (row_header_width + 2)
    for res in resolutions:
        bot += C.BT + C.H * (res_width + 2)
    bot += C.BR + C.RESET
    print(bot)

    # Legend
    print(f"  {C.SUCCESS}{C.BOLD} ● {C.RESET} Supported    {C.ERROR}{C.BOLD} ● {C.RESET} Not supported    {C.DIM} — {C.RESET} Skipped / Unavailable")


def run_all_tests(args):
    """Main function to run the entire test suite."""
    colorful = getattr(args, 'colorful', False)

    if colorful:
        from .utils import COLORFUL as C
        print(f"\n{C.ACCENT}{C.BOLD}╔══════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.ACCENT}{C.BOLD}║   HwCodecDetect — Hardware Codec Detection       ║{C.RESET}")
        print(f"{C.ACCENT}{C.BOLD}╚══════════════════════════════════════════════════╝{C.RESET}")
    else:
        print("Starting hardware codec detection test suite...")

    # Skip auto-install when a custom ffmpeg path is explicitly provided
    if not getattr(args, 'ffmpeg_path', None):
        if install_ffmpeg_if_needed() != 0:
            print("Error: FFmpeg dependency not met. Please check installation.", file=sys.stderr)
            return -1

    # Check codec support before running tests
    if colorful:
        print(f"\n{C.CYAN}{C.BOLD}▶ Checking FFmpeg codec support...{C.RESET}")
    else:
        print("\nChecking FFmpeg codec support...")
    unsupported_encoders, unsupported_decoders = check_codec_support(ENCODERS, DECODERS, colorful)
    print_codec_support_report(unsupported_encoders, unsupported_decoders, colorful)

    temp_dir = prepare_temp_dir("cli")

    encoder_results = _run_encoder_tests(temp_dir, args.encoder_count, args.verbose, unsupported_encoders, colorful)
    decoder_results = _run_decoder_tests(temp_dir, args.decoder_count, args.verbose, unsupported_decoders, colorful)

    all_results = {}
    all_results.update(encoder_results)
    all_results.update(decoder_results)

    _print_summary_table(all_results, colorful)

    # Run bit-depth and chroma tests if enabled
    if getattr(args, 'bitdepth_chroma', True):
        if colorful:
            print(f"\n{C.BORDER}{'━' * 60}{C.RESET}")
            print(f"{C.PURPLE}{C.BOLD}▶ Bit-depth and Chroma Subsampling Detection{C.RESET}")
            print(f"{C.BORDER}{'━' * 60}{C.RESET}")
        else:
            print("\n" + "=" * 60)
            print("Starting Bit-depth and Chroma Subsampling Detection...")
            print("=" * 60)
        bd_encoder_results, bd_decoder_results = run_bitdepth_chroma_tests(
            args.encoder_count, args.decoder_count, args.verbose, colorful
        )
        print_bitdepth_chroma_results(bd_encoder_results, bd_decoder_results, colorful)

    if colorful:
        print(f"\n{C.DIM}▶ Cleaning up temporary files...{C.RESET}")
    else:
        print("\nCleaning up temporary files...")
    shutil.rmtree(temp_dir)
    if colorful:
        print(f"{C.SUCCESS}✔ Cleanup complete.{C.RESET}")
    else:
        print("Cleanup complete.")

    return


def main():
    """Parses arguments and runs the test suite."""

    # Ensure stdout/stderr use UTF-8 on Windows to avoid UnicodeEncodeError
    # when printing Unicode characters (✓/×/—) to GBK/CP936 consoles.
    if sys.platform == "win32":
        for stream_name in ("stdout", "stderr"):
            stream = getattr(sys, stream_name, None)
            if stream is not None and hasattr(stream, "reconfigure"):
                try:
                    stream.reconfigure(encoding="utf-8", errors="replace")
                except Exception:
                    pass

    help_text = """
    This tool automatically detects the hardware video codec capabilities of your system.
    Using FFmpeg, it tests various hardware codecs (like NVEnc, QSV, and VAAPI etc.)
    by generating and processing video files at different resolutions (from 240p to 8K).

    The result is a convenient summary table showing which hardware codecs are
    available on your system and what resolutions they support.

    Author: whyb
    GitHub repository: https://github.com/whyb/HwCodecDetect
    Author contact: whyber@outlook.com
    """

    parser = argparse.ArgumentParser(description="""
    A tool to detect hardware video encoder and decoder capabilities.
    """ + help_text, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "-ec", "--encoder-count",
        type=int,
        default=CONCURRENT_ENCODER_COUNT,
        help=f"Set the number of multi-process concurrent encoder testing. (default: {CONCURRENT_ENCODER_COUNT}) "
             f"\nNote: NVIDIA RTX cards driver have limit of 8 concurrent encodes."
    )

    parser.add_argument(
        "-dc", "--decoder-count",
        type=int,
        default=CONCURRENT_DECODER_COUNT,
        help=f"Set the number of multi-process concurrent decoder testing. (default: {CONCURRENT_DECODER_COUNT})"
    )

    try:
        from importlib.metadata import version
        version_str = version("HwCodecDetect")
    except Exception:
        try:
            from . import __version__ as version_str
        except Exception:
            version_str = "Unknown"

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"HwCodecDetect v{version_str}",
        help="Show program's version number and exit."
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed information for each test'
    )

    parser.add_argument(
        '--no-bitdepth-chroma',
        action='store_true',
        dest='no_bitdepth_chroma',
        help='Disable bit-depth and chroma subsampling detection (enabled by default)'
    )

    parser.add_argument(
        '--ui', '-ui',
        action='store_true',
        default=False,
        help='Launch the graphical user interface (default: CLI mode)'
    )

    parser.add_argument(
        '--colorful',
        action='store_true',
        default=False,
        help='Enable colorful ASCII art style output for CLI mode (ignored when --ui is enabled)'
    )

    parser.add_argument(
        '--ffmpeg-path',
        type=str,
        default=None,
        help='Absolute path to the FFmpeg executable to use for all tests.\n'
             'Overrides FFMPEG_PATH env var and PATH lookup.\n'
             'If not set, falls back to FFMPEG_PATH env var, then PATH.'
    )

    args = parser.parse_args()
    # Set bitdepth_chroma to True unless --no-bitdepth-chroma is specified
    args.bitdepth_chroma = not args.no_bitdepth_chroma

    # Apply custom ffmpeg path (highest priority)
    if args.ffmpeg_path:
        set_ffmpeg_path(args.ffmpeg_path)

    # Check --ui flag OR environment variable (for CI GUI builds)
    if args.ui or os.environ.get("HWCODECDETECT_GUI") == "1":
        from .gui import launch_gui
        launch_gui(args)
        return

    run_all_tests(args)

if __name__ == "__main__":
    main()
