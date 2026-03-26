import cv2
import numpy as np
import tkinter as tk

class WindowManager:
    def __init__(self):
        # 1. Get screen resolution using tkinter
        root = tk.Tk()
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()
        root.destroy()
        
        # Windows registry to track positions
        self.windows = []

    def display(self, name, img, corner="top_left", scale=1.0):
        """
        Displays an image in a specific screen corner.
        Corners: 'top_left', 'top_right', 'bottom_left', 'bottom_right'
        """
        # Resize if requested
        if scale != 1.0:
            img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
        
        h, w = img.shape[:2]
        
        # Calculate coordinates
        if corner == "top_left":
            x, y = 0, 0
        elif corner == "top_right":
            x, y = self.screen_w - w, 0
        elif corner == "bottom_left":
            x, y = 0, self.screen_h - h - 50 # -50 for taskbar
        elif corner == "bottom_right":
            x, y = self.screen_w - w, self.screen_h - h - 50
        else:
            x, y = 0, 0

        # Create, move, and show
        if name not in self.windows:
            cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
            self.windows.append(name)
            
        cv2.imshow(name, img)
        cv2.moveWindow(name, x, y)

    def stack_and_show(self, name, img_list, cols=2, corner="top_left"):
        """
        Easily stacks multiple images into a grid and shows in one corner.
        """
        # Ensure all images are same size and 3-channel
        ref_h, ref_w = img_list[0].shape[:2]
        processed_imgs = []
        
        for im in img_list:
            if len(im.shape) == 2: # Convert Gray to BGR
                im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
            im = cv2.resize(im, (ref_w, ref_h))
            processed_imgs.append(im)
            
        # Create grid
        rows = [cv2.hconcat(processed_imgs[i:i+cols]) for i in range(0, len(processed_imgs), cols)]
        combined = cv2.vconcat(rows)
        
        self.display(name, combined, corner=corner)

# --- EXAMPLE USAGE ---
# wm = WindowManager()
# while True:
#     # frame = your_yolo_result
#     # depth = your_metric3d_result
#     wm.display("RGB", frame, corner="top_left", scale=0.5)
#     wm.display("Depth", depth, corner="top_right", scale=0.5)
#     if cv2.waitKey(1) & 0xFF == ord('q'): break

