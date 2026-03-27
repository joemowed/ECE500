import cv2
import numpy as np
import onnxruntime as ort
import torch

import ort_helpers
# --- CONFIGURATION ---
MODEL_PATH = "./models/dany-v2.onnx"
INPUT_SIZE = 518  # Must be a multiple of 14


# 2. Initialize Webcam
cap = cv2.VideoCapture(0)

print("Starting webcam... Press 'q' to quit.")

session = ort.InferenceSession(
    "models/dany-v2-large.onnx", providers=["CUDAExecutionProvider"]
)
ort_helpers.print_interface(session)
input_name = session.get_inputs()[0].name


while cap.isOpened():
    success, frame = cap.read()
    if not success: break
    # 1. Pre-process (BGR to RGB -> Resize -> Normalize)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) / 255.0
    img = cv2.resize(img, (INPUT_SIZE, INPUT_SIZE))
    # ImageNet Mean/Std
    img = (img - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    img = img.transpose(2, 0, 1)[None].astype(np.float32)

    # 2. Inference
    depth = session.run(None, {input_name: img})[0]

    # 3. Post-process to Grayscale
    depth = depth.squeeze()
    # Normalize to 0-255 (CV_8U is 8-bit unsigned integer / grayscale)
    depth_bw = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    depth_bw = cv2.bitwise_not(depth_bw) 

    
    # Resize back to webcam resolution
    depth_bw_resized = cv2.resize(depth_bw, (frame.shape[1], frame.shape[0]))

    # 4. Display
    # Convert grayscale back to 3-channel so we can stack it with the BGR frame
    depth_bw_3ch = cv2.cvtColor(depth_bw_resized, cv2.COLOR_GRAY2BGR)
    combined = np.hstack((frame, depth_bw_3ch))
    
    cv2.imshow('Depth Anything V2 - B&W', combined)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
