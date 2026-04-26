import cv2
import mediapipe as mp
import os
import math
from collections import deque


# =========================================================
# LOAD MODEL
# =========================================================
model_path = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")


# =========================================================
# MEDIAPIPE SETUP
# =========================================================
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2
)

landmarker = HandLandmarker.create_from_options(options)


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def calculate_angle(a, b, c):
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])

    dot = ba[0]*bc[0] + ba[1]*bc[1]
    mag_ba = math.hypot(ba[0], ba[1])
    mag_bc = math.hypot(bc[0], bc[1])

    if mag_ba * mag_bc == 0:
        return 0

    cos_val = max(-1.0, min(1.0, dot / (mag_ba * mag_bc)))
    return math.degrees(math.acos(cos_val))


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


# =========================================================
# HAND CONNECTIONS
# =========================================================
connections = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20)
]

finger_joints = [
    (5,  6,  8),
    (9,  10, 12),
    (13, 14, 16),
    (17, 18, 20),
]


# =========================================================
# SMOOTHING
# =========================================================
smooth_buffer = deque(maxlen=5)


# =========================================================
# CAMERA
# =========================================================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


# =========================================================
# MAIN LOOP
# =========================================================
while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not working!")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    result = landmarker.detect(mp_image)

    total_fingers = 0

    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:

            h, w, _ = frame.shape
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]

            # ---------- DRAW ----------
            for start, end in connections:
                cv2.line(frame, landmarks[start], landmarks[end], (0, 255, 0), 2)

            finger_count = 0
            wrist = landmarks[0]

            # ---------- HAND SCALE ----------
            palm_size = dist(landmarks[0], landmarks[9])

            # =========================================================
            # THUMB (STRICT LOGIC)
            # =========================================================
            thumb_mcp = landmarks[2]
            thumb_ip  = landmarks[3]
            thumb_tip = landmarks[4]

            angle_thumb = calculate_angle(thumb_mcp, thumb_ip, thumb_tip)

            thumb_far = dist(wrist, thumb_tip) > dist(wrist, thumb_mcp) + 0.12 * palm_size
            thumb_dir = abs(thumb_tip[0] - thumb_ip[0]) > 0.04 * w

            if angle_thumb > 135 and thumb_far and thumb_dir:
                finger_count += 1

            # =========================================================
            # OTHER FINGERS (STRICT LOGIC)
            # =========================================================
            for mcp_i, pip_i, tip_i in finger_joints:

                tip = landmarks[tip_i]
                pip = landmarks[pip_i]
                mcp = landmarks[mcp_i]

                angle = calculate_angle(mcp, pip, tip)

                tip_far = dist(wrist, tip) > dist(wrist, pip) + 0.08 * palm_size

                is_up = tip[1] < pip[1] < mcp[1]

                if angle > 140 and tip_far and is_up:
                    finger_count += 1

            total_fingers += finger_count

    # ---------- SMOOTHING ----------
    smooth_buffer.append(total_fingers)
    smoothed = round(sum(smooth_buffer) / len(smooth_buffer))

    # ---------- DISPLAY ----------
    cv2.putText(frame, f'Total Fingers: {smoothed}', (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow("Finger Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# =========================================================
# CLEANUP
# =========================================================
cap.release()
cv2.destroyAllWindows()