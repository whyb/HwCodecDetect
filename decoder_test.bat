@echo off
chcp 65001 > nul

call install_ffmpeg_if_needed.bat
if %errorlevel% neq 0 (
    echo.
    echo 错误: FFmpeg 依赖项安装失败，请检查网络代理或磁盘写入权限。
    pause
    exit /b -1
)

set "directory_path=%TEMP%\HwCodecDetect"

rem 检查目录是否存在
if exist "%directory_path%\" (
    rem 删除目录中的所有文件和子目录
    rem for /d %%d in ("%directory_path%\*") do rd /s /q "%%d"
    rem for %%f in ("%directory_path%\*") do del /q "%%f"
) else (
    rem 创建目录
    mkdir "%directory_path%"
)

rem 用CPU编码生成将要测试的mp4文件

IF NOT EXIST "%directory_path%/h264_240p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v libx264 -preset ultrafast -pixel_format yuv420p "%directory_path%/h264_240p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h264_360p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v libx264 -preset ultrafast -pixel_format yuv420p "%directory_path%/h264_360p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h264_480p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v libx264 -preset ultrafast -pixel_format yuv420p "%directory_path%/h264_480p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h264_720p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v libx264 -preset ultrafast -pixel_format yuv420p "%directory_path%/h264_720p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h264_1080p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v libx264 -preset ultrafast -pixel_format yuv420p "%directory_path%/h264_1080p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h264_2K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v libx264 -preset ultrafast -pixel_format yuv420p "%directory_path%/h264_2K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h264_4K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v libx264 -preset ultrafast -pixel_format yuv420p "%directory_path%/h264_4K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h264_8K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v libx264 -preset ultrafast -pixel_format yuv420p "%directory_path%/h264_8K.mp4">nul 2>&1

IF NOT EXIST "%directory_path%/h265_240p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v libx265 -pixel_format yuv420p "%directory_path%/h265_240p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h265_360p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v libx265 -pixel_format yuv420p "%directory_path%/h265_360p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h265_480p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v libx265 -pixel_format yuv420p "%directory_path%/h265_480p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h265_720p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v libx265 -pixel_format yuv420p "%directory_path%/h265_720p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h265_1080p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v libx265 -pixel_format yuv420p "%directory_path%/h265_1080p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h265_2K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v libx265 -pixel_format yuv420p "%directory_path%/h265_2K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h265_4K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v libx265 -pixel_format yuv420p "%directory_path%/h265_4K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/h265_8K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v libx265 -pixel_format yuv420p "%directory_path%/h265_8K.mp4">nul 2>&1

IF NOT EXIST "%directory_path%/av1_240p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v librav1e -pixel_format yuv420p "%directory_path%/av1_240p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/av1_360p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v librav1e -pixel_format yuv420p "%directory_path%/av1_360p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/av1_480p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v librav1e -pixel_format yuv420p "%directory_path%/av1_480p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/av1_720p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v librav1e -pixel_format yuv420p "%directory_path%/av1_720p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/av1_1080p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v librav1e -pixel_format yuv420p "%directory_path%/av1_1080p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/av1_2K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v librav1e -pixel_format yuv420p "%directory_path%/av1_2K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/av1_4K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v librav1e -pixel_format yuv420p "%directory_path%/av1_4K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/av1_8K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v librav1e -pixel_format yuv420p "%directory_path%/av1_8K.mp4">nul 2>&1

IF NOT EXIST "%directory_path%/mjpeg_240p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v mjpeg -pixel_format yuv420p "%directory_path%/mjpeg_240p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mjpeg_360p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v mjpeg -pixel_format yuv420p "%directory_path%/mjpeg_360p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mjpeg_480p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v mjpeg -pixel_format yuv420p "%directory_path%/mjpeg_480p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mjpeg_720p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v mjpeg -pixel_format yuv420p "%directory_path%/mjpeg_720p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mjpeg_1080p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v mjpeg -pixel_format yuv420p "%directory_path%/mjpeg_1080p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mjpeg_2K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v mjpeg -pixel_format yuv420p "%directory_path%/mjpeg_2K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mjpeg_4K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v mjpeg -pixel_format yuv420p "%directory_path%/mjpeg_4K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mjpeg_8K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v mjpeg -pixel_format yuv420p "%directory_path%/mjpeg_8K.mp4">nul 2>&1

