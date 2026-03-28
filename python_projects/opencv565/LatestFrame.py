import threading
import subprocess
import numpy as np
import cv2

class LatestFrame:
    def __init__(self, port):
        self.width = 640
        self.height = 480
        # Aggressive flags to kill internal FFmpeg buffering
        self.cmd = [
            'ffmpeg',
            '-probesize', '32',
            '-analyzeduration', '0',
            '-fflags', 'nobuffer+discardcorrupt+flush_packets',
            '-flags', 'low_delay',
            '-i', f'udp://@:{port}?fifo_size=5000&overrun_nonfatal=1',
            '-f', 'image2pipe',
            '-pix_fmt', 'bgr24',
            '-vcodec', 'rawvideo', '-'
        ]
        
        # Start the ffmpeg subprocess
        self.pipe = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, bufsize=10**8)
        
        self.frame = None
        self.lock = threading.Lock()
        self.running = True

        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        # Size of one frame in bytes (640 * 480 * 3 colors)
        frame_size = self.width * self.height * 3
        
        while self.running:
            # Read exactly one frame's worth of bytes
            raw_frame = self.pipe.stdout.read(frame_size)
            
            if len(raw_frame) != frame_size:
                continue

            # Convert bytes to numpy array
            frame = np.frombuffer(raw_frame, dtype='uint8').reshape((self.height, self.width, 3))
            
            with self.lock:
                self.frame = frame

    def read(self):
        with self.lock:
            return self.frame
