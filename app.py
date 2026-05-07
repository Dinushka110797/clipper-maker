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
    page_title="Clipper Maker — by S.D.L.W.Silva",
    page_icon="✂️",
    layout="centered"
)

# ─── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

  /* Global font */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
  }

  /* Dark background */
  .stApp {
    background: linear-gradient(135deg, #07070f 0%, #0e0e1a 50%, #07070f 100%);
  }

  /* Hide default Streamlit header */
  header[data-testid="stHeader"] { background: transparent; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #0e0e1a !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
  }
  [data-testid="stSidebar"] * { color: #ededf5 !important; }

  /* Buttons */
  .stButton > button {
    background: linear-gradient(135deg, #7c6fff, #6d28d9) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 14px 28px !important;
    width: 100% !important;
    box-shadow: 0 0 24px rgba(124,111,255,0.35) !important;
    transition: all 0.2s !important;
    letter-spacing: 0.3px !important;
  }
  .stButton > button:hover {
    box-shadow: 0 0 40px rgba(124,111,255,0.6) !important;
    transform: translateY(-1px) !important;
  }

  /* Download buttons */
  .stDownloadButton > button {
    background: #14141f !important;
    color: #a78bfa !important;
    border: 1px solid rgba(124,111,255,0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
  }
  .stDownloadButton > button:hover {
    background: rgba(124,111,255,0.1) !important;
    border-color: #7c6fff !important;
  }

  /* Text input */
  .stTextInput > div > div > input {
    background: #13131e !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #ededf5 !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #7c6fff !important;
    box-shadow: 0 0 0 2px rgba(124,111,255,0.2) !important;
  }

  /* Expander */
  .streamlit-expanderHeader {
    background: #13131e !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #ededf5 !important;
    font-weight: 600 !important;
  }
  .streamlit-expanderContent {
    background: #0e0e1a !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 0 0 12px 12px !important;
  }

  /* Success / Error */
  .stSuccess {
    background: rgba(74,222,128,0.1) !important;
    border: 1px solid rgba(74,222,128,0.3) !important;
    border-radius: 12px !important;
    color: #4ade80 !important;
  }
  .stError {
    background: rgba(248,113,113,0.1) !important;
    border: 1px solid rgba(248,113,113,0.3) !important;
    border-radius: 12px !important;
  }

  /* Divider */
  hr { border-color: rgba(255,255,255,0.08) !important; }

  /* Selectbox */
  .stSelectbox > div > div {
    background: #13131e !important;
    border-color: rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #ededf5 !important;
  }

  /* Slider */
  .stSlider > div > div > div > div {
    background: #7c6fff !important;
  }

  /* Header top bar */
  .top-bar {
    background: linear-gradient(90deg, #0e0e1a, #13131e, #0e0e1a);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    padding: 10px 0;
    text-align: center;
    font-size: 12px;
    color: #6b6b80;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
  }
  .top-bar span { color: #7c6fff; font-weight: 600; }

  /* Hero section */
  .hero-box {
    background: linear-gradient(135deg, #0e0e1a 0%, #13131e 100%);
    border: 1px solid rgba(124,111,255,0.2);
    border-radius: 24px;
    padding: 40px 36px 32px 36px;
    text-align: center;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
  }
  .hero-glow {
    position: absolute; top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 300px; height: 200px;
    background: radial-gradient(ellipse, rgba(124,111,255,0.15) 0%, transparent 70%);
    pointer-events: none;
  }
  .hero-title {
    font-size: 42px; font-weight: 900;
    letter-spacing: -1.5px; line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 30%, #a78bfa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
  }
  .hero-sub {
    font-size: 15px; color: #6b6b80; line-height: 1.7;
    max-width: 480px; margin: 0 auto 20px auto;
  }
  .hero-sub strong { color: #a78bfa; }
  .hero-pills {
    display: flex; justify-content: center;
    flex-wrap: wrap; gap: 8px; margin-bottom: 8px;
  }
  .pill {
    font-size: 11px; font-weight: 600;
    padding: 5px 13px; border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.1);
    color: #888899; background: rgba(255,255,255,0.04);
    letter-spacing: 0.3px;
  }
  .author-badge {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 11px; font-weight: 600;
    color: #7c6fff; letter-spacing: 0.5px;
    padding: 5px 14px; border-radius: 999px;
    border: 1px solid rgba(124,111,255,0.25);
    background: rgba(124,111,255,0.08);
    margin-top: 12px;
  }

  /* Info card */
  .info-card {
    background: #0e0e1a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
  }
  .info-card h4 {
    font-size: 13px; font-weight: 700;
    color: #a78bfa; margin-bottom: 8px;
    text-transform: uppercase; letter-spacing: 1px;
  }

  /* Step badge */
  .step-badge {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 12px; font-weight: 700;
    padding: 4px 12px; border-radius: 999px;
    background: rgba(124,111,255,0.12);
    border: 1px solid rgba(124,111,255,0.25);
    color: #a78bfa; margin-bottom: 6px;
    letter-spacing: 0.5px;
  }

  /* Footer */
  .footer {
    text-align: center;
    padding: 32px 0 20px 0;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin-top: 48px;
  }
  .footer-name {
    font-size: 15px; font-weight: 700;
    color: #ededf5; margin-bottom: 4px;
    letter-spacing: -0.3px;
  }
  .footer-copy {
    font-size: 12px; color: #444455;
    margin-bottom: 8px;
  }
  .footer-links {
    display: flex; justify-content: center; gap: 16px;
    font-size: 12px;
  }
  .footer-links a { color: #7c6fff; text-decoration: none; }
  .footer-links a:hover { color: #a78bfa; }
  .footer-tag {
    font-size: 10px; color: #333344;
    margin-top: 8px; letter-spacing: 1px;
    text-transform: uppercase;
  }
</style>
""", unsafe_allow_html=True)

# ─── Top Bar ───────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
  ✂️ &nbsp;<span>Clipper Maker</span>&nbsp; — AI-Powered YouTube Clip Extractor &nbsp;|&nbsp;
  Built by <span>S.D.L.W.Silva</span>
</div>
""", unsafe_allow_html=True)

# ─── Hero Section ──────────────────────────────────────────
st.markdown("""
<div class="hero-box">
  <div class="hero-glow"></div>
  <div class="hero-title">✂️ Clipper Maker</div>
  <p class="hero-sub">
    Paste any YouTube URL and our AI automatically finds the
    <strong>best moments</strong> — powered by Whisper, librosa & ffmpeg.
  </p>
  <div class="hero-pills">
    <span class="pill">🎙️ Whisper AI</span>
    <span class="pill">🔍 Audio Analysis</span>
    <span class="pill">✂️ Auto Clipping</span>
    <span class="pill">📦 ZIP Export</span>
  </div>
  <div class="author-badge">👨‍💻 S.D.L.W.Silva</div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar Settings ──────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 16px 0 8px 0;">
      <div style="font-size:22px; margin-bottom:6px;">⚙️</div>
      <div style="font-size:15px; font-weight:800; color:#ededf5; letter-spacing:-0.5px;">Settings</div>
      <div style="font-size:11px; color:#6b6b80; margin-top:2px;">Customize your clips</div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.08); margin-bottom:16px;">
    """, unsafe_allow_html=True)

    num_clips    = st.slider("🎬 Number of clips",            min_value=1,  max_value=10, value=5)
    clip_padding = st.slider("⏱️ Padding per clip (seconds)", min_value=0,  max_value=10, value=2)
    min_gap      = st.slider("📏 Min gap between clips (s)",  min_value=5,  max_value=60, value=10)
    whisper_model= st.selectbox("🧠 Whisper model", ["tiny", "base", "small"], index=1)

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.08); margin: 16px 0;">
    <div style="font-size:11px; color:#6b6b80; line-height:1.8;">
      <b style="color:#a78bfa;">Model Guide:</b><br>
      ⚡ <b style="color:#ededf5;">tiny</b> — fastest, basic accuracy<br>
      ✅ <b style="color:#ededf5;">base</b> — balanced (recommended)<br>
      🎯 <b style="color:#ededf5;">small</b> — slower, more accurate
    </div>
    <hr style="border-color:rgba(255,255,255,0.08); margin: 16px 0;">
    <div style="text-align:center; font-size:11px; color:#444455;">
      © 2026 S.D.L.W.Silva<br>
      <span style="color:#333344;">All rights reserved</span>
    </div>
    """, unsafe_allow_html=True)

# ─── Main Input ────────────────────────────────────────────
url = st.text_input(
    "🔗 YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    help="Paste any public YouTube video URL"
)

if url:
    try:
        with st.spinner("🔍 Fetching video info..."):
            info = get_video_info(url)

        # Video preview card
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(info["thumbnail"], use_container_width=True)
        with col2:
            st.markdown(f"""
            <div style="padding: 8px 0;">
              <div style="font-size:16px; font-weight:800; color:#ededf5;
                          letter-spacing:-0.5px; margin-bottom:10px; line-height:1.4;">
                {info['title']}
              </div>
              <div style="font-size:13px; color:#6b6b80; margin-bottom:6px;">
                👤 <span style="color:#ededf5;">{info['uploader']}</span>
              </div>
              <div style="font-size:13px; color:#6b6b80;">
                ⏱️ Duration:
                <span style="color:#a78bfa; font-weight:600; font-family:monospace;">
                  {info['duration']//60}:{info['duration']%60:02d}
                </span>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        if st.button("🚀 Generate Clips — Let's Go!", use_container_width=True):

            # Step 1 — Download
            st.markdown('<div class="step-badge">📥 Step 1 of 4</div>', unsafe_allow_html=True)
            with st.status("📥 Downloading video...", expanded=True) as status:
                st.write("🌐 Connecting to YouTube...")
                video_path = download_video(url)
                st.write(f"✅ Downloaded: `{os.path.basename(video_path)}`")
                status.update(label="✅ Download complete!", state="complete")

            # Step 2 — Transcribe
            st.markdown('<div class="step-badge">🎙️ Step 2 of 4</div>', unsafe_allow_html=True)
            with st.status("🎙️ Transcribing audio with Whisper AI...", expanded=True) as status:
                st.write(f"🧠 Loading Whisper `{whisper_model}` model...")
                transcript = transcribe_video(video_path, model_size=whisper_model)
                st.write(f"✅ Detected **{transcript['language'].upper()}** — {len(transcript['segments'])} segments found")
                status.update(label="✅ Transcription complete!", state="complete")

            # Step 3 — Analyze
            st.markdown('<div class="step-badge">🔍 Step 3 of 4</div>', unsafe_allow_html=True)
            with st.status("🔍 Analyzing best moments...", expanded=True) as status:
                st.write("📊 Scoring segments by audio energy and speech density...")
                scored = analyze_audio(video_path, transcript["segments"])
                clips  = pick_best_clips(scored, num_clips=num_clips, min_gap=min_gap)
                st.write(f"✅ Selected top **{len(clips)} clips** from {len(scored)} scored segments")
                status.update(label="✅ Analysis complete!", state="complete")

            # Step 4 — Export
            st.markdown('<div class="step-badge">✂️ Step 4 of 4</div>', unsafe_allow_html=True)
            with st.status("✂️ Exporting clips with FFmpeg...", expanded=True) as status:
                st.write("🎬 Cutting and encoding video clips...")
                exported = export_all_clips(video_path, clips, padding=clip_padding)
                st.write(f"✅ Exported **{len(exported)} clips** successfully")
                status.update(label="✅ Export complete!", state="complete")

            # ─── Results ───────────────────────────────────────────
            st.success(f"🎉 Done! {len(exported)} clips are ready to download.")
            st.divider()

            st.markdown("""
            <div style="font-size:18px; font-weight:800; color:#ededf5;
                        letter-spacing:-0.5px; margin-bottom:16px;">
              📁 Your Clips
            </div>
            """, unsafe_allow_html=True)

            for i, clip in enumerate(exported):
                with st.expander(
                    f"✂️ Clip {i+1}  —  {int(clip['start'])}s → {int(clip['end'])}s  |  Score: {clip['score']}"
                ):
                    st.markdown(f"""
                    <div style="font-size:12px; color:#6b6b80; font-style:italic;
                                margin-bottom:12px; padding: 8px 12px;
                                background: rgba(124,111,255,0.06);
                                border-left: 2px solid #7c6fff;
                                border-radius: 0 8px 8px 0;">
                      📝 "{clip['text']}"
                    </div>
                    """, unsafe_allow_html=True)
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

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center; padding: 40px 20px; color:#444455;">
      <div style="font-size:48px; margin-bottom:12px;">🔗</div>
      <div style="font-size:14px; color:#6b6b80;">
        Paste a YouTube URL above to get started
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-name">S.D.L.W.Silva</div>
  <div class="footer-copy">© 2026 S.D.L.W.Silva — All Rights Reserved</div>
  <div class="footer-links">
    <a href="https://github.com/Dinushka110797" target="_blank">🐙 GitHub</a>
    <a href="https://www.linkedin.com/in/dinushka-silva-8302b22a7/" target="_blank">💼 LinkedIn</a>
    <a href="mailto:lakshandinushka929@gmail.com">✉️ Contact</a>
  </div>
  <div class="footer-tag">Clipper Maker v1.0 — Powered by Whisper AI · librosa · ffmpeg · Streamlit</div>
</div>
""", unsafe_allow_html=True)
