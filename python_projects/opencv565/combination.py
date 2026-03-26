import cv2
import time
import torch
import onnxruntime as ort
import numpy as np
from yaml import DirectiveToken
import gst
import ort_helpers
from Yolo import Yolo
from Metric3D import Metric3D
from WindowManager import WindowManager
from torch._C import dtype


HEIGHT, WIDTH = 640, 480  # example, replace with your model's input size
IMG_PATH = "imgs/2026-03-25-090151.jpg"
yolo = Yolo("models/yolo26-night_one.onnx")
m3d = Metric3D()

wm = WindowManager()
sess = ort.InferenceSession(
    "models/metric3d-small.onnx", providers=["CUDAExecutionProvider"]
)
# ----------------------------
# Load image with OpenCV
# ----------------------------
# cap = gst.receive_stream()
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

# img = cv2.imread(IMG_PATH)
prev_time = 0
while True:
    ret, img = cap.read()
    if not ret:
        break
    assert img is not None, "file could not be read, check with os.path.exists()"
    img = cv2.resize(img, (HEIGHT, WIDTH))
    img_AI = ort_helpers.convert_for_NN(img)
    detections = yolo.run(img_AI)
    yolo.draw_bounding_boxes(img,detections)
    depth_map = m3d.run(img_AI)



    depth_img = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(depth_map)
    depth_text = f"MIN DEPTH: {float(min_val):.2f} MAX_DEPTH: {float(max_val):.2f}"

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    fps_text = f"FPS: {int(fps)}"

    cv2.putText(img, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  #
    cv2.putText(depth_img, depth_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  #
    wm.display("RGB", img, corner="top_left")
    wm.display("Depth", depth_img, corner="top_right")
#     if cv2.waitKey(1) & 0xFF == ord('q'): break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
