import threading
import cv2

class LatestFrame:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
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

