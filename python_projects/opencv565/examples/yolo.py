import cv2
import time
import torch
import onnxruntime as ort
import numpy as np
from yaml import DirectiveToken
import gst
import ort_helpers
from torch._C import dtype

HEIGHT, WIDTH = 640, 480  # example, replace with your model's input size
IMG_PATH = "imgs/2026-03-25-090151.jpg"
sess = ort.InferenceSession(
    "models/yolo26-night_one.onnx", providers=["CPUExecutionProvider"]
)
ort_helpers.print_interface(sess)
# ----------------------------
# Load image with OpenCV
# ----------------------------
#cap = gst.receive_stream()
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
    # 'output' is your result from session.run()
    # We use [0] to get the first batch
    detections = output[0][0]

    for i in range(300):
        # Extract the 6 values for this specific detection
        x1, y1, x2, y2, score, class_id = detections[i]

        # 1. Filter out empty/low-confidence slots
        if score > 0.5:
            # 2. Convert coordinates to integers for OpenCV drawing
            # NOTE: If these values are small (0.0 - 1.0), multiply them by
            # your image width and height first!
            left, top, right, bottom = int(x1), int(y1), int(x2), int(y2)

            # Draw the Bounding Box (Green, thickness of 2)
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

            # Create and draw the Label
            label = f"Class {int(class_id)}: {score:.2f}"
            cv2.putText(
                img,
                label,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

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
