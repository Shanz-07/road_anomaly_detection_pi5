🚗 Real-Time Road Anomaly Detection on Raspberry Pi 5 (Edge AI)
Project for Bharat AI-SoC Student Challenge

Team: Embedded Minds | Category: ECE / Embedded AI

This repository implements a high-performance, CPU-optimized YOLO pipeline designed specifically for the ARM architecture of the Raspberry Pi 5. The system detects road anomalies (potholes, speed bumps, obstacles) in real-time, leveraging hardware-specific optimizations to ensure safety without the need for dedicated GPU hardware.
🎯 Objective

To deliver a robust, privacy-first edge AI solution that:

    Maximizes ARM Performance: Utilizes NCNN and FP16 quantization for the Cortex-A76.

    Ensures Continuous Monitoring: Implements a non-blocking multi-threaded architecture.

    Captures Critical Data: Logs event telemetry and saves pre-buffered incident videos.

🧠 Technical Innovations
1. NCNN & FP16 Optimization

The model is powered by the NCNN framework (by Tencent), which is uniquely optimized for ARM mobile CPUs.

    Quantization: We utilize FP16 (Half-Precision) to cut memory bandwidth in half.

    SIMD Acceleration: The pipeline leverages ARM NEON instructions, allowing for parallel data processing at the register level, significantly boosting FPS compared to standard PyTorch/ONNX runtimes.

2. Multi-Threaded Asynchronous Pipeline

The most critical feature of this implementation is the Threaded File-Writer.

    The Problem: Writing high-definition video to an SD card is an I/O bound task that usually "freezes" the main AI loop.

    The Solution: We use a Producer-Consumer model. The main thread handles inference and maintains a 2-second sliding window buffer in RAM. When an anomaly is detected, a background worker thread handles the FFmpeg encoding, ensuring the AI never misses a frame.

🛠 Tech Stack

    Hardware: Raspberry Pi 5 (8GB), USB Webcam / PiCamera2.

    Inference: Ultralytics YOLO → NCNN Export.

    Optimization: ARM NEON SIMD, FP16 Quantization.

    Processing: OpenCV & FFmpeg (Subprocess-based encoding).

📁 Project Structure
Plaintext

.
├── best_ncnn_model/       # NCNN FP16 Optimized YOLO model
├── videos/                # Test datasets
├── clips/                 # Auto-generated incident MP4s (organized by date)
├── logs/                  
│   └── anomaly_log.csv    # Real-time event telemetry
├── main_pi5.py            # Optimized inference & recording pipeline
└── README.md

⚙️ Installation & Usage

    Environment Setup:
    Bash

    python3 -m venv venv && source venv/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install ultralytics opencv-python
    sudo apt update && sudo apt install -y ffmpeg

    Run Pipeline:
    Bash

    python3 main_pi5.py

📈 Performance Benchmarks (Raspberry Pi 5)
Backend	Precision	FPS (Avg)	Latency
PyTorch (Stock)	FP32	~2-3 FPS	High
NCNN (Optimized)	FP16	12-18 FPS	Low
🔎 Deliverables & Evidence

    anomaly_log.csv: Contains timestamped evidence of every detection event.

    Pre-Event Clips: Because of the RAM buffering system, saved videos include the 2 seconds prior to detection, capturing the cause of the anomaly.

📬 Author

Mohd Nouman Ahmed ECE / Embedded AI Developer Developed for the Bharat AI-SoC Student Challenge 2026
