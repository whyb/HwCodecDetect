# FFmpeg 硬件编解码器测试脚本
在今天的编解码硬件加速的生态中，视频编解码技术面临着一个“百家争鸣”的局面。为了利用 GPU 的强大算力，各家硬件厂商都推出了自己的加速框架或编码器标准，例如 NVIDIA 的 NVEnc/NVDec、Intel 的 QSV 和 AMD 的 AMF。此外，操作系统层也提供了通用的接口，如微软的 Media Foundation 和 DXAV 、 D3D12VA ，而开源社区则发展了跨平台的 VAAPI 和 Vulkan 等标准。

这种多样性虽然带来了技术上的进步，但也给普通用户和开发者带来了挑战。由于历史遗留和兼容性问题，一个硬件可能支持多种编码器，但它们在性能、支持的格式和分辨率方面都有所不同。因此，在使用 FFmpeg 进行硬件加速时，很难直观地知道哪种编码器最适合自己的设备。

本项目正是为了解决这一痛点而生。它是一个用于自动化检测系统硬件视频编码器功能的便捷工具。它利用 FFmpeg，通过生成不同分辨率（从 240p 到 8K）的单帧视频文件，并尝试使用各种硬件编码器进行处理，以此来快速判断哪些硬件编码器在您的系统上可用以及它们所支持的分辨率。

## 主要功能
### 编码器
本脚本会自动测试并报告以下主流硬件编码器及其支持的格式：
| 编码器名称                     	| 支持的视频格式                               |
|--------------------------------	|------------------------------------------- |
| NVEnc                          	| H.264、H.265、AV1                          |
| QSV (Quick Sync Video)         	| H.264、H.265、AV1、MJPEG、MPEG-2、VP9       |
| AMF (Advanced Media Framework)    | H.264、H.265、AV1                          |
| Media Foundation               	| H.264、H.265                               |
| VAAPI (Video Acceleration API) 	| H.264、H.265、AV1、MJPEG、MPEG-2、VP8、VP9  |
| Vulkan                         	| H.264、H.265                               |

### 解码器
TODO

## 如何使用

* 准备环境，确保您的系统已安装 FFmpeg。脚本会尝试调用名为 install_ffmpeg_if_needed.bat 的辅助脚本来安装 FFmpeg。
* 运行脚本，想要测试编码器则双击运行 encoder_test.bat，测试解码器则双击运行 decoder_test.bat
* 查看结果，脚本将自动运行一系列测试，并在命令行窗口中实时显示结果。成功的测试将以绿色文字显示 <font color="#16C606">succeeded</font>，失败的测试将以红色文字显示 <font color="#E74856">failed</font>。

脚本执行完毕后，将能清晰地看到您的系统支持哪些硬件编码器以及它们在不同分辨率下的表现。

## 效果展示
下面是作者本地运行测试的部分结果：

