import pathlib
import shutil

import yt_dlp

DOWNLOAD_PATH = pathlib.Path.home() / "Downloads"


def ascii_art() -> str:
    return r"""
==============================
__   _______     ____  _
\ \ / /_   _|   |  _ \| |
 \ V /  | |_____| | | | |
  | |   | |_____| |_| | |___
  |_|   |_|     |____/|_____|

==============================
         By: RayLoveU

Choose an option:
[1] Download Video
[2] Download Audio
[3] Exit
"""


def get_download_path() -> pathlib.Path:
    DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
    return DOWNLOAD_PATH


def is_ffmpeg_installed() -> bool:
    return shutil.which("ffmpeg") is not None


def get_video_format(quality: str, video_container: str = "mp4") -> str:
    quality_filters = {
        "best": "",
        "1080p": "[height<=1080][height>=720]",
        "720p": "[height<=720][height>=480]",
        "480p": "[height<=480][height>=360]",
        "360p": "[height<=360]",
    }
    quality_filter = quality_filters.get(quality, quality_filters["best"])

    if not is_ffmpeg_installed():
        return f"best{quality_filter}[ext={video_container}]"

    if video_container == "mkv":
        return f"bestvideo{quality_filter}+bestaudio/best{quality_filter}"

    audio_extension = "m4a" if video_container == "mp4" else "webm"
    return (
        f"bestvideo{quality_filter}[ext={video_container}]"
        f"+bestaudio[ext={audio_extension}]"
        f"/best{quality_filter}[ext={video_container}]"
    )


def get_audio_format(quality: str) -> str:
    format_map = {
        "best": "bestaudio/best",
        "low": "bestaudio[abr<=64]/bestaudio/best",
        "medium": "bestaudio[abr<=128]/bestaudio/best",
        "high": "bestaudio[abr<=192]/bestaudio/best",
    }
    return format_map.get(quality, format_map["best"])


def get_audio_codec_choice() -> str:
    while True:
        print("\nChoose an audio format:")
        print("[1] MP3")
        print("[2] WAV")
        print("[3] M4A")
        print("[4] AAC")
        print("[5] FLAC")
        print("[6] OGG (Vorbis)")
        print("[7] OPUS")

        choice = input("Enter an audio format choice: ").strip()
        codec_map = {
            "1": "mp3",
            "2": "wav",
            "3": "m4a",
            "4": "aac",
            "5": "flac",
            "6": "vorbis",
            "7": "opus",
        }

        if choice in codec_map:
            return codec_map[choice]

        print("Invalid audio format choice. Please choose 1-7.")


def ask_video_container() -> str:
    while True:
        print("\nChoose a video format:")
        print("[1] MP4")
        print("[2] MKV")
        print("[3] WebM")

        choice = input("Enter a video format choice: ").strip() or "1"
        container_map = {
            "1": "mp4",
            "2": "mkv",
            "3": "webm",
        }

        if choice in container_map:
            return container_map[choice]

        print("Invalid video format choice. Please choose 1-3.")


def show_download_progress(progress: dict) -> None:
    if progress.get("status") == "downloading":
        downloaded = progress.get("downloaded_bytes") or 0
        total = progress.get("total_bytes") or progress.get("total_bytes_estimate")
        percentage = f"{min(downloaded / total, 1) * 100:.1f}%" if total else "--"
        eta = progress.get("eta")
        eta_text = "calculating..." if eta is None else f"{int(eta) // 60:02d}:{int(eta) % 60:02d}"

        print(f"\r{percentage} | ETA: {eta_text}"
    elif progress.get("status") in {"finished", "error"}:
        print()


def download_media(
    url: str,
    media_type: str,
    quality: str = "best",
    video_container: str = "mp4",
    audio_format: str = "mp3",
) -> None:
    download_path = get_download_path()

    if media_type == "video":
        ydl_opts = {
            "format": get_video_format(quality, video_container),
            "outtmpl": str(download_path / "%(title)s.%(ext)s"),
            "noplaylist": True,
            "noprogress": True,
            "progress_hooks": [show_download_progress],
        }
        if is_ffmpeg_installed():
            ydl_opts["merge_output_format"] = video_container
            ydl_opts["remuxvideo"] = video_container
        success_message = "Video download complete!"
    elif media_type == "audio":
        if not is_ffmpeg_installed():
            print(
                "\nAudio download failed: FFmpeg is not installed. "
                "Install FFmpeg and make sure it is available on PATH to "
                "convert audio to the selected format."
            )
            return
        ydl_opts = {
            "format": get_audio_format(quality),
            "outtmpl": str(download_path / "%(title)s.%(ext)s"),
            "noplaylist": True,
            "noprogress": True,
            "progress_hooks": [show_download_progress],
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": "0",
            }],
        }
        success_message = f"{audio_format.upper()} audio download complete!"
    else:
        raise ValueError(f"Invalid media type: {media_type}")

    try:
        print(f"\nSaving to: {download_path}")
        if media_type == "video":
            print(f"Quality: {quality.upper()}")
            print(f"Video format: {video_container.upper()}\n")
            if not is_ffmpeg_installed():
                print(
                    "Note: FFmpeg was not found. Only videos already available "
                    "with audio in the selected format can be downloaded.\n"
                )
        else:
            print(f"Audio quality: {quality.upper()}\n")
            print(f"Audio format: {audio_format.upper()}\n")
        print("Starting download...\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"\n{success_message}")
    except Exception as error:
        print(f"\nDownload failed: {error}")


def ask_choice() -> str:
    while True:
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice in {"1", "2", "3"}:
            return choice

        print("Invalid choice. Please choose 1, 2, or 3.")


def ask_video_quality() -> str:
    while True:
        print("\nChoose video quality:")
        print("[1] Best")
        print("[2] 1080p")
        print("[3] 720p")
        print("[4] 480p")
        print("[5] 360p")

        choice = input("Enter a quality choice: ").strip()

        quality_map = {
            "1": "best",
            "2": "1080p",
            "3": "720p",
            "4": "480p",
            "5": "360p",
        }

        if choice in quality_map:
            return quality_map[choice]

        print("Invalid quality choice. Please choose 1-5.")


def ask_audio_quality() -> str:
    while True:
        print("\nChoose audio quality:")
        print("[1] Best")
        print("[2] Low (<=64kbps)")
        print("[3] Medium (<=128kbps)")
        print("[4] High (<=192kbps)")

        choice = input("Enter an audio quality choice: ").strip()

        quality_map = {
            "1": "best",
            "2": "low",
            "3": "medium",
            "4": "high",
        }

        if choice in quality_map:
            return quality_map[choice]

        print("Invalid audio quality choice. Please choose 1-4.")


def prompt_for_url() -> str:
    url = input("Enter URL: ").strip()
    if not url:
        print("URL cannot be empty.")
        return ""
    return url


def main() -> None:
    while True:
        print(ascii_art())
        choice = ask_choice()

        if choice == "3":
            print("Thank you! Exiting.")
            break

        url = prompt_for_url()
        if not url:
            continue

        if choice == "1":
            quality = ask_video_quality()
            video_container = ask_video_container()
            download_media(url, "video", quality=quality, video_container=video_container)
        elif choice == "2":
            audio_format = get_audio_codec_choice()
            audio_quality = ask_audio_quality()
            download_media(url, "audio", quality=audio_quality, audio_format=audio_format)

        again = input("Download another file? (y/n): ").strip().lower()
        if again not in {"y", "yes"}:
            print("Thank you! Exiting.")
            break


if __name__ == "__main__":
    main()
