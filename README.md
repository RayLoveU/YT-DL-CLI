# Video and Audio Downloader

A command-line downloader built with Python and [yt-dlp](https://github.com/yt-dlp/yt-dlp). It can download videos in MP4, MKV, or WebM, or extract audio in several formats.

## Requirements

- `Python`
- `yt-dlp`
- `FFmpeg`

Install yt-dlp:

```powershell
python -m pip install yt-dlp
```

Install FFmpeg separately and make sure `ffmpeg` is available on your `PATH`. Video downloads may work without FFmpeg when the selected format is already available as a complete file. Audio downloads require FFmpeg.

## Run

From the project directory:

```powershell
python main.py
```

Follow the prompts to choose video or audio, provide a URL, and select quality and format. The video format defaults to MP4 if you leave its choice blank. Download progress displays the percentage and estimated remaining time.

Files are saved to the current user's `Downloads` folder.

## Video formats

- **MP4**
- **MKV**
- **WebM**

When FFmpeg is installed, yt-dlp uses it to merge and remux video into the selected container. Without FFmpeg, only a complete source file available in the selected format can be downloaded.

## Audio formats

MP3, WAV, M4A, AAC, FLAC, OGG (Vorbis), and OPUS.