NVIDIA Hardware H264 Encoder(NVEnc):
<br/>&nbsp;<font color="#16C606">240p succeeded</font>
<br/>&nbsp;<font color="#16C606">360p succeeded</font>
<br/>&nbsp;<font color="#16C606">480p succeeded</font>
<br/>&nbsp;<font color="#16C606">720p succeeded</font>
<br/>&nbsp;<font color="#16C606">1080p succeeded</font>
<br/>&nbsp;<font color="#16C606">2K succeeded</font>
<br/>&nbsp;<font color="#16C606">4K succeeded</font>
<br/>&nbsp;<font color="#E74856">8K failed</font>
<br/>Intel Hardware H264 Encoder(QSV):
<br/>&nbsp;<font color="#16C606">240p succeeded</font>
<br/>&nbsp;<font color="#16C606">360p succeeded</font>
<br/>&nbsp;<font color="#16C606">480p succeeded</font>
<br/>&nbsp;<font color="#16C606">720p succeeded</font>
<br/>&nbsp;<font color="#16C606">1080p succeeded</font>
<br/>&nbsp;<font color="#16C606">2K succeeded</font>
<br/>&nbsp;<font color="#16C606">4K succeeded</font>
<br/>&nbsp;<font color="#E74856">8K failed</font>
<br/>Intel Hardware H265 Encoder(QSV):
<br/>&nbsp;<font color="#16C606">240p succeeded</font>
<br/>&nbsp;<font color="#16C606">360p succeeded</font>
<br/>&nbsp;<font color="#16C606">480p succeeded</font>
<br/>&nbsp;<font color="#16C606">720p succeeded</font>
<br/>&nbsp;<font color="#16C606">1080p succeeded</font>
<br/>&nbsp;<font color="#16C606">2K succeeded</font>
<br/>&nbsp;<font color="#16C606">4K succeeded</font>
<br/>&nbsp;<font color="#16C606">8K succeeded</font>
<br/>Intel Hardware AV1 Encoder(QSV):
<br/>&nbsp;<font color="#E74856">240p failed</font>
<br/>&nbsp;<font color="#E74856">360p failed</font>
<br/>&nbsp;<font color="#E74856">480p failed</font>
<br/>&nbsp;<font color="#E74856">720p failed</font>
<br/>&nbsp;<font color="#E74856">1080p failed</font>
<br/>&nbsp;<font color="#E74856">2K failed</font>
<br/>&nbsp;<font color="#E74856">4K failed</font>
<br/>&nbsp;<font color="#E74856">8K failed</font>
<br/>Intel Hardware MJPEG Encoder(QSV):
<br/>&nbsp;<font color="#16C606">240p succeeded</font>
<br/>&nbsp;<font color="#16C606">360p succeeded</font>
<br/>&nbsp;<font color="#16C606">480p succeeded</font>
<br/>&nbsp;<font color="#16C606">720p succeeded</font>
<br/>&nbsp;<font color="#16C606">1080p succeeded</font>
<br/>&nbsp;<font color="#16C606">2K succeeded</font>
<br/>&nbsp;<font color="#16C606">4K succeeded</font>
<br/>&nbsp;<font color="#16C606">8K succeeded</font>
<br/>Intel Hardware MJPEG-2 Encoder(QSV):
<br/>&nbsp;<font color="#16C606">240p succeeded</font>
<br/>&nbsp;<font color="#16C606">360p succeeded</font>
<br/>&nbsp;<font color="#16C606">480p succeeded</font>
<br/>&nbsp;<font color="#16C606">720p succeeded</font>
<br/>&nbsp;<font color="#16C606">1080p succeeded</font>
<br/>&nbsp;<font color="#E74856">2K failed</font>
<br/>&nbsp;<font color="#E74856">4K failed</font>
<br/>&nbsp;<font color="#E74856">8K failed</font>
<br/>Intel Hardware VP9 Encoder(QSV):
<br/>&nbsp;<font color="#16C606">240p succeeded</font>
<br/>&nbsp;<font color="#16C606">360p succeeded</font>
<br/>&nbsp;<font color="#16C606">480p succeeded</font>
<br/>&nbsp;<font color="#16C606">720p succeeded</font>
<br/>&nbsp;<font color="#16C606">1080p succeeded</font>
<br/>&nbsp;<font color="#16C606">2K succeeded</font>
<br/>&nbsp;<font color="#16C606">4K succeeded</font>
<br/>&nbsp;<font color="#16C606">8K succeeded</font>
<br/>AMD Hardware H264 Encoder(AMF):
<br/>&nbsp;<font color="#16C606">240p succeeded</font>
<br/>&nbsp;<font color="#16C606">360p succeeded</font>
<br/>&nbsp;<font color="#16C606">480p succeeded</font>
<br/>&nbsp;<font color="#16C606">720p succeeded</font>
<br/>&nbsp;<font color="#16C606">1080p succeeded</font>
<br/>&nbsp;<font color="#16C606">2K succeeded</font>
<br/>&nbsp;<font color="#16C606">4K succeeded</font>
<br/>&nbsp;<font color="#E74856">8K failed</font>