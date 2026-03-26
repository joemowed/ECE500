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
yolo = ort.InferenceSession(
    "models/yolo26-night_one.onnx", providers=["CUDAExecutionProvider"]
)
sess = ort.InferenceSession(
    "models/metric3d-small.onnx", providers=["CUDAExecutionProvider"]
)
ort_helpers.print_interface(yolo)
# ----------------------------
# Load image with OpenCV
# ----------------------------
cap = gst.receive_stream()
# cap = cv2.VideoCapture(0)

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
    output = yolo.run(["output0"], {"images": input_tensor})
    # 'output' is your result from session.run()
    # We use [0] to get the first batch
    detections = output[0][0]

    img_norm = img.astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img_norm = (img_norm - mean) / std

    #    # Convert to CHW and add batch dim
    input_tensor = np.transpose(img_norm, (2, 0, 1))  # HWC -> CHW
    input_tensor = np.expand_dims(input_tensor, 0)  # 1,3,H,W

    # ----------------------------
    # Run inference
    # ----------------------------
    outputs = sess.run(["predicted_depth"], {"pixel_values": input_tensor})
    depth_map = outputs[0]
    predicted_depth = np.squeeze(depth_map)

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

    # Depth map: normalize to 0-255 for visualization
    depth_img = cv2.normalize(predicted_depth, None, 0, 255, cv2.NORM_MINMAX).astype(
        np.uint8
    )

    cv2.imshow("Input", img)
    cv2.imshow("Depth", depth_img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
