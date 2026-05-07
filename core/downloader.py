import yt_dlp
import os

def download_video(url: str, output_dir: str = "temp") -> str:
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": False,
        "no_warnings": False,
        "nocheckcertificate": True,
        "extractor_retries": 3,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate",
        },
        "compat_opts": {"no-youtube-unavailable-videos"},
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    if not filename.endswith(".mp4"):
        filename = os.path.splitext(filename)[0] + ".mp4"

    print(f"\n✅ Downloaded: {filename}")
    return filename


def get_video_info(url: str) -> dict:
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-us,en;q=0.5",
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "uploader": info.get("uploader"),
        }
