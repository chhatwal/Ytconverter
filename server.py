import os
import re
import threading
import uuid
import shutil
from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import yt_dlp

BASE_DIR = Path(__file__).parent.resolve()
app = Flask(__name__, static_folder=str(BASE_DIR))
CORS(app)

DOWNLOAD_DIR = BASE_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

jobs = {}

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def cleanup_old_files():
    """Delete files older than 1 hour to save disk space on Render."""
    import time
    now = time.time()
    for f in DOWNLOAD_DIR.glob("*"):
        if f.is_file() and (now - f.stat().st_mtime) > 3600:
            try:
                f.unlink()
            except:
                pass

def run_download(job_id, url, fmt, quality):
    cleanup_old_files()
    jobs[job_id]["status"] = "downloading"
    jobs[job_id]["progress"] = 5

    def progress_hook(d):
        if d["status"] == "downloading":
            pct = d.get("_percent_str", "0%").strip().replace("%", "")
            try:
                jobs[job_id]["progress"] = min(88, max(5, int(float(pct))))
                jobs[job_id]["speed"] = d.get("_speed_str", "").strip()
                jobs[job_id]["eta"] = d.get("_eta_str", "").strip()
            except:
                pass
        elif d["status"] == "finished":
            jobs[job_id]["progress"] = 90
            jobs[job_id]["status"] = "converting"

    output_template = str(DOWNLOAD_DIR / f"{job_id}_%(title)s.%(ext)s")
    base_opts = {
        "outtmpl": output_template,
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        if fmt == "mp3":
            ydl_opts = {
                **base_opts,
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": quality,
                }],
            }
            out_ext = "mp3"
        else:
            height = quality.replace("p", "")
            ydl_opts = {
                **base_opts,
                "format": f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best",
                "merge_output_format": "mp4",
            }
            out_ext = "mp4"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video")
            thumb = info.get("thumbnail", "")
            duration = info.get("duration", 0)
            channel = info.get("uploader", "")

        jobs[job_id]["progress"] = 95

        found = list(DOWNLOAD_DIR.glob(f"{job_id}_*.{out_ext}"))
        if not found:
            found = sorted(DOWNLOAD_DIR.glob(f"{job_id}_*"),
                           key=lambda f: f.stat().st_size, reverse=True)

        if found:
            filepath = found[0]
            actual_ext = filepath.suffix.lstrip(".")
            jobs[job_id].update({
                "status": "done", "progress": 100,
                "filename": filepath.name, "title": title,
                "thumbnail": thumb, "duration": duration,
                "channel": channel,
                "size_mb": round(filepath.stat().st_size / (1024 * 1024), 2),
                "ext": actual_ext,
            })
        else:
            jobs[job_id].update({"status": "error",
                                  "error": "Output file not found after download."})
    except Exception as e:
        jobs[job_id].update({"status": "error", "error": str(e)})


@app.route("/")
def index():
    return send_from_directory(str(BASE_DIR), "index.html")


@app.route("/info", methods=["POST"])
def get_info():
    data = request.json
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
            info = ydl.extract_info(url, download=False)
        return jsonify({
            "title": info.get("title", ""),
            "thumbnail": info.get("thumbnail", ""),
            "duration": info.get("duration", 0),
            "channel": info.get("uploader", ""),
            "view_count": info.get("view_count", 0),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/convert", methods=["POST"])
def convert():
    data = request.json
    url = data.get("url", "").strip()
    fmt = data.get("format", "mp3")
    quality = data.get("quality", "192")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {"status": "queued", "progress": 0}
    t = threading.Thread(target=run_download, args=(job_id, url, fmt, quality))
    t.daemon = True
    t.start()
    return jsonify({"job_id": job_id})


@app.route("/progress/<job_id>")
def progress(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)


@app.route("/download/<job_id>")
def download(job_id):
    job = jobs.get(job_id)
    if not job or job.get("status") != "done":
        return jsonify({"error": "File not ready"}), 404
    filepath = DOWNLOAD_DIR / job["filename"]
    if not filepath.exists():
        return jsonify({"error": "File missing"}), 404
    ext = job.get("ext", "mp3")
    mime_map = {"mp3": "audio/mpeg", "mp4": "video/mp4",
                "m4a": "audio/mp4", "webm": "audio/webm"}
    mime = mime_map.get(ext, "application/octet-stream")
    safe_name = sanitize_filename(job.get("title", "download")) + f".{ext}"
    return send_file(filepath, mimetype=mime, as_attachment=True, download_name=safe_name)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n🎵 YT Converter running on port {port}")
    app.run(debug=False, host="0.0.0.0", port=port, threaded=True)
