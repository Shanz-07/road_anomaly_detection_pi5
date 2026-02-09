# 🚗 Real-Time Road Anomaly Detection on Raspberry Pi (Edge AI)

This repository implements a lightweight, CPU-only YOLO-based road anomaly detector designed to run on Raspberry Pi 5. The system processes camera or video input, detects road anomalies (potholes, speed bumps, damaged/unsurfaced roads, obstacles), logs events, and saves short MP4 clips around detected anomalies.

---

## 🎯 Objective

Run a practical edge-AI pipeline that:
- Runs on Raspberry Pi 5 CPU (no GPU required)
- Detects road anomalies in near real-time
- Logs detection events to a CSV
- Saves pre- and post-event video clips
- Provides a live preview and FPS overlay for monitoring

---

## 🔧 Folder Structure

- Main entrypoint: `main_pi5.py` (update config values at the top of this file)
- Model folder: `best_ncnn_model/` (NCNN-optimized YOLO files)
- Logs: `logs/anomaly_log.csv` (auto-created with header if missing)
- Saved clips: `clips/YYYY-MM-DD/<class>_HH-MM-SS.mp4`

---

## 🧠 Features

- Real-time detection using Ultralytics YOLO
- Supports USB webcam, Raspberry Pi Camera (Picamera2), or prerecorded video files
- Pre-event and post-event buffering (configurable)
- Asynchronous saving with FFmpeg (non-blocking via a worker thread)
- FPS overlay and live preview (toggleable)
- CSV logging with timestamp, class name, confidence, and clip path

---

## 🛠 Tech Stack

- Hardware: Raspberry Pi 5, USB webcam or Raspberry Pi Camera Module
- Software: Raspberry Pi OS, Python 3.13, OpenCV, Ultralytics YOLO, .pt converted <to> NCNN runtime for optimized frames, FFmpeg

---

## 📁 Project structure (relevant files)

.
├── best_ncnn_model/        # Optimized YOLO model (NCNN format)
├── videos/                 # Example input videos
├── clips/                  # Saved clips (organized by date)
├── logs/                   # Logs folder
│   └── anomaly_log.csv     # Detection log (auto-created)
├── main_pi5.py             # Main inference and recording pipeline
└── README.md

---

## ⚙️ Installation

1. Create and activate a Python virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate    # Linux / macOS
# On Windows (PowerShell): .\venv\Scripts\Activate.ps1
# On Windows (cmd): venv\Scripts\activate
```

Upgrade pip and tooling inside the venv:

```bash
pip install --upgrade pip setuptools wheel
```

2. Install system dependencies:

```bash
sudo apt update
sudo apt install -y ffmpeg python3-opencv
```

3. Install Python packages (inside the activated venv):

```bash
pip install ultralytics
# Optional: install any NCNN Python wrapper if required by your workflow
```

Note: If you plan to use Picamera2, install Picamera2 and follow Raspberry Pi OS instructions for camera support.

---

## ▶️ Usage

1. Open `main_pi5.py` and configure the top-level settings:
- `SOURCE` — path to a video file, or `usb0`, `usb1`, etc., or `picamera0`
- `MODEL_PATH` — model folder (default `best_ncnn_model`)
- `CONF_THRESH` — detection confidence threshold
- `ANOMALY_CLASSES` — list of class indices considered anomalies
- `PRE_BUFFER_SECONDS` / `POST_BUFFER_SECONDS` — number of seconds kept before/after an event
- `SHOW_PREVIEW` / `SHOW_FPS` — toggle preview and FPS overlay

2. Run the script:

```bash
python3 main_pi5.py
```

3. Interact:
- Press `Q` in the preview window to request a clean exit. The script waits to finish writing any in-progress clip before shutting down.

---

## 🔎 How saving & logging works

- The script maintains a fixed-length in-memory `frame_buffer` for pre-event frames and accumulates post-event frames after a detection triggers.
- When the configured post-event buffer is reached, frames are sent to a separate worker thread that calls `ffmpeg` to write an MP4 (non-blocking for detection).
- Saved clips are placed in `clips/YYYY-MM-DD/` and the path is appended to `logs/anomaly_log.csv` along with timestamp, class name and confidence.

---

## ⚠️ Notes & Troubleshooting

- If the source FPS cannot be read from a video/camera, the script falls back to a sensible default (25 for file/USB, 30 for Picamera2).
- Ensure `ffmpeg` is installed and available in PATH for MP4 writing.
- If running on Pi Camera, ensure Picamera2 is installed and the camera is enabled.
- If FPS or performance is lower than expected, try lowering the input resolution or using a more optimized/int8 model.

---

## 📌 Default anomaly classes (configurable in `ANOMALY_CLASSES` in `main_pi5.py`)

- Road Damage / Potholes
- Speed Bumps
- Unsurfaced / Damaged Roads
- Obstacles / Pedestrians

---

## 📈 Performance (example)

Device | Backend | FPS (approx)
---|---:|---:
Raspberry Pi 5 | YOLO-NCNN (INT8) | ~7–15 FPS (depends on model & resolution)

---

## 📜 License

This project is provided for educational and research purposes.

---

## 🙌 Acknowledgements

- Ultralytics YOLO
- NCNN runtime (optional)
- OpenCV
- FFmpeg

---

## 📬 Author

Mohd Nouman Ahmed
ECE / Embedded AI Project
2026