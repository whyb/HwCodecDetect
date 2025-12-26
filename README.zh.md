# FFmpeg 硬件编解码器检测脚本(HwCodecDetect)
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

在今天的编解码硬件加速的生态中，视频编解码技术面临着一个“百家争鸣”的局面。为了利用 GPU 的强大算力，各家硬件厂商都推出了自己的加速框架或编码器标准，例如 NVIDIA 的 NVEnc/NVDec、Intel 的 QSV 和 AMD 的 AMF。此外，操作系统层也提供了通用的接口，如微软的 Media Foundation 和 DXVA2 、 D3D12VA ，而开源社区则发展了跨平台的 VAAPI 和 Vulkan 等标准。

这种多样性虽然带来了技术上的进步，但也给普通用户和开发者带来了挑战。由于历史遗留和兼容性问题，一个硬件可能支持多种编码器，但它们在性能、支持的格式和分辨率方面都有所不同。因此，在使用 FFmpeg 进行硬件加速时，很难直观地知道哪种编码器最适合自己的设备。

本项目正是为了解决这一痛点而生。它是一个用于自动化检测系统硬件视频编码器功能的便捷工具。它利用 FFmpeg，通过生成不同分辨率（从 240p 到 8K）的单帧视频文件，并尝试使用各种硬件编码器进行处理，以此来快速判断哪些硬件编码器在您的系统上可用以及它们所支持的分辨率。

## 主要功能
### 编码器
脚本会自动检测并报告以下主流硬件编码器及其支持的格式：
| 编码器名称                     	        | 支持的视频编码格式                           |
|------------------------------------------|------------------------------------------- |
| NVEnc                          	       | H.264、H.265、AV1                          |
| QSV (Quick Sync Video)         	       | H.264、H.265、AV1、MJPEG、MPEG-2、VP9       |
| AMF (Advanced Media Framework)           | H.264、H.265、AV1                          |
| Media Foundation               	       | H.264、H.265                               |
| D3D12VA (Direct3D 12 Video Acceleration) | H.265                                      |
| VAAPI (Video Acceleration API) 	       | H.264、H.265、AV1、MJPEG、MPEG-2、VP8、VP9  |
| Vulkan                         	       | H.264、H.265                               |
| Apple VideoToolbox               	       | H.264、H.265                               |

### 解码器
脚本会自动检测并报告以下主流硬件解码器及其支持的格式：
| 编码器名称                                 | 支持的视频编码格式                                             |
|------------------------------------------	|------------------------------------------------------------- |
| NVDec (CUVID)                  	        | H.264、H.265、AV1、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8、VP9    |
| QSV (Quick Sync Video)         	        | H.264、H.265、AV1、MJPEG、MPEG-2、VP8、VP9                    |
| AMF (Advanced Media Framework)            | H.264、H.265、AV1                                            |
| DXVA2 (DirectX Video Acceleration)        | H.264、H.265、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8              |
| D3D11VA (Direct3D 11 Video Acceleration) 	| H.264、H.265、AV1、MJPEG、MPEG-1、MPEG-2、MPEG-4、VP8、VP9    |
| Vulkan                                  	| H.264、H.265、AV1                                            |
| Apple VideoToolbox                    	| H.264、H.265、MPEG-2、MPEG-4                                 |


## 如何使用
### 方式一：通过 PyPI 安装 (推荐)
如果您只需快速使用本工具，这是最简单的方式。
1. 安装：通过 pip 从 [PyPI 官方仓库](https://pypi.org/project/hwcodecdetect) 安装 hwcodecdetect。
    ```bash
    pip install hwcodecdetect
    ```

2. 运行：安装完成后，直接在命令行中运行 hwcodecdetect 命令。
    ```bash
    hwcodecdetect
    ```

### 方法二：下载并运行可执行文件 (独立运行)
如果您希望在不安装 Python 依赖的情况下运行该工具，或者 PyPI 安装失败，请使用此方法。

1. 下载：前往项目的 [**Releases 页面**](https://github.com/whyb/HwCodecDetect/releases)，下载与您的操作系统对应的可执行文件（例如：`HwCodecDetect-Linux-x64`、`HwCodecDetect-Windows-x64.exe`）。

2. （仅限 Linux/macOS）添加执行权限：如果您使用的是 Linux 或 macOS，您需要授予下载的文件执行权限。
    ```bash
    # 将 'HwCodecDetect-Linux-x64' 替换为实际下载的文件名
    chmod +x HwCodecDetect-Linux-x64
    ```

3. 运行：直接在终端中执行该文件。
    ```bash
    # 适用于 Linux/macOS
    ./HwCodecDetect-Linux-x64

    # 适用于 Windows (例如在 PowerShell 或命令提示符(cmd)中)
    .\HwCodecDetect-Windows-x64.exe
    ```

### 方式三：从源码本地安装
如果您从 GitHub 克隆了项目源码，并想在本地环境中运行，可以采用此方法。
1. 克隆仓库：首先，将项目源码克隆到本地。
    ```bash
    git clone https://github.com/whyb/HwCodecDetect.git ./HwCodecDetect
    ```
2. 安装依赖：进入项目根目录，通过 pip 安装项目所需的依赖。
    ```bash
    cd HwCodecDetect
    pip install .
    ```
3. 运行：安装完成后，直接在命令行中运行 hwcodecdetect 命令。
    ```bash
    hwcodecdetect
    ```

## 效果展示
下面是本地运行测试的可能的结果：
<video src="https://github.com/whyb/HwCodecDetect/blob/main/imgs/hwcodecdetect.mp4?raw=true" muted autoplay loop controls style="max-width: 100%;">
</video>

## Star增长记录
[![Star History Chart](https://api.star-history.com/svg?repos=whyb/HwCodecDetect&type=date&legend=top-left)](https://www.star-history.com/#whyb/HwCodecDetect&type=date&legend=top-left)