from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

# إنشاء مجلد التخزين إذا لم يكن موجودًا
output_dir = "downloads"
os.makedirs(output_dir, exist_ok=True)


@app.route('/')
def home():
  return "Server is running!"


@app.route('/download')
def download_video():
  video_id = request.args.get('videoID')
  quality = request.args.get('quality', '720')

  if not video_id:
    return "Error: videoID parameter is missing.", 400

  # تحديد اسم الملف النهائي
  output_filename = f"{output_dir}/{video_id}.mp4"

  # أمر yt-dlp لتنزيل الفيديو ودمج الصوت والفيديو معاً
  cmd = [
      "yt-dlp",
      f"https://www.youtube.com/watch?v={video_id}",
      "-f",
      f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
      "-o",
      f"{output_dir}/{video_id}.%(ext)s",
      "--merge-output-format",
      "mp4",  # دمج الصوت والفيديو في ملف MP4
      "--no-post-overwrites",  # تجنب استبدال الملفات
      "--no-warnings"  # تقليل التحذيرات
  ]

  try:
    print(f"🔹 Running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
  except subprocess.CalledProcessError as e:
    return f"❌ Error downloading video: {str(e)}", 500

  # التأكد من وجود الملف بعد التنزيل
  if os.path.exists(output_filename):
    print(f"✅ Found file: {output_filename}")
    return send_file(output_filename, as_attachment=True)
  else:
    print(f"❌ ERROR: File not found -> {output_filename}")
    return "File not found after download.", 404


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