IF NOT EXIST "%directory_path%/mpeg1_240p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v mpeg1video -pixel_format yuv420p "%directory_path%/mpeg1_240p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg1_360p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v mpeg1video -pixel_format yuv420p "%directory_path%/mpeg1_360p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg1_480p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v mpeg1video -pixel_format yuv420p "%directory_path%/mpeg1_480p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg1_720p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v mpeg1video -pixel_format yuv420p "%directory_path%/mpeg1_720p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg1_1080p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v mpeg1video -pixel_format yuv420p "%directory_path%/mpeg1_1080p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg1_2K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v mpeg1video -pixel_format yuv420p "%directory_path%/mpeg1_2K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg1_4K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v mpeg1video -pixel_format yuv420p "%directory_path%/mpeg1_4K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg1_8K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v mpeg1video -pixel_format yuv420p "%directory_path%/mpeg1_8K.mp4">nul 2>&1

IF NOT EXIST "%directory_path%/mpeg2_240p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v mpeg2video -pixel_format yuv420p "%directory_path%/mpeg2_240p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg2_360p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v mpeg2video -pixel_format yuv420p "%directory_path%/mpeg2_360p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg2_480p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v mpeg2video -pixel_format yuv420p "%directory_path%/mpeg2_480p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg2_720p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v mpeg2video -pixel_format yuv420p "%directory_path%/mpeg2_720p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg2_1080p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v mpeg2video -pixel_format yuv420p "%directory_path%/mpeg2_1080p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg2_2K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v mpeg2video -pixel_format yuv420p "%directory_path%/mpeg2_2K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg2_4K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v mpeg2video -pixel_format yuv420p "%directory_path%/mpeg2_4K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg2_8K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v mpeg2video -pixel_format yuv420p "%directory_path%/mpeg2_8K.mp4">nul 2>&1

IF NOT EXIST "%directory_path%/mpeg4_240p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v mpeg4 -pixel_format yuv420p "%directory_path%/mpeg4_240p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg4_360p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v mpeg4 -pixel_format yuv420p "%directory_path%/mpeg4_360p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg4_480p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v mpeg4 -pixel_format yuv420p "%directory_path%/mpeg4_480p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg4_720p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v mpeg4 -pixel_format yuv420p "%directory_path%/mpeg4_720p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg4_1080p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v mpeg4 -pixel_format yuv420p "%directory_path%/mpeg4_1080p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg4_2K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v mpeg4 -pixel_format yuv420p "%directory_path%/mpeg4_2K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg4_4K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v mpeg4 -pixel_format yuv420p "%directory_path%/mpeg4_4K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/mpeg4_8K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v mpeg4 -pixel_format yuv420p "%directory_path%/mpeg4_8K.mp4">nul 2>&1

IF NOT EXIST "%directory_path%/vp8_240p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v libvpx -pixel_format yuv420p "%directory_path%/vp8_240p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp8_360p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v libvpx -pixel_format yuv420p "%directory_path%/vp8_360p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp8_480p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v libvpx -pixel_format yuv420p "%directory_path%/vp8_480p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp8_720p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v libvpx -pixel_format yuv420p "%directory_path%/vp8_720p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp8_1080p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v libvpx -pixel_format yuv420p "%directory_path%/vp8_1080p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp8_2K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v libvpx -pixel_format yuv420p "%directory_path%/vp8_2K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp8_4K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v libvpx -pixel_format yuv420p "%directory_path%/vp8_4K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp8_8K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v libvpx -pixel_format yuv420p "%directory_path%/vp8_8K.mp4">nul 2>&1

