from flask import Flask, request, render_template, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        format_choice = request.form["format"]
        unique_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.%(ext)s")

        ydl_opts = {
            "outtmpl": output_template,
            "format": "bestaudio/best" if format_choice == "mp3" else "best",
        }

        if format_choice == "mp3":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                return f"Error: {e}"

        # Find the output file
        for ext in ["mp3", "mp4", "mkv", "webm"]:
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.{ext}")
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)

        return "Download failed. Please try again."

    return render_template("index.html")