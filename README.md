# ✋ Finger Counting using Computer Vision

![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)

Real-time finger counting using OpenCV and MediaPipe with geometric hand landmark analysis.

---

## 🚀 Features
- Real-time hand detection  
- Accurate finger counting using angle-based logic  
- Supports multiple hands  
- Smooth output using buffering  

---

## 🧠 How it works
- MediaPipe detects **21 hand landmarks**  
- Angles between finger joints are calculated  
- Straight finger → large angle → counted  
- Bent finger → small angle → ignored  

---

## 🛠 Tech Stack
- Python  
- OpenCV  
- MediaPipe  

---

## ▶️ Run

```bash
pip install opencv-python mediapipe
python finger_count.py