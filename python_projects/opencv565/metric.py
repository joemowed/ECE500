import cv2
import time
import torch
import onnxruntime as ort
import numpy as np
from torch._C import dtype

IMG_PATH = "imgs/2026-03-25-090151.jpg"
sess = ort.InferenceSession(
    "models/metric3d-small.onnx", providers=["CUDAExecutionProvider"]
)

# ----------------------------
# Load image with OpenCV
# ----------------------------
cap = cv2.VideoCapture(0)  # 0 = default webcam

if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

# img = cv2.imread(IMG_PATH)
prev_time = 0
while True:
    ret, img = cap.read()
    if not ret:
        break

    assert img is not None, "file could not be read, check with os.path.exists()"
    # Get dimensions
    height, width = img.shape[:2]

    # Normalize to [0,1]
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

    # ----------------------------
    # Postprocess: Convert to OpenCV images
    # ----------------------------

    # Depth map: normalize to 0-255 for visualization
    depth_img = cv2.normalize(predicted_depth, None, 0, 255, cv2.NORM_MINMAX).astype(
        np.uint8
    )

    # ----------------------------
    # Display
    # ----------------------------
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Convert FPS to string and display on the frame
    fps_text = f"FPS: {int(fps)}"
    cv2.putText(img, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  #

    cv2.imshow("Input", img)
    cv2.imshow("Depth", depth_img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
