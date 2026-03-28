import threading
import subprocess
import numpy as np
import os

class LatestFrame:
    def __init__(self, port):
        self.width = 640
        self.height = 480
        self.frame_size = self.width * self.height * 3
        
        self.cmd = [
            'ffmpeg',
            '-loglevel', 'quiet',
            '-flags', 'low_delay',
            '-fflags', 'nobuffer+discardcorrupt',
            '-i', f'udp://0.0.0.0:{port}?fifo_size=1000000&overrun_nonfatal=1',
            '-f', 'image2pipe',
            '-pix_fmt', 'bgr24',
            '-vcodec', 'rawvideo', '-'
        ]
        
        # Use a large bufsize for the pipe itself to prevent OS-level stalls
        self.pipe = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, bufsize=self.frame_size * 5)
        
        self.frame = None
        self.lock = threading.Lock()
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            # 1. Read the raw bytes
            raw_frame = self.pipe.stdout.read(self.frame_size)
            
            if len(raw_frame) != self.frame_size:
                continue

            # 2. TRANSFORM: Convert to numpy
            img = np.frombuffer(raw_frame, dtype='uint8').reshape((self.height, self.width, 3))
            
            # 3. THE FLUSH: If more data is waiting in the pipe, it means we are 
            # behind. We need to clear the pipe to get to the "live" data.
            # On Linux, we can check how many bytes are waiting:
            import fcntl, termios, struct
            while True:
                # Check how many bytes are waiting in the stdout buffer
                waiting = struct.unpack('I', fcntl.ioctl(self.pipe.stdout.fileno(), termios.FIONREAD, struct.pack('I', 0)))[0]
                if waiting < self.frame_size:
                    break
                # Skip to the next frame
                self.pipe.stdout.read(self.frame_size)

            with self.lock:
                self.frame = img

    def read(self):
        with self.lock:
            return self.frame
