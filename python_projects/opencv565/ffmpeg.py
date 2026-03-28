import cv2
from LatestFrame import LatestFrame

# Just pass the port number now
cap = LatestFrame(5002)

while True:
    frame = cap.read()
    if frame is None:
        continue
        
    cv2.imshow("Ultra-Low Latency", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
