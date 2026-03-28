import os
import cv2
import threading

class LatestFrame:
    def __init__(self, src):
        # Tell FFmpeg to disable internal buffering and force low latency
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp|fflags;nobuffer|flags;low_delay|framedrop;1"
        
        self.cap = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
        
        # Manually set the buffer size to 1 frame if the backend supports it
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        self.frame = None
        self.lock = threading.Lock()
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()
    def update(self):
        while self.running:
            self.cap.grab()
            ret, frame = self.cap.retrieve()
            if ret:
                with self.lock:
                    self.frame = frame  # overwrite old frame

    def read(self):
        with self.lock:
            return self.frame

