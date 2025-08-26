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
    for /d %%d in ("%directory_path%\*") do rd /s /q "%%d"
    for %%f in ("%directory_path%\*") do del /q "%%f"
) else (
    rem 创建目录
    mkdir "%directory_path%"
)

echo NVIDIA Hardware H264 Encoder(NVEnc):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v h264_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h264_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v h264_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h264_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v h264_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h264_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v h264_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h264_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v h264_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h264_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v h264_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h264_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v h264_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h264_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v h264_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h264_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo NVIDIA Hardware H265 Encoder(NVEnc):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v hevc_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h265_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v hevc_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h265_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v hevc_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h265_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v hevc_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h265_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v hevc_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h265_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v hevc_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h265_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v hevc_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h265_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v hevc_nvenc -pixel_format yuv420p "%directory_path%/nvidia_h265_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo NVIDIA Hardware AV1 Encoder(NVEnc):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v av1_nvenc -pixel_format yuv420p "%directory_path%/nvidia_av1_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v av1_nvenc -pixel_format yuv420p "%directory_path%/nvidia_av1_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v av1_nvenc -pixel_format yuv420p "%directory_path%/nvidia_av1_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v av1_nvenc -pixel_format yuv420p "%directory_path%/nvidia_av1_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v av1_nvenc -pixel_format yuv420p "%directory_path%/nvidia_av1_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v av1_nvenc -pixel_format yuv420p "%directory_path%/nvidia_av1_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v av1_nvenc -pixel_format yuv420p "%directory_path%/nvidia_av1_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v av1_nvenc -pixel_format yuv420p "%directory_path%/nvidia_av1_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)


echo Intel Hardware H264 Encoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v h264_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h264_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v h264_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h264_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v h264_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h264_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v h264_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h264_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v h264_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h264_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v h264_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h264_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v h264_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h264_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v h264_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h264_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware H265 Encoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v hevc_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h265_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v hevc_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h265_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v hevc_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h265_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v hevc_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h265_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v hevc_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h265_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v hevc_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h265_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v hevc_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h265_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v hevc_qsv -dual_gfx 0 -pixel_format yuv420p "%directory_path%/intel_h265_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware AV1 Encoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v av1_qsv -pixel_format yuv420p "%directory_path%/intel_av1_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v av1_qsv -pixel_format yuv420p "%directory_path%/intel_av1_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v av1_qsv -pixel_format yuv420p "%directory_path%/intel_av1_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v av1_qsv -pixel_format yuv420p "%directory_path%/intel_av1_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v av1_qsv -pixel_format yuv420p "%directory_path%/intel_av1_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v av1_qsv -pixel_format yuv420p "%directory_path%/intel_av1_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v av1_qsv -pixel_format yuv420p "%directory_path%/intel_av1_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v av1_qsv -pixel_format yuv420p "%directory_path%/intel_av1_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware MJPEG Encoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v mjpeg_qsv -pixel_format yuv420p "%directory_path%/intel_mjpeg_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v mjpeg_qsv -pixel_format yuv420p "%directory_path%/intel_mjpeg_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v mjpeg_qsv -pixel_format yuv420p "%directory_path%/intel_mjpeg_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v mjpeg_qsv -pixel_format yuv420p "%directory_path%/intel_mjpeg_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v mjpeg_qsv -pixel_format yuv420p "%directory_path%/intel_mjpeg_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v mjpeg_qsv -pixel_format yuv420p "%directory_path%/intel_mjpeg_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v mjpeg_qsv -pixel_format yuv420p "%directory_path%/intel_mjpeg_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v mjpeg_qsv -pixel_format yuv420p "%directory_path%/intel_mjpeg_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware MJPEG-2 Encoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v mpeg2_qsv -pixel_format yuv420p "%directory_path%/intel_mpeg2_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v mpeg2_qsv -pixel_format yuv420p "%directory_path%/intel_mpeg2_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v mpeg2_qsv -pixel_format yuv420p "%directory_path%/intel_mpeg2_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v mpeg2_qsv -pixel_format yuv420p "%directory_path%/intel_mpeg2_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v mpeg2_qsv -pixel_format yuv420p "%directory_path%/intel_mpeg2_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v mpeg2_qsv -pixel_format yuv420p "%directory_path%/intel_mpeg2_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v mpeg2_qsv -pixel_format yuv420p "%directory_path%/intel_mpeg2_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v mpeg2_qsv -pixel_format yuv420p "%directory_path%/intel_mpeg2_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Intel Hardware VP9 Encoder(QSV):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v vp9_qsv -pixel_format yuv420p "%directory_path%/intel_vp9_240p.webm"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v vp9_qsv -pixel_format yuv420p "%directory_path%/intel_vp9_360p.webm"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v vp9_qsv -pixel_format yuv420p "%directory_path%/intel_vp9_480p.webm"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v vp9_qsv -pixel_format yuv420p "%directory_path%/intel_vp9_720p.webm"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v vp9_qsv -pixel_format yuv420p "%directory_path%/intel_vp9_1080p.webm"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v vp9_qsv -pixel_format yuv420p "%directory_path%/intel_vp9_2K.webm"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v vp9_qsv -pixel_format yuv420p "%directory_path%/intel_vp9_4K.webm"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v vp9_qsv -pixel_format yuv420p "%directory_path%/intel_vp9_8K.webm"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)


