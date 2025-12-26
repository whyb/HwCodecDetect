# FFmpeg Hardware Codec Detect Script(HwCodecDetect)
<p align="center">
    <a href="https://github.com/whyb/HwCodecDetect/actions/workflows/run-test.yml">
        <img src="https://github.com/whyb/HwCodecDetect/actions/workflows/run-test.yml/badge.svg" />
    </a>
    <a href="https://pypi.org/project/hwcodecdetect">
        <img src="https://badgen.net/pypi/v/hwcodecdetect?color=yellow" />
    </a>
    <a href="https://pypi.org/project/hwcodecdetect">
        <img src="https://static.pepy.tech/badge/hwcodecdetect" />
    </a>
    <a href="https://deepwiki.com/whyb/HwCodecDetect">
        <img src="https://img.shields.io/badge/DeepWiki-whyb%2FHwCodecDetect-yellow.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAyCAYAAAAnWDnqAAAAAXNSR0IArs4c6QAAA05JREFUaEPtmUtyEzEQhtWTQyQLHNak2AB7ZnyXZMEjXMGeK/AIi+QuHrMnbChYY7MIh8g01fJoopFb0uhhEqqcbWTp06/uv1saEDv4O3n3dV60RfP947Mm9/SQc0ICFQgzfc4CYZoTPAswgSJCCUJUnAAoRHOAUOcATwbmVLWdGoH//PB8mnKqScAhsD0kYP3j/Yt5LPQe2KvcXmGvRHcDnpxfL2zOYJ1mFwrryWTz0advv1Ut4CJgf5uhDuDj5eUcAUoahrdY/56ebRWeraTjMt/00Sh3UDtjgHtQNHwcRGOC98BJEAEymycmYcWwOprTgcB6VZ5JK5TAJ+fXGLBm3FDAmn6oPPjR4rKCAoJCal2eAiQp2x0vxTPB3ALO2CRkwmDy5WohzBDwSEFKRwPbknEggCPB/imwrycgxX2NzoMCHhPkDwqYMr9tRcP5qNrMZHkVnOjRMWwLCcr8ohBVb1OMjxLwGCvjTikrsBOiA6fNyCrm8V1rP93iVPpwaE+gO0SsWmPiXB+jikdf6SizrT5qKasx5j8ABbHpFTx+vFXp9EnYQmLx02h1QTTrl6eDqxLnGjporxl3NL3agEvXdT0WmEost648sQOYAeJS9Q7bfUVoMGnjo4AZdUMQku50McDcMWcBPvr0SzbTAFDfvJqwLzgxwATnCgnp4wDl6Aa+Ax283gghmj+vj7feE2KBBRMW3FzOpLOADl0Isb5587h/U4gGvkt5v60Z1VLG8BhYjbzRwyQZemwAd6cCR5/XFWLYZRIMpX39AR0tjaGGiGzLVyhse5C9RKC6ai42ppWPKiBagOvaYk8lO7DajerabOZP46Lby5wKjw1HCRx7p9sVMOWGzb/vA1hwiWc6jm3MvQDTogQkiqIhJV0nBQBTU+3okKCFDy9WwferkHjtxib7t3xIUQtHxnIwtx4mpg26/HfwVNVDb4oI9RHmx5WGelRVlrtiw43zboCLaxv46AZeB3IlTkwouebTr1y2NjSpHz68WNFjHvupy3q8TFn3Hos2IAk4Ju5dCo8B3wP7VPr/FGaKiG+T+v+TQqIrOqMTL1VdWV1DdmcbO8KXBz6esmYWYKPwDL5b5FA1a0hwapHiom0r/cKaoqr+27/XcrS5UwSMbQAAAABJRU5ErkJggg==" />
    </a>
</p>

