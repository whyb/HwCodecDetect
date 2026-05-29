"""
Codec, resolution, and pixel format definitions shared across CLI, GUI, and bit-depth modules.
Single source of truth for all hardware codec data.
"""

# Resolution definitions
RESOLUTIONS = {
    "240p": "426x240",
    "360p": "640x360",
    "480p": "854x480",
    "720p": "1280x720",
    "1080p": "1920x1080",
    "2K": "2560x1440",
    "4K": "3840x2160",
    "8K": "7680x4320",
}

# Mapping of a decoder's ffmpeg name and codec to its descriptive title
DECODER_TITLES = {
    ("h264_cuvid", "h264"): "NVIDIA CUDA H264 Decoder(NVDEC)",
    ("h264_qsv", "h264"): "Intel Quick Sync Video H264 Decoder(QSV)",
    ("hevc_cuvid", "h265"): "NVIDIA CUDA H265 Decoder(NVDEC)",
    ("hevc_qsv", "h265"): "Intel Quick Sync Video H265 Decoder(QSV)",
    ("av1_cuvid", "av1"): "NVIDIA CUDA AV1 Decoder(NVDEC)",
    ("av1_qsv", "av1"): "Intel Quick Sync Video AV1 Decoder(QSV)",
    ("mjpeg_cuvid", "mjpeg"): "NVIDIA CUDA MJPEG Decoder(NVDEC)",
    ("mjpeg_qsv", "mjpeg"): "Intel Quick Sync Video MJPEG Decoder(QSV)",
    ("mpeg1_cuvid", "mpeg1"): "NVIDIA CUDA MPEG-1 Decoder(NVDEC)",
    ("mpeg2_cuvid", "mpeg2"): "NVIDIA CUDA MPEG-2 Decoder(NVDEC)",
    ("mpeg2_qsv", "mpeg2"): "Intel Quick Sync Video MPEG-2 Decoder(QSV)",
    ("mpeg4_cuvid", "mpeg4"): "NVIDIA CUDA MPEG-4 Decoder(NVDEC)",
    ("vp8_cuvid", "vp8"): "NVIDIA CUDA VP8 Decoder(NVDEC)",
    ("vp8_qsv", "vp8"): "Intel Quick Sync Video VP8 Decoder(QSV)",
    ("vp9_cuvid", "vp9"): "NVIDIA CUDA VP9 Decoder(NVDEC)",
    ("vp9_qsv", "vp9"): "Intel Quick Sync Video VP9 Decoder(QSV)",
    ("dxva2", "h264"): "Microsoft DirectX Video Acceleration H264 Decoder(DXVA2)",
    ("dxva2", "h265"): "Microsoft DirectX Video Acceleration H265 Decoder(DXVA2)",
    ("dxva2", "av1"): "Microsoft DirectX Video Acceleration AV1 Decoder(DXVA2)",
    ("dxva2", "mjpeg"): "Microsoft DirectX Video Acceleration MJPEG Decoder(DXVA2)",
    ("dxva2", "mpeg1"): "Microsoft DirectX Video Acceleration MPEG-1 Decoder(DXVA2)",
    ("dxva2", "mpeg2"): "Microsoft DirectX Video Acceleration MPEG-2 Decoder(DXVA2)",
    ("dxva2", "mpeg4"): "Microsoft DirectX Video Acceleration MPEG-4 Decoder(DXVA2)",
    ("dxva2", "vp8"): "Microsoft DirectX Video Acceleration VP8 Decoder(DXVA2)",
    ("dxva2", "vp9"): "Microsoft DirectX Video Acceleration VP9 Decoder(DXVA2)",
    ("d3d11va", "h264"): "Microsoft Direct3D 11 Video Acceleration H264 Decoder(D3D11VA)",
    ("d3d11va", "h265"): "Microsoft Direct3D 11 Video Acceleration H265 Decoder(D3D11VA)",
    ("d3d11va", "av1"): "Microsoft Direct3D 11 Video Acceleration AV1 Decoder(D3D11VA)",
    ("d3d11va", "mjpeg"): "Microsoft Direct3D 11 Video Acceleration MJPEG Decoder(D3D11VA)",
    ("d3d11va", "mpeg1"): "Microsoft Direct3D 11 Video Acceleration MPEG-1 Decoder(D3D11VA)",
    ("d3d11va", "mpeg2"): "Microsoft Direct3D 11 Video Acceleration MPEG-2 Decoder(D3D11VA)",
    ("d3d11va", "mpeg4"): "Microsoft Direct3D 11 Video Acceleration MPEG-4 Decoder(D3D11VA)",
    ("d3d11va", "vp8"): "Microsoft Direct3D 11 Video Acceleration VP8 Decoder(D3D11VA)",
    ("d3d11va", "vp9"): "Microsoft Direct3D 11 Video Acceleration VP9 Decoder(D3D11VA)",
    ("d3d12va", "h264"): "Microsoft Direct3D 12 Video Acceleration H264 Decoder(D3D12VA)",
    ("d3d12va", "h265"): "Microsoft Direct3D 12 Video Acceleration H265 Decoder(D3D12VA)",
    ("d3d12va", "av1"): "Microsoft Direct3D 12 Video Acceleration AV1 Decoder(D3D12VA)",
    ("d3d12va", "mjpeg"): "Microsoft Direct3D 12 Video Acceleration MJPEG Decoder(D3D12VA)",
    ("d3d12va", "mpeg1"): "Microsoft Direct3D 12 Video Acceleration MPEG-1 Decoder(D3D12VA)",
    ("d3d12va", "mpeg2"): "Microsoft Direct3D 12 Video Acceleration MPEG-2 Decoder(D3D12VA)",
    ("d3d12va", "mpeg4"): "Microsoft Direct3D 12 Video Acceleration MPEG-4 Decoder(D3D12VA)",
    ("d3d12va", "vp8"): "Microsoft Direct3D 12 Video Acceleration VP8 Decoder(D3D12VA)",
    ("d3d12va", "vp9"): "Microsoft Direct3D 12 Video Acceleration VP9 Decoder(D3D12VA)",
    ("vulkan", "h264"): "Vulkan Hardware H264 Decoder(Vulkan)",
    ("vulkan", "h265"): "Vulkan Hardware H265 Decoder(Vulkan)",
    ("vulkan", "av1"): "Vulkan Hardware AV1 Decoder(Vulkan)",
    ("videotoolbox", "h264"): "Apple macOS Hardware H264 Decoder(VideoToolbox)",
    ("videotoolbox", "h265"): "Apple macOS Hardware H265 Decoder(VideoToolbox)",
    ("videotoolbox", "mpeg2"): "Apple macOS Hardware MPEG-2 Decoder(VideoToolbox)",
    ("videotoolbox", "mpeg4"): "Apple macOS Hardware MPEG-4 Decoder(VideoToolbox)",
    ("videotoolbox", "prores"): "Apple macOS Hardware ProRes Decoder(VideoToolbox)",
    ("videotoolbox", "vp9"): "Apple macOS Hardware VP9 Decoder(VideoToolbox)",
}

