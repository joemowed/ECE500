import cv2
import numpy as np
import tkinter as tk
import time

class WindowManager:
    def __init__(self,scale=1.0):
        # 1. Get screen resolution using tkinter
        root = tk.Tk()
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()
        root.destroy()
        
        # Windows registry to track positions
        self.windows = []
        self.fps_timers = {}
        self.scale =scale

    def display(self, name, img, corner="top_left"):
        """
        Displays an image in a specific screen corner.
        Corners: 'top_left', 'top_right', 'bottom_left', 'bottom_right'
        """
        # Resize if requested
        if self.scale != 1.0:
            img = cv2.resize(img, (0, 0), fx=self.scale, fy=self.scale)
        
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
            self.fps_timers[name] = time.time()
            
        current_time = time.time()
        fps = 1 / (current_time - self.fps_timers[name])
        self.fps_timers[name] = current_time
        fps_text = f"FPS: {int(fps)}"
        height, width = img.shape[:2]
        cv2.putText(img, fps_text, (10, height-60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  
        cv2.imshow(name, img)
        cv2.moveWindow(name, x, y)

# --- EXAMPLE USAGE ---
# wm = WindowManager()
# while True:
#     # frame = your_yolo_result
#     # depth = your_metric3d_result
#     wm.display("RGB", frame, corner="top_left", scale=0.5)
#     wm.display("Depth", depth, corner="top_right", scale=0.5)
#     if cv2.waitKey(1) & 0xFF == ord('q'): break