IF NOT EXIST "%directory_path%/vp9_240p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v libvpx-vp9 -pixel_format yuv420p "%directory_path%/vp9_240p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp9_360p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v libvpx-vp9 -pixel_format yuv420p "%directory_path%/vp9_360p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp9_480p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v libvpx-vp9 -pixel_format yuv420p "%directory_path%/vp9_480p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp9_720p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v libvpx-vp9 -pixel_format yuv420p "%directory_path%/vp9_720p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp9_1080p.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v libvpx-vp9 -pixel_format yuv420p "%directory_path%/vp9_1080p.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp9_2K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v libvpx-vp9 -pixel_format yuv420p "%directory_path%/vp9_2K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp9_4K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v libvpx-vp9 -pixel_format yuv420p "%directory_path%/vp9_4K.mp4">nul 2>&1
IF NOT EXIST "%directory_path%/vp9_8K.mp4" ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v libvpx-vp9 -pixel_format yuv420p "%directory_path%/vp9_8K.mp4">nul 2>&1

rem 开始测试decoder

echo NVIDIA Hardware H264 Decoder(NVDec):
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_cuvid -i "%directory_path%/h264_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_cuvid -i "%directory_path%/h264_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_cuvid -i "%directory_path%/h264_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_cuvid -i "%directory_path%/h264_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_cuvid -i "%directory_path%/h264_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_cuvid -i "%directory_path%/h264_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_cuvid -i "%directory_path%/h264_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_cuvid -i "%directory_path%/h264_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo NVIDIA Hardware H265 Decoder(NVDec):
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_cuvid -i "%directory_path%/h265_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_cuvid -i "%directory_path%/h265_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_cuvid -i "%directory_path%/h265_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_cuvid -i "%directory_path%/h265_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_cuvid -i "%directory_path%/h265_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_cuvid -i "%directory_path%/h265_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_cuvid -i "%directory_path%/h265_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_cuvid -i "%directory_path%/h265_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo NVIDIA Hardware AV1 Decoder(NVDec):
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_cuvid -i "%directory_path%/av1_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_cuvid -i "%directory_path%/av1_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_cuvid -i "%directory_path%/av1_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_cuvid -i "%directory_path%/av1_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_cuvid -i "%directory_path%/av1_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_cuvid -i "%directory_path%/av1_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_cuvid -i "%directory_path%/av1_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_cuvid -i "%directory_path%/av1_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo NVIDIA Hardware MJPEG Decoder(NVDec):
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_cuvid -i "%directory_path%/mjpeg_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_cuvid -i "%directory_path%/mjpeg_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_cuvid -i "%directory_path%/mjpeg_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_cuvid -i "%directory_path%/mjpeg_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_cuvid -i "%directory_path%/mjpeg_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_cuvid -i "%directory_path%/mjpeg_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_cuvid -i "%directory_path%/mjpeg_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_cuvid -i "%directory_path%/mjpeg_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo NVIDIA Hardware MPEG-1 Decoder(NVDec):
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg1_cuvid -i "%directory_path%/mpeg1_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg1_cuvid -i "%directory_path%/mpeg1_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg1_cuvid -i "%directory_path%/mpeg1_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg1_cuvid -i "%directory_path%/mpeg1_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg1_cuvid -i "%directory_path%/mpeg1_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg1_cuvid -i "%directory_path%/mpeg1_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg1_cuvid -i "%directory_path%/mpeg1_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg1_cuvid -i "%directory_path%/mpeg1_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo NVIDIA Hardware MPEG-2 Decoder(NVDec):
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_cuvid -i "%directory_path%/mpeg2_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_cuvid -i "%directory_path%/mpeg2_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_cuvid -i "%directory_path%/mpeg2_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_cuvid -i "%directory_path%/mpeg2_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_cuvid -i "%directory_path%/mpeg2_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_cuvid -i "%directory_path%/mpeg2_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_cuvid -i "%directory_path%/mpeg2_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_cuvid -i "%directory_path%/mpeg2_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo NVIDIA Hardware MPEG-4 Decoder(NVDec):
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg4_cuvid -i "%directory_path%/mpeg4_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg4_cuvid -i "%directory_path%/mpeg4_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg4_cuvid -i "%directory_path%/mpeg4_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg4_cuvid -i "%directory_path%/mpeg4_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg4_cuvid -i "%directory_path%/mpeg4_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg4_cuvid -i "%directory_path%/mpeg4_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg4_cuvid -i "%directory_path%/mpeg4_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg4_cuvid -i "%directory_path%/mpeg4_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo NVIDIA Hardware VP8 Decoder(NVDec):
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_cuvid -i "%directory_path%/vp8_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_cuvid -i "%directory_path%/vp8_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_cuvid -i "%directory_path%/vp8_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_cuvid -i "%directory_path%/vp8_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_cuvid -i "%directory_path%/vp8_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_cuvid -i "%directory_path%/vp8_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_cuvid -i "%directory_path%/vp8_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_cuvid -i "%directory_path%/vp8_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo NVIDIA Hardware VP9 Decoder(NVDec):
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_cuvid -i "%directory_path%/vp9_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_cuvid -i "%directory_path%/vp9_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_cuvid -i "%directory_path%/vp9_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_cuvid -i "%directory_path%/vp9_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_cuvid -i "%directory_path%/vp9_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_cuvid -i "%directory_path%/vp9_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_cuvid -i "%directory_path%/vp9_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_cuvid -i "%directory_path%/vp9_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)


