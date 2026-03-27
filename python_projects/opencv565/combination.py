import cv2
import tkinter as tk
import math
import time
import torch
import onnxruntime as ort
import numpy as np
from yaml import DirectiveToken
import gst
from Depth_Anything import Depth_Anything
import ort_helpers
from Yolo import Yolo
from Metric3D import Metric3D
from WindowManager import WindowManager
from torch._C import dtype
import matplotlib.pyplot as plt

FOV = 78  # example, replace with your model's input size
plt.ion()
fig = plt.figure(figsize=(8, 8), dpi=200)
ax = fig.add_subplot(111, projection="polar")
sc = ax.scatter([], [])
ax.set_theta_zero_location("N")  # N = North (up)
ax.set_theta_direction(-1)  # clockwise
ax.set_thetamin(-FOV / 2)
ax.set_thetamax(FOV / 2)
winman = plt.get_current_fig_manager()
try:
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    # Calculate position for top right corner
    # The (x, y) coordinates define the top-left corner of the window
    win_width = int(screen_width * 0.4)
    win_height = int(screen_height * 0.4)
    pos_x = screen_width - win_width  # Assuming default DPI of 100
    pos_y = 0  # Top of the screen

    # Format the geometry string
    # "{}x{}+{}+{}".format(width_pixels, height_pixels, pos_x, pos_y)
    # The size in the geometry string needs to be in pixels. If using default dpi=100,
    # 10 inches width = 1000 pixels, 5 inches height = 500 pixels.
    window_geometry = "{}x{}+{}+{}".format(win_width, win_height, pos_x, pos_y)

    winman.window.geometry(window_geometry)  #

except AttributeError:
    # Handle other backends (e.g., Qt)
    # For Qt, you might use manager.window.move(x, y)
    winman.window.move(100, 0)  # Example for other backends
ax.set_rmax(1)
plt.draw()
plt.pause(0.1)


def get_color(class_id: int):
    if class_id == 1:
        return (1, 0, 0)


yolo = Yolo("models/yolo26-night_one.onnx")
m3d = Depth_Anything()
detector = cv2.wechat_qrcode_WeChatQRCode()

wm = WindowManager()
sess = ort.InferenceSession(
    "models/metric3d-small.onnx", providers=["CUDAExecutionProvider"]
)
# ----------------------------
# Load image with OpenCV
# ----------------------------
# UDP stream URL
stream_url = "udp://@:5002?fifo_size=200000&overrun_nonfatal=1"

# Add FFmpeg options to reduce packet loss issues
cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Keep only latest frame
# cap = gst.receive_stream()
# cap = cv2.VideoCapture(0)


if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

# img = cv2.imread(IMG_PATH)
prev_time = 0
depth_time = time.time()
qr_time = time.time()
depth_text = ""
one_shot_depth = True
qr_searching = True
qr_enable = True
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
while True:
    ret, img = cap.read()
    if not ret:
        break
    try:
        assert img is not None, "file could not be read, check with os.path.exists()"
        HEIGHT, WIDTH = img.shape[:2]
        QR_img = img.copy()
        strings, bbox_qr = (), ()
        if qr_searching:
            strings, bbox_qr = detector.detectAndDecode(QR_img)
            qr_time = time.time()
            if bbox_qr != ():
                qr_searching = False
                pts = bbox_qr[0].astype(int)
                cv2.polylines(QR_img, [pts], True, (0, 255, 255), 2)
                cv2.putText(
                    QR_img,
                    strings[0],
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2.0,
                    (0, 255, 0),
                    2,
                )

            wm.display("CNN QR Read", QR_img, corner="bottom_right")
        img_AI = ort_helpers.convert_for_NN(img)
        detections = yolo.run(img_AI)
        yolo.draw_bounding_boxes(img, detections)
        if depth_time + 0.5 < time.time():
            one_shot_depth = False
            # if depth_time + 0.5 < time.time():
            depth_map = m3d.run(img_AI)
            # depth_map = np.clip(depth_map, 0, 3)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(depth_map)
            depth_text = (
                f"MIN DEPTH: {float(min_val):.2f} MAX_DEPTH: {float(max_val):.2f}"
            )
            labels = []
            depth_detections = np.zeros((300, 6))
            for i, data in enumerate(detections):
                x1, y1, x2, y2, score, class_id = data
                if score > 0.5:
                    left, top, right, bottom = int(x1), int(y1), int(x2), int(y2)
                    depth_detections[i] = m3d.get_box_average(
                        depth_map, x1, y1, x2, y2, class_id
                    )
                    mean_depth = depth_detections[i][5]
                    labels.append((f"Depth: {mean_depth:.3f},", left, top))
            depth_img = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX).astype(
                np.uint8
            )
            depth_img = cv2.cvtColor(depth_img, cv2.COLOR_GRAY2RGB)
            for label, x, y in labels:
                cv2.putText(
                    depth_img,
                    label,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
            yolo.draw_bounding_boxes(depth_img, depth_detections, False, -1)
            cv2.putText(
                depth_img,
                depth_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )  #
            angles, distances, colors = [], [], []
            for pt in depth_detections:
                x1, y1, x2, y2, class_id, depth = pt
                if x1 == y1 == y2 == x2 == 0:
                    break
                x = float((x2 + x1) / 2)
                y = (y2 + y1) / 2
                angle = (x / WIDTH - 0.5) * FOV
                colors.append(get_color(class_id))
                angles.append(np.radians(angle))
                depth = abs(depth - max_val) / max_val
                distances.append(depth)
                cv2.circle(
                    depth_img,
                    (int(x), int(y)),
                    radius=5,
                    color=(0, 0, 255),
                    thickness=-1,
                )
            if not distances == []:
                sc.set_offsets(np.c_[angles, distances])
                sc.set_color(colors)
                plt.draw()
                plt.pause(0.01)
            depth_img = cv2.bitwise_not(depth_img)
            wm.display("Depth", depth_img, corner="bottom_left")
            depth_time = time.time()

        wm.display("RGB", img, corner="top_left")
        #     if cv2.waitKey(1) & 0xFF == ord('q'): break
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("d"):
            one_shot_depth = True
        if key == ord("r"):
            qr_searching = True
    finally:
        pass