echo AMD Hardware H264 Encoder(AMF):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v h264_amf -pixel_format yuv420p "%directory_path%/amd_h264_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v h264_amf -pixel_format yuv420p "%directory_path%/amd_h264_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v h264_amf -pixel_format yuv420p "%directory_path%/amd_h264_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v h264_amf -pixel_format yuv420p "%directory_path%/amd_h264_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v h264_amf -pixel_format yuv420p "%directory_path%/amd_h264_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v h264_amf -pixel_format yuv420p "%directory_path%/amd_h264_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v h264_amf -pixel_format yuv420p "%directory_path%/amd_h264_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v h264_amf -pixel_format yuv420p "%directory_path%/amd_h264_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo AMD Hardware H265 Encoder(AMF):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v hevc_amf -pixel_format yuv420p "%directory_path%/amd_h265_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v hevc_amf -pixel_format yuv420p "%directory_path%/amd_h265_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v hevc_amf -pixel_format yuv420p "%directory_path%/amd_h265_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v hevc_amf -pixel_format yuv420p "%directory_path%/amd_h265_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v hevc_amf -pixel_format yuv420p "%directory_path%/amd_h265_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v hevc_amf -pixel_format yuv420p "%directory_path%/amd_h265_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v hevc_amf -pixel_format yuv420p "%directory_path%/amd_h265_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v hevc_amf -pixel_format yuv420p "%directory_path%/amd_h265_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo AMD Hardware AV1 Encoder(AMF):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v av1_amf -pixel_format yuv420p "%directory_path%/amd_av1_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v av1_amf -pixel_format yuv420p "%directory_path%/amd_av1_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v av1_amf -pixel_format yuv420p "%directory_path%/amd_av1_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v av1_amf -pixel_format yuv420p "%directory_path%/amd_av1_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v av1_amf -pixel_format yuv420p "%directory_path%/amd_av1_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v av1_amf -pixel_format yuv420p "%directory_path%/amd_av1_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v av1_amf -pixel_format yuv420p "%directory_path%/amd_av1_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v av1_amf -pixel_format yuv420p "%directory_path%/amd_av1_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)


echo Microsoft Hardware H264 Encoder(MediaFoundation):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v h264_mf -pixel_format yuv420p "%directory_path%/microsoft_h264_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v h264_mf -pixel_format yuv420p "%directory_path%/microsoft_h264_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v h264_mf -pixel_format yuv420p "%directory_path%/microsoft_h264_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v h264_mf -pixel_format yuv420p "%directory_path%/microsoft_h264_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v h264_mf -pixel_format yuv420p "%directory_path%/microsoft_h264_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v h264_mf -pixel_format yuv420p "%directory_path%/microsoft_h264_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v h264_mf -pixel_format yuv420p "%directory_path%/microsoft_h264_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v h264_mf -pixel_format yuv420p "%directory_path%/microsoft_h264_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Microsoft Hardware H265 Encoder(MediaFoundation):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v hevc_mf -pixel_format yuv420p "%directory_path%/microsoft_h265_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v hevc_mf -pixel_format yuv420p "%directory_path%/microsoft_h265_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v hevc_mf -pixel_format yuv420p "%directory_path%/microsoft_h265_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v hevc_mf -pixel_format yuv420p "%directory_path%/microsoft_h265_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v hevc_mf -pixel_format yuv420p "%directory_path%/microsoft_h265_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v hevc_mf -pixel_format yuv420p "%directory_path%/microsoft_h265_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v hevc_mf -pixel_format yuv420p "%directory_path%/microsoft_h265_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v hevc_mf -pixel_format yuv420p "%directory_path%/microsoft_h265_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)


