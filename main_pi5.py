import cv2
import os
import csv
import threading
import queue
from datetime import datetime
from collections import deque
from ultralytics import YOLO
import subprocess
import sys

MODEL_PATH="best_ncnn_model"
SOURCE="videos/vid1.mp4"        #use picamera0 for rpicams or use a prerecorded video path
CONF_THRESH= 0.4
PRE_BUFFER_SECONDS= 2
POST_BUFFER_SECONDS= 3
ANOMALY_CLASSES= [2, 3, 4, 5]
SHOW_PREVIEW= True
SHOW_FPS= True

os.makedirs("logs", exist_ok=True)
os.makedirs("clips", exist_ok=True)
log_file= "logs/anomaly_log.csv"

if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        csv.writer(f).writerow(["timestamp", "class", "confidence(%)", "clip"])


def get_today_folder():
    date_str= datetime.now().strftime("%Y-%m-%d")
    day_folder= os.path.join("clips", date_str)
    os.makedirs(day_folder, exist_ok=True)
    return day_folder

model = YOLO(MODEL_PATH, task="detect")

if os.path.isfile(SOURCE):
    source_type= "video"
elif "usb" in SOURCE:
    source_type= "usb"
    usb_idx= int(SOURCE.replace("usb", ""))
elif "picamera" in SOURCE:
    source_type= "picamera"
else:
    print("Invalid source")
    sys.exit(1)

if source_type in ["video", "usb"]:
    cap= cv2.VideoCapture(SOURCE if source_type== "video" else usb_idx)
    if not cap.isOpened():
        print("Could not open source")
        sys.exit(1)

    fps= cap.get(cv2.CAP_PROP_FPS)
    if fps<= 1:
        fps= 25

    width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


elif source_type == "picamera":
    from picamera2 import Picamera2
    import numpy as np

    cap = Picamera2()
    cap.configure(
        cap.create_video_configuration(
            main={"format": "XRGB8888", "size": (640, 480)}
        )
    )
    cap.start()

    fps = 30
    width, height = 640, 480


#Buffers {used to keep fotage before 2 second of detected anomaly for pre and after 3 seconds after detecting anomaly that is post}
pre_buffer_max= int(fps * PRE_BUFFER_SECONDS)
post_buffer_max= int(fps * POST_BUFFER_SECONDS)
frame_buffer= deque(maxlen=pre_buffer_max)

save_queue= queue.Queue()

#Seperate thread for video saving after detecing anomaly to utilise parallel processing.
def file_writer_worker():
    while True:
        item= save_queue.get()
        if item is None:
            save_queue.task_done()
            break

        mp4_path, frames, fps, size= item
        width, height= size

        proc = subprocess.Popen(
            [
                "ffmpeg", "-y",
                "-f", "rawvideo",
                "-pix_fmt", "bgr24",
                "-s", f"{width}x{height}",
                "-r", str(fps),
                "-i", "-",
                "-c:v", "libx264",
                "-profile:v", "baseline",
                "-level", "3.0",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                mp4_path
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        for f in frames:
            proc.stdin.write(f.tobytes())

        proc.stdin.close()
        proc.wait()
        print("MP4 saved:", mp4_path)
        save_queue.task_done()

threading.Thread(target=file_writer_worker, daemon=True).start()

#Yolo detection_loop_anomaly
recording= False
post_event_frames= []
current_clip_path= ""
exit_requested= False


prev_time = datetime.now()
fps_display = 0.0
frame_count = 0

print("Live anomaly system started")

try:
    while True:
        if source_type in ["video", "usb"]:
            ret, frame= cap.read()
            if not ret:
                break
        else:
            frame= cv2.cvtColor(cap.capture_array(), cv2.COLOR_BGRA2BGR)

        results= model(frame, conf=CONF_THRESH, verbose=False)
        boxes= results[0].boxes if results else []

        anomaly_boxes= [b for b in boxes if int(b.cls[0]) in ANOMALY_CLASSES]
        anomaly_now= len(anomaly_boxes) > 0

        for b in anomaly_boxes:
            x1, y1, x2, y2 = map(int, b.xyxy[0])
            label = model.names[int(b.cls[0])]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if anomaly_now and not recording:
            recording = True
            post_event_frames = []

            b = anomaly_boxes[0]
            label_name = model.names[int(b.cls[0])]
            time_str = datetime.now().strftime("%H-%M-%S")
            day_folder = get_today_folder()

            current_clip_path = os.path.join(day_folder, f"{label_name}_{time_str}.mp4")

            with open(log_file, "a", newline="") as f:
                csv.writer(f).writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    label_name,
                    round(float(b.conf[0]) * 100, 1),
                    current_clip_path
                ])

        if recording:
            post_event_frames.append(frame.copy())
            if len(post_event_frames) >= post_buffer_max:
                save_queue.put((
                    current_clip_path,
                    list(frame_buffer) + post_event_frames,
                    fps,
                    (width, height)
                ))
                recording = False
                post_event_frames = []
        else:
            frame_buffer.append(frame.copy())

        #fps counter
        frame_count += 1
        now = datetime.now()
        elapsed = (now - prev_time).total_seconds()
        if elapsed >= 1.0:
            fps_display = frame_count / elapsed
            frame_count = 0
            prev_time = now

        if SHOW_PREVIEW:
            if SHOW_FPS:
                cv2.putText(frame, f"FPS: {fps_display:.1f}",
                            (15, 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 255, 0),
                            2)

            cv2.imshow("Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                exit_requested = True

        if exit_requested and not recording:
            break

finally:
    print("Shutting down cleanly...")
    save_queue.put(None)
    save_queue.join()

    if source_type in ["video", "usb"]:
        cap.release()
    else:
        cap.stop()
    cv2.destroyAllWindows()
    print("Done.")
