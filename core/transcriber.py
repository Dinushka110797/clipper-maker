import whisper
import os

def transcribe_video(video_path: str, model_size: str = "base") -> dict:
    """
    Transcribes audio from a video file using OpenAI Whisper.
    Returns a dict with full text and timestamped segments.
    """
    print(f"\n🎙️ Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)

    print(f"📝 Transcribing: {video_path}")
    result = model.transcribe(video_path, verbose=False)

    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": seg["start"],   # seconds
            "end": seg["end"],       # seconds
            "text": seg["text"].strip()
        })

    print(f"✅ Transcription complete — {len(segments)} segments found")
    return {
        "full_text": result["text"],
        "segments": segments,
        "language": result.get("language", "unknown")
    }