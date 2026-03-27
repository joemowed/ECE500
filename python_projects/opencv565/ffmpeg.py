import subprocess
import numpy as np
import cv2

WIDTH = 640
HEIGHT = 480

cmd = [
    "ffmpeg",
    "-fflags",
    "nobuffer",
    "-flags",
    "low_delay",
    "-fflags",
    "discardcorrupt",
    "-analyzeduration",
    "0",
    "-probesize",
    "32",
    "-i",
    "udp://@:5002",
    "-f",
    "rawvideo",
    "-pix_fmt",
    "bgr24",
    "-",
]

pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)

while True:
    raw_frame = pipe.stdout.read(WIDTH * HEIGHT * 3)
    if len(raw_frame) != WIDTH * HEIGHT * 3:
        continue

    frame = np.frombuffer(raw_frame, np.uint8).reshape((HEIGHT, WIDTH, 3))

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
