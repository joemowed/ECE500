import onnxruntime as ort
import numpy as np
import cv2
def preprocess_yolo_image(img: np.ndarray, target_size=(640, 640)) -> np.ndarray:
    """
    Preprocess an OpenCV image for YOLO model input using NumPy.

    Args:
        img (np.ndarray): Input image in BGR format (as OpenCV loads it).
        target_size (tuple): (width, height) the model expects.

    Returns:
        np.ndarray: Preprocessed image of shape [1, 3, H, W], float32, values 0-1.
    """
    # 1. Convert BGR -> RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 3. Scale pixels to 0-1
    img_norm = img_rgb.astype(np.float32) / 255.0

    # 4. HWC -> CHW
    img_chw = np.transpose(img_norm, (2, 0, 1))

    # 5. Add batch dimension: 1 x 3 x H x W
    img_batch = np.expand_dims(img_chw, axis=0)

    return img_batch

def print_interface(session:ort.InferenceSession)->None:
# 2. Get input details
    print("Model Inputs:")
    for input_meta in session.get_inputs():
        print(f"* Name: [Name: {input_meta.name}]")
        print(f"  Shape: {input_meta.shape}")
        print(f"  Type: {input_meta.type}")

# 3. Get output details
    print("\nModel Outputs:")
    for output_meta in session.get_outputs():
        print(f"* Name: [Name: {output_meta.name}]")
        print(f"  Shape: {output_meta.shape}")
        print(f"  Type: {output_meta.type}")