echo Intel Hardware H264 Decoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_qsv -i "%directory_path%/h264_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_qsv -i "%directory_path%/h264_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_qsv -i "%directory_path%/h264_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_qsv -i "%directory_path%/h264_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_qsv -i "%directory_path%/h264_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_qsv -i "%directory_path%/h264_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_qsv -i "%directory_path%/h264_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v h264_qsv -i "%directory_path%/h264_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware H265 Decoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_qsv -i "%directory_path%/h265_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_qsv -i "%directory_path%/h265_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_qsv -i "%directory_path%/h265_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_qsv -i "%directory_path%/h265_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_qsv -i "%directory_path%/h265_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_qsv -i "%directory_path%/h265_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_qsv -i "%directory_path%/h265_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v hevc_qsv -i "%directory_path%/h265_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware AV1 Decoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_qsv -i "%directory_path%/av1_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_qsv -i "%directory_path%/av1_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_qsv -i "%directory_path%/av1_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_qsv -i "%directory_path%/av1_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_qsv -i "%directory_path%/av1_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_qsv -i "%directory_path%/av1_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_qsv -i "%directory_path%/av1_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v av1_qsv -i "%directory_path%/av1_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware MJPEG Decoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_qsv -i "%directory_path%/mjpeg_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_qsv -i "%directory_path%/mjpeg_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_qsv -i "%directory_path%/mjpeg_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_qsv -i "%directory_path%/mjpeg_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_qsv -i "%directory_path%/mjpeg_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_qsv -i "%directory_path%/mjpeg_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_qsv -i "%directory_path%/mjpeg_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mjpeg_qsv -i "%directory_path%/mjpeg_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware MPEG-2 Decoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_qsv -i "%directory_path%/mpeg2_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_qsv -i "%directory_path%/mpeg2_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_qsv -i "%directory_path%/mpeg2_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_qsv -i "%directory_path%/mpeg2_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_qsv -i "%directory_path%/mpeg2_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_qsv -i "%directory_path%/mpeg2_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_qsv -i "%directory_path%/mpeg2_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v mpeg2_qsv -i "%directory_path%/mpeg2_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware VP8 Decoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_qsv -i "%directory_path%/vp8_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_qsv -i "%directory_path%/vp8_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_qsv -i "%directory_path%/vp8_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_qsv -i "%directory_path%/vp8_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_qsv -i "%directory_path%/vp8_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_qsv -i "%directory_path%/vp8_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_qsv -i "%directory_path%/vp8_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp8_qsv -i "%directory_path%/vp8_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware VP9 Decoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_qsv -i "%directory_path%/vp9_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_qsv -i "%directory_path%/vp9_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_qsv -i "%directory_path%/vp9_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_qsv -i "%directory_path%/vp9_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_qsv -i "%directory_path%/vp9_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_qsv -i "%directory_path%/vp9_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_qsv -i "%directory_path%/vp9_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v vp9_qsv -i "%directory_path%/vp9_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)


