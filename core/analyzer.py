import librosa
import numpy as np

def analyze_audio(video_path: str, segments: list, clip_duration: int = 30) -> list:
    """
    Scores each transcript segment based on audio energy and speech density.
    Returns segments sorted by score (best first).
    """
    print(f"\n🔍 Analyzing audio: {video_path}")

    # Load audio from video
    y, sr = librosa.load(video_path, sr=None, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    print(f"⏱️ Video duration: {duration:.1f}s | Sample rate: {sr}Hz")

    scored_segments = []

    for seg in segments:
        start = seg["start"]
        end = seg["end"]
        text = seg["text"]

        # Skip very short segments
        if (end - start) < 1.0:
            continue

        # Extract audio slice for this segment
        start_sample = int(start * sr)
        end_sample = int(min(end * sr, len(y)))
        audio_slice = y[start_sample:end_sample]

        if len(audio_slice) == 0:
            continue

        # Score 1: RMS energy (louder = more exciting)
        rms = float(np.sqrt(np.mean(audio_slice ** 2)))

        # Score 2: Speech density (more words per second = content-rich)
        words = len(text.split())
        seg_duration = max(end - start, 0.1)
        speech_density = words / seg_duration

        # Score 3: Text length bonus (longer speech = more meaningful)
        text_bonus = min(len(text) / 100.0, 1.0)

        # Combined score (weighted)
        score = (rms * 3.0) + (speech_density * 0.5) + (text_bonus * 0.3)

        scored_segments.append({
            "start": start,
            "end": end,
            "text": text,
            "score": round(score, 4),
            "rms": round(rms, 4),
            "speech_density": round(speech_density, 4),
        })

    # Sort by score descending
    scored_segments.sort(key=lambda x: x["score"], reverse=True)

    print(f"✅ Scored {len(scored_segments)} segments")
    return scored_segments


def pick_best_clips(scored_segments: list, num_clips: int = 5, min_gap: float = 10.0) -> list:
    """
    Picks the top N non-overlapping clips from scored segments.
    min_gap ensures clips are spread across the video.
    """
    selected = []
    used_times = []

    for seg in scored_segments:
        if len(selected) >= num_clips:
            break

        # Check overlap with already selected clips
        overlap = False
        for used_start, used_end in used_times:
            if not (seg["end"] < used_start - min_gap or seg["start"] > used_end + min_gap):
                overlap = True
                break

        if not overlap:
            selected.append(seg)
            used_times.append((seg["start"], seg["end"]))

    # Sort selected clips by time order
    selected.sort(key=lambda x: x["start"])

    print(f"\n🎯 Selected {len(selected)} best clips:")
    for i, clip in enumerate(selected):
        print(f"  Clip {i+1}: [{clip['start']:.1f}s → {clip['end']:.1f}s] score={clip['score']} | \"{clip['text'][:50]}\"")

    return selected