# 🚗 Real-Time Road Anomaly Detection on Raspberry Pi (Edge AI)

This project implements a **real-time road anomaly detection system** on **Raspberry Pi 5** using a lightweight **YOLO object detection model** optimized for **CPU-only inference**.  
The system processes dashcam footage, detects road anomalies (potholes, speed bumps, damaged roads, obstacles), logs detections with timestamps, and automatically saves short video clips for each anomaly.

---

## 🎯 Objective

Build an **edge AI application** that:
- Runs fully on Raspberry Pi 5 CPU (no GPU / accelerators)
- Detects road anomalies in real-time
- Logs detection events
- Saves short video clips around each anomaly
- Achieves near real-time performance (≥ 5 FPS)

---

## 🧠 Features

- ✅ Real-time anomaly detection using YOLO (NCNN backend)
- ✅ Supports USB webcam, Pi Camera, or video file input
- ✅ Pre-event & post-event clip recording
- ✅ Asynchronous video saving using FFmpeg (non-blocking)
- ✅ FPS overlay for performance monitoring
- ✅ Date-wise automatic clip organization
- ✅ CSV logging with timestamp, class name & confidence
- ✅ CPU-only optimized inference for Raspberry Pi 5

---

## 🛠 Tech Stack

**Hardware**
- Raspberry Pi 5  
- Raspberry Pi Camera Module Rev1.3 or USB webcam  
- High-speed microSD card  

**Software**
- Raspberry Pi OS  
- Python 3.13  
- OpenCV  
- Ultralytics YOLO  
- NCNN (edge-optimized runtime)  
- FFmpeg  

---

## 📁 Project Structure

.
├── best_ncnn_model/ # Optimized YOLO model (NCNN format)
├── videos/ # Input test videos
├── clips/ # Saved anomaly clips (date-wise)
├── logs/
│ └── anomaly_log.csv # Detection logs
├── rt_det_pi5.py # Main inference pipeline
└── README.md


---

## ⚙️ Installation

### 1️⃣ Install dependencies
```bash
sudo apt update
sudo apt install -y ffmpeg python3-opencv
pip install ultralytics

2️⃣ Clone the repo

git clone https://github.com/your-username/road-anomaly-detection-rpi.git
cd road-anomaly-detection-rpi

▶️ Usage

Edit source in main.py:

SOURCE = "videos/vid1.mp4"   # or "usb0" or "picamera0"

Run:

python3 main.py

Press Q to quit safely.
🧪 Example Output

    Live Detection Window with bounding boxes and FPS overlay

    Saved MP4 clips in:

    clips/YYYY-MM-DD/

    CSV log file:

    logs/anomaly_log.csv

Example CSV:

timestamp,class,confidence(%),clip
2026-02-06 18:30:12,RoadDamage,92.4,clips/2026-02-06/RoadDamage_18-30-12.mp4

⚡ Performance
Device	Backend	FPS (Approx)
Raspberry Pi 5	YOLO-NCNN (INT8)	7–15 FPS

    Achieves near real-time performance on CPU-only setup.

📌 Supported Anomaly Classes

    🕳️ Road Damage / Potholes

    🚧 Speed Bumps

    🛣️ Unsurfaced Roads

    🚶 Obstacles / Pedestrians

(Classes configurable in ANOMALY_CLASSES)

📈 Learning Outcomes

    Edge AI deployment on ARM devices

    Real-time video processing pipelines

    Model quantization & CPU optimization

    Accuracy vs speed trade-off analysis

    Practical embedded computer vision

📜 License

This project is for educational and research purposes.


🙌 Acknowledgements

    Ultralytics YOLO
    NCNN Runtime
    OpenCV
    FFmpeg

📬 Author

Mohd Nouman Ahmed
ECE / Embedded AI Project
2026