echo Microsoft DirectX Video Acceleration H264 Decoder(DXVA2):
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/h264_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/h264_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/h264_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/h264_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/h264_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/h264_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/h264_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/h264_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Microsoft DirectX Video Acceleration H265 Decoder(DXVA2):
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Microsoft DirectX Video Acceleration AV1 Decoder(DXVA2):
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/av1_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/av1_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/av1_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/av1_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/av1_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/av1_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/av1_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/av1_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Microsoft DirectX Video Acceleration MJPEG Decoder(DXVA2):
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mjpeg_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mjpeg_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mjpeg_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mjpeg_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mjpeg_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mjpeg_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mjpeg_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mjpeg_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Microsoft DirectX Video Acceleration MPEG-1 Decoder(DXVA2):
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg1_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg1_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg1_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg1_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg1_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg1_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg1_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg1_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Microsoft DirectX Video Acceleration MPEG-2 Decoder(DXVA2):
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg2_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg2_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg2_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg2_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg2_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg2_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg2_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg2_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Microsoft DirectX Video Acceleration MPEG-4 Decoder(DXVA2):
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg4_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg4_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg4_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg4_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg4_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg4_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg4_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/mpeg4_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Microsoft DirectX Video Acceleration VP8 Decoder(DXVA2):
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/vp8_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/vp8_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/vp8_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/vp8_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/vp8_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/vp8_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/vp8_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel dxva2 -i "%directory_path%/vp8_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Microsoft DirectX Video Acceleration VP9 Decoder(DXVA2):
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/vp9_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/vp9_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/vp9_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/vp9_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/vp9_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/vp9_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/vp9_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v dxva2 -i "%directory_path%/vp9_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)


echo Direct3D 11 Video Acceleration H264 Decoder(D3D11VA):
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h264_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h264_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h264_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h264_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h264_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h264_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h264_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h264_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Direct3D 11 Video Acceleration H265 Decoder(D3D11VA):
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/h265_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Direct3D 11 Video Acceleration AV1 Decoder(D3D11VA):
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/av1_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/av1_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/av1_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/av1_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/av1_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/av1_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/av1_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/av1_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Direct3D 11 Video Acceleration MJPEG Decoder(D3D11VA):
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mjpeg_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mjpeg_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mjpeg_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mjpeg_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mjpeg_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mjpeg_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mjpeg_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mjpeg_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Direct3D 11 Video Acceleration MPEG-1 Decoder(D3D11VA):
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg1_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg1_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg1_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg1_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg1_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg1_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg1_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg1_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Direct3D 11 Video Acceleration MPEG-2 Decoder(D3D11VA):
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg2_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg2_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg2_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg2_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg2_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg2_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg2_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg2_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Direct3D 11 Video Acceleration MPEG-4 Decoder(D3D11VA):
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg4_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg4_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg4_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg4_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg4_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg4_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg4_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/mpeg4_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Direct3D 11 Video Acceleration VP8 Decoder(D3D11VA):
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/vp8_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/vp8_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/vp8_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/vp8_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/vp8_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/vp8_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/vp8_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -hwaccel d3d11va -i "%directory_path%/vp8_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Direct3D 11 Video Acceleration VP9 Decoder(D3D11VA):
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/vp9_240p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/vp9_360p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/vp9_480p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/vp9_720p.mp4"  -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/vp9_1080p.mp4" -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/vp9_2K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/vp9_4K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -c:v d3d11va -i "%directory_path%/vp9_8K.mp4"    -c:v libx264 -preset ultrafast -f null null
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)


rem clean all
rem for /d %%d in ("%directory_path%\*") do rd /s /q "%%d"
rem for %%f in ("%directory_path%\*") do del /q "%%f"
pause