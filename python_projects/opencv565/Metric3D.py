from cv2.typing import MatLike
import onnxruntime as ort
import numpy as np
class Metric3D:
    def __init__(self):
        self.sess = ort.InferenceSession("models/metric3d-small.onnx", providers=["CUDAExecutionProvider"])
    def run(self,img:MatLike)->MatLike:
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(3,1,1)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(3,1,1)
        img = (img - mean) / std
        img = np.expand_dims(img, 0)  #add batch dim
        outputs = self.sess.run(["predicted_depth"], {"pixel_values": img})
        depth_map = outputs[0]
        return np.squeeze(depth_map)

