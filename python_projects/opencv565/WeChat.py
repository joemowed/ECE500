import cv2
import time
import numpy as np
from WindowManager import WindowManager

HEIGHT, WIDTH = 640, 480  # example, replace with your model's input size

wm = WindowManager()
cap = cv2.VideoCapture(0)
detector = cv2.wechat_qrcode_WeChatQRCode()

if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

prev_time = 0
while True:
    ret, img = cap.read()
    if not ret:
        break
    assert img is not None, "file could not be read, check with os.path.exists()"
    strings, bbox = detector.detectAndDecode(img)
    if bbox is not None:
        for i in range(len(bbox)):
            pts = bbox[i].astype(int)

            # Draw box
            cv2.polylines(img, [pts], isClosed=True, color=(0,255,0), thickness=2)

            # Put decoded text
            cv2.putText(
                img,
                strings[i],
                tuple(pts[0]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )
    wm.display("CNN QR Read", img, corner="top_left")
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
