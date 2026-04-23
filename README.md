# ✂️ Clipper Maker

> **AI-powered YouTube clip extractor — paste a URL, get the best moments automatically.**

Built with Python, OpenAI Whisper, librosa, ffmpeg, and Streamlit.

---

## 🎬 What It Does

Clipper Maker takes any YouTube video URL and automatically finds the most highlight-worthy moments using AI audio analysis and speech transcription — then exports them as clean, ready-to-share MP4 clips through a simple web interface.

No manual scrubbing. No guesswork. Just great clips.

---

## ✨ Features

- 📥 **YouTube Downloader** — supports any public YouTube video via yt-dlp
- 🎙️ **AI Transcription** — powered by OpenAI Whisper (runs fully offline)
- 🔍 **Smart Clip Detection** — scores segments by audio energy + speech density
- ✂️ **Auto Export** — cuts and encodes clips with ffmpeg
- 🌐 **Web UI** — clean Streamlit interface with live progress tracking
- 📦 **Bulk Download** — download all clips as a single ZIP file

---

## 🖥️ Demo

```
Paste YouTube URL → AI analyzes video → Top 5 clips exported → Download in one click
```

---

## 🗂️ Project Structure

```
clipper-maker/
├── app.py                  # Streamlit web UI
├── requirements.txt        # Python dependencies
├── core/
│   ├── downloader.py       # YouTube video downloader (yt-dlp)
│   ├── transcriber.py      # Audio transcription (Whisper)
│   ├── analyzer.py         # Clip scoring & selection (librosa)
│   └── clipper.py          # Video cutting & export (ffmpeg)
└── utils/
    └── helpers.py          # Utility functions
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.9+
- ffmpeg installed and added to PATH

**Install ffmpeg (Windows):**
1. Download from [gyan.dev/ffmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your System PATH

**Install ffmpeg (Mac):**
```bash
brew install ffmpeg
```

**Install ffmpeg (Linux):**
```bash
sudo apt install ffmpeg
```

---

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Dinushka110797/clipper-maker.git
cd clipper-maker

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
streamlit run app.py
```

Then open your browser at **http://localhost:8501**

1. Paste any YouTube URL
2. Adjust settings in the sidebar (clip count, padding, Whisper model)
3. Hit **Generate Clips**
4. Preview and download your clips

---

## 🧠 How the AI Works

| Step | Module | Technology | What happens |
|------|--------|------------|-------------|
| 1 | `downloader.py` | yt-dlp | Video downloaded as MP4 |
| 2 | `transcriber.py` | OpenAI Whisper | Audio converted to timestamped text |
| 3 | `analyzer.py` | librosa + numpy | Each segment scored by energy & speech |
| 4 | `clipper.py` | ffmpeg | Best segments cut and exported |

**Scoring formula:**
```
score = (RMS energy × 3.0) + (speech density × 0.5) + (text length bonus × 0.3)
```

---

## ⚙️ Settings

| Setting | Default | Description |
|---------|---------|-------------|
| Number of clips | 5 | How many clips to extract |
| Clip padding | 2s | Extra seconds added before/after each clip |
| Min gap between clips | 10s | Prevents clips from being too close together |
| Whisper model | base | `tiny` (fast) / `base` (balanced) / `small` (accurate) |

---

## 📦 Dependencies

```
yt-dlp          — YouTube video downloader
openai-whisper  — Speech-to-text transcription
librosa         — Audio analysis
ffmpeg-python   — Video processing interface
streamlit       — Web UI framework
torch           — Neural network backend for Whisper
numpy           — Numerical computing
```

---

## 🪪 License

MIT License — free to use, modify, and share.

---

## 👨‍💻 Author

**Dinushka** — [@Dinushka110797](https://github.com/Dinushka110797)

> Built from scratch in a single session. Every line written with purpose. 🚀
