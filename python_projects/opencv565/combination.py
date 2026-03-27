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
detector = cv2.wechat_qrcode_WeChatQRCode()

wm = WindowManager()
sess = ort.InferenceSession(
    "models/metric3d-small.onnx", providers=["CUDAExecutionProvider"]
)
# ----------------------------
# Load image with OpenCV
# ----------------------------
#cap = gst.receive_stream()
cap = cv2.VideoCapture(0)


if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

# img = cv2.imread(IMG_PATH)
prev_time = 0
depth_time = time.time()
depth_text = ""
while True:
    ret, img = cap.read()
    if not ret:
        break
    assert img is not None, "file could not be read, check with os.path.exists()"
    QR_img = img.copy() 
    strings, bbox_qr = detector.detectAndDecode(QR_img)
    img = cv2.resize(img, (HEIGHT, WIDTH))
    img_AI = ort_helpers.convert_for_NN(img)
    detections = yolo.run(img_AI)
    yolo.draw_bounding_boxes(img, detections)
    if depth_time + 0.5 < time.time():
        depth_map = m3d.run(img_AI)
        depth_map = np.clip(depth_map,0,3)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(depth_map)
        depth_text = f"MIN DEPTH: {float(min_val):.2f} MAX_DEPTH: {float(max_val):.2f}"
        labels = []
        depth_detections = np.zeros((300,6))
        for i,data in enumerate(detections):
            x1, y1, x2, y2, score, class_id = data
            if score > 0.5:
                left, top, right, bottom = int(x1), int(y1), int(x2), int(y2)
                depth_detections[i] = m3d.get_box_average(depth_map,x1,y1,x2,y2)
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
        yolo.draw_bounding_boxes(depth_img, depth_detections, False,-1)
        cv2.putText(
            depth_img,
            depth_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
        )  #
        wm.display("Depth", depth_img, corner="bottom_left")
        depth_time = time.time()

    if bbox_qr !=():
        pts = bbox_qr[0].astype(int)
        cv2.polylines(QR_img, [pts], True, (0,255,255), 2)
        cv2.putText(QR_img, strings[0], (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 2)

    wm.display("CNN QR Read", QR_img, corner="top_right")
    wm.display("RGB", img, corner="top_left")
    #     if cv2.waitKey(1) & 0xFF == ord('q'): break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