echo Video Acceleration H264 Encoder(VAAPI):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v h264_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h264_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v h264_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h264_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v h264_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h264_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v h264_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h264_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v h264_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h264_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v h264_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h264_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v h264_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h264_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v h264_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h264_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Video Acceleration H265 Encoder(VAAPI):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v hevc_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h265_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v hevc_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h265_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v hevc_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h265_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v hevc_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h265_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v hevc_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h265_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v hevc_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h265_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v hevc_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h265_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v hevc_vaapi -pixel_format yuv420p "%directory_path%/vaapi_h265_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Video Acceleration AV1 Encoder(VAAPI):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v av1_vaapi -pixel_format yuv420p "%directory_path%/vaapi_av1_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v av1_vaapi -pixel_format yuv420p "%directory_path%/vaapi_av1_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v av1_vaapi -pixel_format yuv420p "%directory_path%/vaapi_av1_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v av1_vaapi -pixel_format yuv420p "%directory_path%/vaapi_av1_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v av1_vaapi -pixel_format yuv420p "%directory_path%/vaapi_av1_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v av1_vaapi -pixel_format yuv420p "%directory_path%/vaapi_av1_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v av1_vaapi -pixel_format yuv420p "%directory_path%/vaapi_av1_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v av1_vaapi -pixel_format yuv420p "%directory_path%/vaapi_av1_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Video Acceleration MJPEG Encoder(VAAPI):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v mjpeg_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mjpeg_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v mjpeg_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mjpeg_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v mjpeg_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mjpeg_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v mjpeg_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mjpeg_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v mjpeg_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mjpeg_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v mjpeg_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mjpeg_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v mjpeg_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mjpeg_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v mjpeg_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mjpeg_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Video Acceleration MJPEG-2 Encoder(VAAPI):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v mpeg2_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mpeg2_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v mpeg2_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mpeg2_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v mpeg2_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mpeg2_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v mpeg2_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mpeg2_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v mpeg2_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mpeg2_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v mpeg2_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mpeg2_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v mpeg2_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mpeg2_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v mpeg2_vaapi -pixel_format yuv420p "%directory_path%/vaapi_mpeg2_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Video Acceleration VP8 Encoder(VAAPI):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v vp8_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp8_240p.webm"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v vp8_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp8_360p.webm"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v vp8_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp8_480p.webm"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v vp8_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp8_720p.webm"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v vp8_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp8_1080p.webm"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v vp8_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp8_2K.webm"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v vp8_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp8_4K.webm"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v vp8_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp8_8K.webm"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Video Acceleration VP9 Encoder(VAAPI):
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v vp9_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp9_240p.webm"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v vp9_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp9_360p.webm"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v vp9_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp9_480p.webm"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v vp9_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp9_720p.webm"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v vp9_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp9_1080p.webm"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v vp9_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp9_2K.webm"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v vp9_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp9_4K.webm"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v vp9_vaapi -pixel_format yuv420p "%directory_path%/vaapi_vp9_8K.webm"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)


echo Vulkan Hardware H264 Encoder:
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v h264_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h264_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v h264_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h264_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v h264_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h264_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v h264_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h264_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v h264_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h264_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v h264_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h264_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v h264_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h264_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v h264_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h264_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)

echo Vulkan Hardware H265 Encoder:
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=426x240:d=1 -frames:v 1 -c:v hevc_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h265_240p.mp4"
IF %errorlevel% EQU 0 (echo  [92m240p succeeded[0m) ELSE (echo  [91m240p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=640x360:d=1 -frames:v 1 -c:v hevc_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h265_360p.mp4"
IF %errorlevel% EQU 0 (echo  [92m360p succeeded[0m) ELSE (echo  [91m360p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=854x480:d=1 -frames:v 1 -c:v hevc_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h265_480p.mp4"
IF %errorlevel% EQU 0 (echo  [92m480p succeeded[0m) ELSE (echo  [91m480p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1280x720:d=1 -frames:v 1 -c:v hevc_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h265_720p.mp4"
IF %errorlevel% EQU 0 (echo  [92m720p succeeded[0m) ELSE (echo  [91m720p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=1920x1080:d=1 -frames:v 1 -c:v hevc_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h265_1080p.mp4"
IF %errorlevel% EQU 0 (echo  [92m1080p succeeded[0m) ELSE (echo  [91m1080p failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=2560x1440:d=1 -frames:v 1 -c:v hevc_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h265_2K.mp4"
IF %errorlevel% EQU 0 (echo  [92m2K succeeded[0m) ELSE (echo  [91m2K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=3840x2160:d=1 -frames:v 1 -c:v hevc_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h265_4K.mp4"
IF %errorlevel% EQU 0 (echo  [92m4K succeeded[0m) ELSE (echo  [91m4K failed[0m)
ffmpeg -loglevel quiet -hide_banner -y -f lavfi -i color=white:s=7680x4320:d=1 -frames:v 1 -c:v hevc_vulkan -pixel_format yuv420p "%directory_path%/vulkan_h265_8K.mp4"
IF %errorlevel% EQU 0 (echo  [92m8K succeeded[0m) ELSE (echo  [91m8K failed[0m)


rem clean all
for /d %%d in ("%directory_path%\*") do rd /s /q "%%d"
for %%f in ("%directory_path%\*") do del /q "%%f"
pause