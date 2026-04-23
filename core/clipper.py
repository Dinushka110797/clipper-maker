import subprocess
import os

def export_clip(video_path: str, start: float, end: float, output_path: str, padding: float = 2.0) -> str:
    """
    Exports a single clip from a video using ffmpeg.
    Adds padding before/after for better context.
    """
    # Add padding but clamp to valid range
    clip_start = max(0, start - padding)
    clip_end = end + padding
    duration = clip_end - clip_start

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    command = [
        "ffmpeg",
        "-y",                        # overwrite output
        "-ss", str(clip_start),      # start time
        "-i", video_path,            # input file
        "-t", str(duration),         # duration
        "-c:v", "libx264",           # video codec
        "-c:a", "aac",               # audio codec
        "-preset", "fast",           # encoding speed
        "-crf", "23",                # quality (lower = better)
        output_path
    ]

    print(f"  ✂️  Exporting: {os.path.basename(output_path)} [{clip_start:.1f}s → {clip_end:.1f}s]")

    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if result.returncode != 0:
        print(f"  ❌ Failed to export: {output_path}")
        return None

    size_kb = os.path.getsize(output_path) // 1024
    print(f"  ✅ Done — {size_kb} KB")
    return output_path


def export_all_clips(video_path: str, clips: list, output_dir: str = "output", padding: float = 2.0) -> list:
    """
    Exports all selected clips to the output directory.
    Returns list of output file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    exported = []

    # Get base name of video (without extension)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    # Sanitize filename
    base_name = "".join(c for c in base_name if c.isalnum() or c in (" ", "-", "_")).strip()
    base_name = base_name[:40]  # limit length

    print(f"\n🎬 Exporting {len(clips)} clips to '{output_dir}/'")

    for i, clip in enumerate(clips):
        output_path = os.path.join(output_dir, f"clip_{i+1:02d}_{int(clip['start'])}s.mp4")
        result = export_clip(video_path, clip["start"], clip["end"], output_path, padding)
        if result:
            exported.append({
                "path": result,
                "start": clip["start"],
                "end": clip["end"],
                "text": clip["text"],
                "score": clip["score"]
            })

    print(f"\n🎉 Successfully exported {len(exported)}/{len(clips)} clips!")
    return exported