[中文版](https://github.com/whyb/HwCodecDetect/blob/main/README.zh.md)

Today's hardware-accelerated video codec landscape is a "field of a hundred schools of thought." To leverage the immense power of GPUs, hardware manufacturers have introduced their own acceleration frameworks and encoding standards, such as NVIDIA's NVEnc/NVDec, Intel's QSV, and AMD's AMF. Additionally, operating systems provide universal APIs like Microsoft's Media Foundation, DXVA2, and D3D12VA, while the open-source community has developed cross-platform standards like VAAPI and Vulkan.

While this diversity drives technological progress, it also presents a challenge for users and developers. Due to historical issues and compatibility quirks, a single piece of hardware might support multiple encoders, but they can differ significantly in performance, supported formats, and resolutions. As a result, when using FFmpeg for hardware acceleration, it's not always clear which encoder is best suited for a specific device.

This project was created to solve this very problem. It's a convenient tool for automatically detecting the hardware video encoder capabilities of your system. Using FFmpeg, it generates single-frame video files at various resolutions (from 240p to 8K) and attempts to process them with different hardware encoders. This allows it to quickly determine which hardware encoders are available on your system and what resolutions they support.

## Key Features
### Encoders
The script automatically detect and reports on the following major hardware encoders and their supported formats:
| Encoder Name                   	       | Supported Video Formats                   |
|------------------------------------------|------------------------------------------- |
| NVEnc                          	       | H.264、H.265、AV1                          |
| QSV (Quick Sync Video)         	       | H.264、H.265、AV1、MJPEG、MPEG-2、VP9       |
| AMF (Advanced Media Framework)           | H.264、H.265、AV1                          |
| Media Foundation               	       | H.264、H.265                               |
| D3D12VA (Direct3D 12 Video Acceleration) | H.265                                      |
| VAAPI (Video Acceleration API) 	       | H.264、H.265、AV1、MJPEG、MPEG-2、VP8、VP9  |
| Vulkan                         	       | H.264、H.265                               |
| Apple VideoToolbox               	       | H.264、H.265                               |

### Decoders
The script automatically detect and reports on the following major hardware decoders and their supported formats:
| Decoder Name                              | Supported Video Formats                                      |
|------------------------------------------	|------------------------------------------------------------- |
| NVDec (CUVID)                  	        | H.264、H.265、AV1、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8、VP9    |
| QSV (Quick Sync Video)         	        | H.264、H.265、AV1、MJPEG、MPEG-2、VP8、VP9                    |
| AMF (Advanced Media Framework)            | H.264、H.265、AV1                                            |
| DXVA2 (DirectX Video Acceleration)        | H.264、H.265、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8              |
| D3D11VA (Direct3D 11 Video Acceleration) 	| H.264、H.265、AV1、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8、VP9    |
| Vulkan                                  	| H.264、H.265、AV1                                            |
| Apple VideoToolbox                    	| H.264、H.265、MPEG-2、MPEG-4                                 |


## How to Use
You can install and use HwCodecDetect in two ways.
### Method 1: Install via PyPI (Recommended)
This is the easiest method if you just want to use the tool quickly.

1. Install: Use pip to install hwcodecdetect from the [official PyPI repository](https://pypi.org/project/hwcodecdetect).
    ```bash
    pip install hwcodecdetect
    ```

2. Run: After installation, run the hwcodecdetect command directly from your terminal.
    ```bash
    hwcodecdetect
    ```

### Method 2: Download and Run Executable (Standalone)
Use this method if you prefer to run the tool without installing Python dependencies, or if the PyPI installation fails.

1. Download: Go to the project's [**Releases page**](https://github.com/whyb/HwCodecDetect/releases) and download the executable file corresponding to your operating system (e.g., `HwCodecDetect-Linux-x64`, `HwCodecDetect-Windows-x64.exe`).

2. (Linux/macOS only) Add Execute Permission: If you are on Linux or macOS, you need to grant the downloaded file execute permission.
    ```bash
    # Replace 'HwCodecDetect-Linux-x64' with the actual downloaded filename
    chmod +x HwCodecDetect-Linux-x64
    ```

3. Run: Execute the file directly from your terminal.
    ```bash
    # For Linux/macOS
    ./HwCodecDetect-Linux-x64

    # For Windows (e.g., in PowerShell or Command Prompt)
    .\HwCodecDetect-Windows-x64.exe
    ```

### Method 3: Install from Source
Use this method if you have cloned the project source code from GitHub and want to run it locally.

1. Clone the repository: First, clone the project source code to your local machine.
    ```bash
    git clone https://github.com/whyb/HwCodecDetect.git ./HwCodecDetect
    ```

2. Install dependencies: Navigate into the project's root directory and use pip to install the required dependencies.
    ```bash
    cd HwCodecDetect
    pip install .
    ```

3. Run: After the installation is complete, run the hwcodecdetect command directly.
    ```bash
    hwcodecdetect
    ```

## Final effect
Here are some possible results from a local test run:
![test result](https://raw.githubusercontent.com/whyb/HwCodecDetect/main/imgs/hwcodecdetect.gif)

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=whyb/HwCodecDetect&type=date&legend=top-left)](https://www.star-history.com/#whyb/HwCodecDetect&type=date&legend=top-left)