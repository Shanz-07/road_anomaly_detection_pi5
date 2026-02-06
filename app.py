from flask import Flask, render_template, jsonify, request, redirect, session, send_file
import csv
import os

app = Flask(__name__)
app.secret_key = "change-this-secret"

LOG_FILE = "logs/anomaly_log.csv"
CLIPS_DIR = "clips"

USERNAME = "admin"
PASSWORD = "1234"

# -------- AUTH --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")

# -------- API --------
@app.route("/api/logs")
def api_logs():
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, newline="") as f:
            logs = list(csv.DictReader(f))
    return jsonify(logs)

@app.route("/api/stats")
def api_stats():
    stats = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, newline="") as f:
            for row in csv.DictReader(f):
                cls = row["class"]
                stats[cls] = stats.get(cls, 0) + 1
    return jsonify(stats)

@app.route("/api/clips")
def api_clips():
    clips = []
    if os.path.exists(CLIPS_DIR):
        for root, _, files in os.walk(CLIPS_DIR):
            for f in files:
                if f.endswith(".mp4"):
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, CLIPS_DIR)
                    clips.append(rel_path.replace("\\", "/"))
    clips.sort(reverse=True)
    return jsonify(clips)

@app.route("/api/delete_clip", methods=["POST"])
def api_delete_clip():
    name = request.json["name"]
    path = os.path.join(CLIPS_DIR, name)
    if os.path.exists(path):
        os.remove(path)
        return jsonify({"ok": True})
    return jsonify({"ok": False})

@app.route("/clips/<path:filename>")
def serve_clip(filename):
    path = os.path.join(CLIPS_DIR, filename)
    if not os.path.exists(path):
        return "Not found", 404
    return send_file(path, mimetype="video/mp4", as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)