# Mapping of an encoder's ffmpeg name and codec to its descriptive title
ENCODER_TITLES = {
    ("h264_nvenc", "h264"): "NVIDIA Hardware H264 Encoder(NVEnc)",
    ("hevc_nvenc", "h265"): "NVIDIA Hardware H265 Encoder(NVEnc)",
    ("av1_nvenc", "av1"): "NVIDIA Hardware AV1 Encoder(NVEnc)",
    ("h264_qsv", "h264"): "Intel Hardware H264 Encoder(QSV)",
    ("hevc_qsv", "h265"): "Intel Hardware H265 Encoder(QSV)",
    ("av1_qsv", "av1"): "Intel Hardware AV1 Encoder(QSV)",
    ("mjpeg_qsv", "mjpeg"): "Intel Hardware MJPEG Encoder(QSV)",
    ("mpeg2_qsv", "mpeg2"): "Intel Hardware MPEG-2 Encoder(QSV)",
    ("vp9_qsv", "vp9"): "Intel Hardware VP9 Encoder(QSV)",
    ("h264_amf", "h264"): "AMD Hardware H264 Encoder(AMF)",
    ("hevc_amf", "h265"): "AMD Hardware H265 Encoder(AMF)",
    ("av1_amf", "av1"): "AMD Hardware AV1 Encoder(AMF)",
    ("h264_mf", "h264"): "Microsoft Hardware H264 Encoder(MediaFoundation)",
    ("hevc_mf", "h265"): "Microsoft Hardware H265 Encoder(MediaFoundation)",
    ("av1_mf", "av1"): "Microsoft Hardware AV1 Encoder(MediaFoundation)",
    ("h264_d3d12va", "h264"): "Microsoft Direct3D 12 Video Acceleration H264 Encoder(D3D12VA)",
    ("hevc_d3d12va", "h265"): "Microsoft Direct3D 12 Video Acceleration H265 Encoder(D3D12VA)",
    ("av1_d3d12va", "av1"): "Microsoft Direct3D 12 Video Acceleration AV1 Encoder(D3D12VA)",
    ("h264_vaapi", "h264"): "Video Acceleration H264 Encoder(VAAPI)",
    ("hevc_vaapi", "h265"): "Video Acceleration H265 Encoder(VAAPI)",
    ("av1_vaapi", "av1"): "Video Acceleration AV1 Encoder(VAAPI)",
    ("mjpeg_vaapi", "mjpeg"): "Video Acceleration MJPEG Encoder(VAAPI)",
    ("mpeg2_vaapi", "mpeg2"): "Video Acceleration MPEG-2 Encoder(VAAPI)",
    ("vp8_vaapi", "vp8"): "Video Acceleration VP8 Encoder(VAAPI)",
    ("vp9_vaapi", "vp9"): "Video Acceleration VP9 Encoder(VAAPI)",
    ("h264_vulkan", "h264"): "Vulkan Hardware H264 Encoder(Vulkan)",
    ("hevc_vulkan", "h265"): "Vulkan Hardware H265 Encoder(Vulkan)",
    ("av1_vulkan", "av1"): "Vulkan Hardware AV1 Encoder(Vulkan)",
    ("h264_videotoolbox", "h264"): "Apple macOS Hardware H264 Encoder(VideoToolbox)",
    ("hevc_videotoolbox", "h265"): "Apple macOS Hardware H265 Encoder(VideoToolbox)",
    ("prores_videotoolbox", "prores"): "Apple macOS Hardware ProRes Encoder(VideoToolbox)",
}

