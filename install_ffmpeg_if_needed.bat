@echo off

set "FFMPEG_URL=https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip"
set "ZIP_FILE_NAME=ffmpeg_temp.zip"
set "BIN_DIR_IN_ZIP=ffmpeg-master-latest-win64-gpl-shared\bin"
set "EXIT_CODE=0"

:: Step 1: 检查FFmpeg是否在PATH中
where ffmpeg >nul 2>nul
if %errorlevel% equ 0 (
    goto :cleanup
)

:: Step 2: 下载文件
powershell.exe -Command "Invoke-WebRequest -Uri '%FFMPEG_URL%' -OutFile '%TEMP%\%ZIP_FILE_NAME%'" >nul
if %errorlevel% neq 0 (
    set "EXIT_CODE=-1"
    goto :cleanup
)

set "TEMP_EXTRACT_DIR=%TEMP%\ffmpeg_extracted"

:: Step 3: 解压文件
powershell.exe -Command "Expand-Archive -Path '%TEMP%\%ZIP_FILE_NAME%' -DestinationPath '%TEMP_EXTRACT_DIR%'" >nul
if %errorlevel% neq 0 (
    set "EXIT_CODE=-1"
    goto :cleanup
)

:: Step 4: 尝试将文件移动到当前目录
move /Y "%TEMP_EXTRACT_DIR%\%BIN_DIR_IN_ZIP%\*" "%~dp0" >nul
if %errorlevel% neq 0 (
    :: 移动失败，改用临时目录
    echo 无法解压到当前目录，正在尝试使用系统临时目录。
    set "INSTALL_DIR=%TEMP%\%BIN_DIR_IN_ZIP%"
    set PATH=%PATH%;%INSTALL_DIR%
) else (
    set "INSTALL_DIR=%~dp0"
)

:: Step 5: 清理临时文件
:cleanup
if exist "%TEMP%\%ZIP_FILE_NAME%" del "%TEMP%\%ZIP_FILE_NAME%"
if exist "%TEMP_EXTRACT_DIR%" rd /s /q "%TEMP_EXTRACT_DIR%"

:: Step 6: 返回退出代码
exit /b %EXIT_CODE%