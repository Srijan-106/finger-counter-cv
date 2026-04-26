# ✋ Finger Counting using Computer Vision

A real-time finger counting system using a webcam, built with OpenCV and MediaPipe.

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
- If angle is large → finger is open  
- If angle is small → finger is closed  

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