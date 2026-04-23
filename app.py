import streamlit as st
import os
import zipfile
import io

from core.downloader import download_video, get_video_info
from core.transcriber import transcribe_video
from core.analyzer import analyze_audio, pick_best_clips
from core.clipper import export_all_clips

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Clipper Maker",
    page_icon="✂️",
    layout="centered"
)

st.title("✂️ Clipper Maker")
st.caption("Paste a YouTube URL and get the best clips automatically — powered by AI.")

# ─── Sidebar Settings ──────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    num_clips = st.slider("Number of clips", min_value=1, max_value=10, value=5)
    clip_padding = st.slider("Padding per clip (seconds)", min_value=0, max_value=10, value=2)
    min_gap = st.slider("Min gap between clips (seconds)", min_value=5, max_value=60, value=10)
    whisper_model = st.selectbox("Whisper model", ["tiny", "base", "small"], index=1)
    st.markdown("---")
    st.markdown("**Model sizes:**")
    st.markdown("- `tiny` → fastest, less accurate")
    st.markdown("- `base` → balanced ✅")
    st.markdown("- `small` → slower, more accurate")

# ─── Main Input ────────────────────────────────────────────
url = st.text_input("🔗 YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        with st.spinner("Fetching video info..."):
            info = get_video_info(url)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(info["thumbnail"], use_container_width=True)
        with col2:
            st.subheader(info["title"])
            duration_min = info["duration"] // 60
            duration_sec = info["duration"] % 60
            st.markdown(f"👤 **{info['uploader']}**")
            st.markdown(f"⏱️ Duration: `{duration_min}:{duration_sec:02d}`")

        st.divider()

        if st.button("🚀 Generate Clips", use_width=True):

            # Step 1 — Download
            with st.status("📥 Downloading video...", expanded=True) as status:
                st.write("Connecting to YouTube...")
                video_path = download_video(url)
                st.write(f"✅ Downloaded: `{os.path.basename(video_path)}`")
                status.update(label="✅ Download complete!", state="complete")

            # Step 2 — Transcribe
            with st.status("🎙️ Transcribing audio...", expanded=True) as status:
                st.write(f"Loading Whisper `{whisper_model}` model...")
                transcript = transcribe_video(video_path, model_size=whisper_model)
                st.write(f"✅ Found {len(transcript['segments'])} segments in {transcript['language'].upper()}")
                status.update(label="✅ Transcription complete!", state="complete")

            # Step 3 — Analyze
            with st.status("🔍 Analyzing best moments...", expanded=True) as status:
                st.write("Scoring segments by energy and speech density...")
                scored = analyze_audio(video_path, transcript["segments"])
                clips = pick_best_clips(scored, num_clips=num_clips, min_gap=min_gap)
                st.write(f"✅ Selected top {len(clips)} clips")
                status.update(label="✅ Analysis complete!", state="complete")

            # Step 4 — Export
            with st.status("✂️ Exporting clips...", expanded=True) as status:
                st.write("Cutting and encoding clips with FFmpeg...")
                exported = export_all_clips(video_path, clips, padding=clip_padding)
                st.write(f"✅ Exported {len(exported)} clips")
                status.update(label="✅ Export complete!", state="complete")

            # ─── Results ───────────────────────────────────────────
            st.success(f"🎉 Done! {len(exported)} clips ready.")
            st.divider()
            st.subheader("📁 Your Clips")

            for i, clip in enumerate(exported):
                with st.expander(f"Clip {i+1} — {int(clip['start'])}s to {int(clip['end'])}s | Score: {clip['score']}"):
                    st.caption(f"📝 *\"{clip['text']}\"*")
                    with open(clip["path"], "rb") as f:
                        st.video(f.read())
                    with open(clip["path"], "rb") as f:
                        st.download_button(
                            label=f"⬇️ Download Clip {i+1}",
                            data=f,
                            file_name=os.path.basename(clip["path"]),
                            mime="video/mp4",
                            key=f"dl_{i}"
                        )

            # ─── ZIP Download ──────────────────────────────────────
            st.divider()
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for clip in exported:
                    zf.write(clip["path"], os.path.basename(clip["path"]))
            zip_buffer.seek(0)

            st.download_button(
                label="📦 Download All Clips as ZIP",
                data=zip_buffer,
                file_name="clips.zip",
                mime="application/zip"
            )

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")