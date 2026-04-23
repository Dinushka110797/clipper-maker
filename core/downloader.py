import yt_dlp
import os

def download_video(url: str, output_dir: str = "temp") -> str:
    """
    Downloads a YouTube video and returns the file path.
    """
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": False,
        "no_warnings": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "video")
        ext = info.get("ext", "mp4")
        filename = ydl.prepare_filename(info)

    # Normalize extension to .mp4
    if not filename.endswith(".mp4"):
        filename = os.path.splitext(filename)[0] + ".mp4"

    print(f"\n✅ Downloaded: {filename}")
    return filename


def get_video_info(url: str) -> dict:
    """
    Fetches video metadata without downloading.
    """
    ydl_opts = {"quiet": True, "skip_download": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "duration": info.get("duration"),  # in seconds
            "thumbnail": info.get("thumbnail"),
            "uploader": info.get("uploader"),
        }