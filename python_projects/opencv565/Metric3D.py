from cv2.typing import MatLike
import onnxruntime as ort
import numpy as np
class Metric3D:
    def __init__(self):
        self.sess = ort.InferenceSession("models/metric3d-large.onnx", providers=["CUDAExecutionProvider"])
    def run(self,img:MatLike)->MatLike:
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(3,1,1)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(3,1,1)
        img = (img - mean) / std
        img = np.expand_dims(img, 0)  #add batch dim
        outputs = self.sess.run(["predicted_depth"], {"pixel_values": img})
        depth_map = outputs[0]
        return np.squeeze(depth_map)
    
    def get_box_average(self,img, x1, y1, x2, y2):
        padding = 0
        # 1. Get image boundaries to prevent crashes
        h, w = img.shape[:2]
        
        dx = x2-x1
        dy = y2-y1
        if(dy <0 or dx<0):
            print("ERROR: BOUNDING BOX INVERTED")
            return 0
        dx/=4  
        dy/=4
        x1+=dx
        x2-=dx
        y1+=dy
        y2-=dy
        print("AVERGAE",x1,y1,x2,y2)
        # 2. Ensure coordinates are within image and are integers
        x1, y1 = max(0, int(x1+padding)), max(0, int(y1+padding))
        x2, y2 = min(w, int(x2-padding)), min(h, int(y2-padding))

        print("INT",x1,y1,x2,y2)
        
        # 3. Crop the bounding box area (ROI)
        # Remember: OpenCV uses [y_start:y_end, x_start:x_end]
        roi = img[y1:y2, x1:x2]
        
        # 4. Return the average if the box isn't empty
        if roi.size == 0:
            print("NULL BOX")
            return 0
            
        return (x1, y1, x2, y2, 0, np.mean(roi)    )
        

