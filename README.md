# FFmpeg Hardware Codec Test Script(HwCodecDetect)
<p align="center">
    <a href="https://pypi.org/project/hwcodecdetect">
        <img src="https://badgen.net/pypi/v/hwcodecdetect?color=yellow" />
    </a>
    <a href="https://pypi.org/project/hwcodecdetect">
        <img src="https://static.pepy.tech/badge/hwcodecdetect" />
    </a>
</p>

[中文版](https://github.com/whyb/HwCodecDetect/blob/main/README.zh.md)

Today's hardware-accelerated video codec landscape is a "field of a hundred schools of thought." To leverage the immense power of GPUs, hardware manufacturers have introduced their own acceleration frameworks and encoding standards, such as NVIDIA's NVEnc/NVDec, Intel's QSV, and AMD's AMF. Additionally, operating systems provide universal APIs like Microsoft's Media Foundation, DXVA, and D3D12VA, while the open-source community has developed cross-platform standards like VAAPI and Vulkan.

While this diversity drives technological progress, it also presents a challenge for users and developers. Due to historical issues and compatibility quirks, a single piece of hardware might support multiple encoders, but they can differ significantly in performance, supported formats, and resolutions. As a result, when using FFmpeg for hardware acceleration, it's not always clear which encoder is best suited for a specific device.

This project was created to solve this very problem. It's a convenient tool for automatically detecting the hardware video encoder capabilities of your system. Using FFmpeg, it generates single-frame video files at various resolutions (from 240p to 8K) and attempts to process them with different hardware encoders. This allows it to quickly determine which hardware encoders are available on your system and what resolutions they support.

## Key Features
### Encoders
The script automatically tests and reports on the following major hardware encoders and their supported formats:
| Encoder Name                   	 | Supported Video Formats                   |
|-----------------------------------|------------------------------------------- |
| NVEnc                          	| H.264、H.265、AV1                          |
| QSV (Quick Sync Video)         	| H.264、H.265、AV1、MJPEG、MPEG-2、VP9       |
| AMF (Advanced Media Framework)    | H.264、H.265、AV1                          |
| Media Foundation               	| H.264、H.265                               |
| VAAPI (Video Acceleration API) 	| H.264、H.265、AV1、MJPEG、MPEG-2、VP8、VP9  |
| Vulkan                         	| H.264、H.265                               |

### Decoders
The script automatically tests and reports on the following major hardware decoders and their supported formats:
| Decoder Name                              | Supported Video Formats                                      |
|------------------------------------------	|------------------------------------------------------------- |
| NVDec (CUVID)                  	        | H.264、H.265、AV1、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8、VP9    |
| QSV (Quick Sync Video)         	        | H.264、H.265、AV1、MJPEG、MPEG-2、VP8、VP9                    |
| AMF (Advanced Media Framework)            | H.264、H.265、AV1                                            |
| DXVA2 (DirectX Video Acceleration)        | H.264、H.265、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8              |
| D3D11VA (Direct3D 11 Video Acceleration) 	| H.264、H.265、AV1、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8、VP9    |


## How to Use

### 1. Install via PyPI
```bash
pip install HwCodecDetect
```

### 2. Run the Test
```bash
HwCodecDetect
```


## Demo
Here are some possible results from a local test run:
![decoder test result](https://raw.githubusercontent.com/whyb/HwCodecDetect/main/imgs/decoder.png)

![encoder test result](https://raw.githubusercontent.com/whyb/HwCodecDetect/main/imgs/encoder.png)