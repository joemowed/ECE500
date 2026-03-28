import subprocess
import numpy as np
import cv2
import LatestFrame as lf

stream_url = (
    "udp://@:5002?" "fifo_size=500000&" "overrun_nonfatal=1&" "fflags=discardcorrupt&"
)
# Add FFmpeg options to reduce packet loss issues
cap = lf.LatestFrame(stream_url)

while True:
    frame = cap.read()
    if frame is None:
        continue
    cv2.imshow("ffmpeg test",frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