# Decoder definitions: codec -> {lib, hw_decoders}
DECODERS = {
    "h264": {"lib": "libx264", "hw_decoders": ["h264_cuvid", "h264_qsv", "dxva2", "d3d11va", "d3d12va", "vulkan", "videotoolbox"]},
    "h265": {"lib": "libx265", "hw_decoders": ["hevc_cuvid", "hevc_qsv", "d3d11va", "d3d12va", "vulkan", "videotoolbox"]},
    "av1": {"lib": "librav1e", "hw_decoders": ["av1_cuvid", "av1_qsv", "dxva2", "d3d11va", "d3d12va", "vulkan"]},
    "mjpeg": {"lib": "mjpeg", "hw_decoders": ["mjpeg_cuvid", "mjpeg_qsv", "dxva2", "d3d11va", "d3d12va"]},
    "mpeg1": {"lib": "mpeg1video", "hw_decoders": ["mpeg1_cuvid", "dxva2", "d3d11va", "d3d12va"]},
    "mpeg2": {"lib": "mpeg2video", "hw_decoders": ["mpeg2_cuvid", "mpeg2_qsv", "dxva2", "d3d11va", "d3d12va", "videotoolbox"]},
    "mpeg4": {"lib": "mpeg4", "hw_decoders": ["mpeg4_cuvid", "dxva2", "d3d11va", "d3d12va", "videotoolbox"]},
    "vp8": {"lib": "libvpx", "hw_decoders": ["vp8_cuvid", "vp8_qsv", "dxva2", "d3d11va", "d3d12va"]},
    "vp9": {"lib": "libvpx-vp9", "hw_decoders": ["vp9_cuvid", "vp9_qsv", "dxva2", "d3d11va", "d3d12va", "videotoolbox"]},
    "prores": {"lib": "prores", "hw_decoders": ["videotoolbox"]},
}

# Encoder definitions: codec -> {lib, hw_encoders}
ENCODERS = {
    "h264": {"lib": "libx264", "hw_encoders": ["h264_nvenc", "h264_qsv", "h264_amf", "h264_mf", "h264_d3d12va", "h264_vaapi", "h264_vulkan", "h264_videotoolbox"]},
    "h265": {"lib": "libx265", "hw_encoders": ["hevc_nvenc", "hevc_qsv", "hevc_amf", "hevc_mf", "hevc_d3d12va", "hevc_vaapi", "hevc_vulkan", "hevc_videotoolbox"]},
    "av1": {"lib": "librav1e", "hw_encoders": ["av1_nvenc", "av1_qsv", "av1_amf", "av1_mf", "av1_d3d12va", "av1_vaapi", "av1_vulkan"]},
    "mjpeg": {"lib": "mjpeg", "hw_encoders": ["mjpeg_qsv", "mjpeg_vaapi"]},
    "mpeg2": {"lib": "mpeg2video", "hw_encoders": ["mpeg2_qsv", "mpeg2_vaapi"]},
    "vp8": {"lib": "libvpx", "hw_encoders": ["vp8_vaapi"]},
    "vp9": {"lib": "libvpx-vp9", "hw_encoders": ["vp9_qsv", "vp9_vaapi"]},
    "prores": {"lib": "prores", "hw_encoders": ["prores_videotoolbox"]},
}

# Combine both decoder and encoder data into a single structure
ALL_CODECS = {
    **DECODERS,
    **{k: v for k, v in ENCODERS.items() if k not in DECODERS}
}

# Fixed resolution for bit-depth and chroma tests
BITDEPTH_CHROMA_RESOLUTION = "1280x720"

# Pixel format definitions: (pix_fmt_name, bit_depth, chroma_sampling, description)
PIXEL_FORMATS = [
    ("yuv420p", 8, "4:2:0", "8-bit YUV 4:2:0"),
    ("yuv422p", 8, "4:2:2", "8-bit YUV 4:2:2"),
    ("yuv444p", 8, "4:4:4", "8-bit YUV 4:4:4"),
    ("yuv420p10le", 10, "4:2:0", "10-bit YUV 4:2:0"),
    ("yuv422p10le", 10, "4:2:2", "10-bit YUV 4:2:2"),
    ("yuv444p10le", 10, "4:4:4", "10-bit YUV 4:4:4"),
    ("yuv420p12le", 12, "4:2:0", "12-bit YUV 4:2:0"),
    ("yuv422p12le", 12, "4:2:2", "12-bit YUV 4:2:2"),
    ("yuv444p12le", 12, "4:4:4", "12-bit YUV 4:4:4"),
]
