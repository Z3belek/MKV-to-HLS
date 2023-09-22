<p align="center">
  <img src="https://zebelek.vercel.app/_next/static/media/Logo.1d5e7f97.svg" alt="Icono de la Aplicación" width="100">
</p>

<h1 align="center">ZBK | MKV to HLS</h1>

<p align="center">
  The easy way to convert MKV to HLS. 🤖
</p>

![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
## Description
🎥 This project automates the conversion of multiple MKV files into HLS (HTTP Live Streaming) format with multiple resolutions and audio tracks. HLS is a widely used protocol for online video streaming.

## Features

✨ Converts MKV files into HLS format.
✨ Supports multiple AAC audio tracks.
✨ Creates multiple resolutions for HLS streaming.
✨ Generates a master `.m3u8` file that allows the selection of resolutions and audio tracks.

## Dependencies

- [Python 3.x](https://www.python.org/downloads/): The code is written in Python 3 and requires a Python installation.
- [FFmpeg](https://www.ffmpeg.org/): It is used to manipulate video and audio files. Ensure that FFmpeg is installed and accessible from the command line.

## Hardware Requirements

🖥️ NVIDIA graphics card (optional): The code utilizes NVIDIA's CUDA hardware acceleration for video conversion. It is recommended to have a CUDA-compatible NVIDIA graphics card for optimal performance.

## Environment Setup

1. Clone this repository to your system.
```bash
git clone https://github.com/Z3belek/MKV-to-HLS.git
```

2. Install Python dependencies.
```bash
pip install -r requirements.txt
```

3. Ensure that FFmpeg is accessible from the command line.
```bash
ffmpeg -version
```

## Usage

1. Place the MKV files in the same folder as `main.py`.

2. Execute the `main.py` script to start the conversion.
```bash
py main.py
```

3. A folder will be created for each MKV file, and within each folder, the `resoluciones` will be created in separate subfolders.

3. Temporary MP4 and AAC files will be generated and will be removed upon completion of the conversion.

4. `Hls` files will be created within each resolution folder..

5. The master `.m3u8` file will be generated in the root folder of each file.

## License

This project is licensed under the MIT License. Please refer to the ([LICENSE](https://github.com/Z3belek/MKV-to-HLS/blob/main/LICENSE)) file for more details.

## Contributions

Contributions are welcome. If you wish to contribute to this project, create a Pull Request with your suggestions.
