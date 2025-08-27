# FFmpeg 硬件编解码器测试脚本(HwCodecDetect)
<p align="center">
    <a href="https://pypi.org/project/hwcodecdetect">
        <img src="https://badgen.net/pypi/v/hwcodecdetect?color=yellow" />
    </a>
    <a href="https://pypi.org/project/hwcodecdetect">
        <img src="https://static.pepy.tech/badge/hwcodecdetect" />
    </a>
</p>

在今天的编解码硬件加速的生态中，视频编解码技术面临着一个“百家争鸣”的局面。为了利用 GPU 的强大算力，各家硬件厂商都推出了自己的加速框架或编码器标准，例如 NVIDIA 的 NVEnc/NVDec、Intel 的 QSV 和 AMD 的 AMF。此外，操作系统层也提供了通用的接口，如微软的 Media Foundation 和 DXAV 、 D3D12VA ，而开源社区则发展了跨平台的 VAAPI 和 Vulkan 等标准。

这种多样性虽然带来了技术上的进步，但也给普通用户和开发者带来了挑战。由于历史遗留和兼容性问题，一个硬件可能支持多种编码器，但它们在性能、支持的格式和分辨率方面都有所不同。因此，在使用 FFmpeg 进行硬件加速时，很难直观地知道哪种编码器最适合自己的设备。

本项目正是为了解决这一痛点而生。它是一个用于自动化检测系统硬件视频编码器功能的便捷工具。它利用 FFmpeg，通过生成不同分辨率（从 240p 到 8K）的单帧视频文件，并尝试使用各种硬件编码器进行处理，以此来快速判断哪些硬件编码器在您的系统上可用以及它们所支持的分辨率。

## 主要功能
### 编码器
脚本会自动测试并报告以下主流硬件编码器及其支持的格式：
| 编码器名称                     	 | 支持的视频编码格式                           |
|-----------------------------------|------------------------------------------- |
| NVEnc                          	| H.264、H.265、AV1                          |
| QSV (Quick Sync Video)         	| H.264、H.265、AV1、MJPEG、MPEG-2、VP9       |
| AMF (Advanced Media Framework)    | H.264、H.265、AV1                          |
| Media Foundation               	| H.264、H.265                               |
| VAAPI (Video Acceleration API) 	| H.264、H.265、AV1、MJPEG、MPEG-2、VP8、VP9  |
| Vulkan                         	| H.264、H.265                               |

### 解码器
脚本会自动测试并报告以下主流硬件解码器及其支持的格式：
| 编码器名称                                 | 支持的视频编码格式                                             |
|------------------------------------------	|------------------------------------------------------------- |
| NVDec (CUVID)                  	        | H.264、H.265、AV1、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8、VP9    |
| QSV (Quick Sync Video)         	        | H.264、H.265、AV1、MJPEG、MPEG-2、VP8、VP9                    |
| AMF (Advanced Media Framework)            | H.264、H.265、AV1                                            |
| DXVA2 (DirectX Video Acceleration)        | H.264、H.265、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8              |
| D3D11VA (Direct3D 11 Video Acceleration) 	| H.264、H.265、AV1、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8、VP9    |


## 如何使用

### 1. 通过pypi安装
```bash
pip install HwCodecDetect
```

### 2. 运行测试
```bash
HwCodecDetect
```


## 效果展示
下面是本地运行测试的可能的结果：

![decoder test result](https://raw.githubusercontent.com/whyb/HwCodecDetect/main/imgs/decoder.png)

![encoder test result](https://raw.githubusercontent.com/whyb/HwCodecDetect/main/imgs/encoder.png)