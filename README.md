# 🎵 YTDown — YouTube MP3 & MP4 Converter

A beautiful, fully local YouTube downloader powered by **yt-dlp** and **Flask**.

---

## ⚡ Quick Start (3 steps)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

> You also need **ffmpeg** installed on your system:
> - **Mac**: `brew install ffmpeg`
> - **Windows**: Download from https://ffmpeg.org/download.html and add to PATH
> - **Linux**: `sudo apt install ffmpeg`

### 2. Run the server
```bash
python server.py
```

### 3. Open your browser
```
http://localhost:5000
```

---

## 🎬 How to use

1. Paste a YouTube URL (e.g. `https://www.youtube.com/watch?v=JRLmQDhfczg`)
2. Click **Preview** to see video info
3. Choose **MP3** (audio) or **MP4** (video)
4. Pick your quality (up to 320kbps / 1080p)
5. Click **Convert & Download**
6. Wait for the progress bar — then click **Download File**

---

## 📁 File locations

Downloaded files are saved in the `downloads/` folder next to `server.py`.

---

## 🔧 Features

- ✅ MP3 up to 320kbps
- ✅ MP4 up to 1080p
- ✅ Live progress bar with speed & ETA
- ✅ Video preview before converting
- ✅ 100% local — no data sent anywhere
- ✅ Dark mode UI

---

## ⚠️ Legal Note

For personal use only. Respect YouTube's Terms of Service and copyright laws.
Do not download content you do not have rights to.
