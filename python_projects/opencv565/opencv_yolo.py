
import cv2
import time
import torch
import onnxruntime as ort
import numpy as np
import gst
import ort_helpers
from torch._C import dtype

HEIGHT, WIDTH = 640, 480  # example, replace with your model's input size
IMG_PATH = "imgs/2026-03-25-090151.jpg"
sess = ort.InferenceSession(
    "models/yolo26-night_one.onnx", providers=["CUDAExecutionProvider"]
)
ort_helpers.print_interface(sess)
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



    input_tensor = ort_helpers.preprocess_yolo_image(img)

    # ----------------------------
    # Run inference
    # ----------------------------
    output = sess.run(["output0"], {"images": input_tensor})
    output = output[0]
    output = output[0]
    confidence_threshold = 0.1
    preds = output[output[:, 4] > confidence_threshold]  # filter by confidence

    height, width, _ = img.shape  # original image size

    for x, y, w, h, conf, cls in preds:
        # convert from center-width-height to top-left / bottom-right
        x1 = int((x - w/2) * width)
        y1 = int((y - h/2) * height)
        x2 = int((x + w/2) * width)
        y2 = int((y + h/2) * height)

        # Draw box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, str(int(cls)), (x1, y1-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# Show the result
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Convert FPS to string and display on the frame
    fps_text = f"FPS: {int(fps)}"
    cv2.putText(img, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  #

    cv2.imshow("Composed", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
