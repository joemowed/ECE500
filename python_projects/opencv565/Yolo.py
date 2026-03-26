import cv2
from cv2.typing import MatLike
import onnxruntime as ort
import numpy as np
import ort_helpers

class Yolo:


    def __init__(self,model_onnx_path:str):
        self.sess = ort.InferenceSession(model_onnx_path, providers=["CPUExecutionProvider"])
        ort_helpers.print_interface(self.sess)

    def run(self,img:MatLike)->np.ndarray:
        input_tensor = self.preprocess_yolo_image(img)
        output = self.sess.run(["output0"], {"images": input_tensor})
        # 'output' is your result from session.run()
        # We use [0] to get the first batch
        detections = output[0][0]
        return detections
    def draw_bounding_boxes(self,img:MatLike,detections,draw_label=True,min_confidence=0.5):
        for data in  detections:
            # Extract the 6 values for this specific detection
            x1, y1, x2, y2, score, class_id = data

            # 1. Filter out empty/low-confidence slots
            if score > min_confidence:
                # 2. Convert coordinates to integers for OpenCV drawing
                # NOTE: If these values are small (0.0 - 1.0), multiply them by
                # your image width and height first!
                left, top, right, bottom = int(x1), int(y1), int(x2), int(y2)

                # Draw the Bounding Box (Green, thickness of 2)
                cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

                # Create and draw the Label
                if(draw_label):
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

    def preprocess_yolo_image(self,img: np.ndarray) -> np.ndarray:

        # 5. Add batch dimension: 1 x 3 x H x W
        img_batch = np.expand_dims(img, axis=0)

        return img_batch
