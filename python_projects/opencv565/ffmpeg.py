import cv2

# UDP stream URL
stream_url = "udp://@:5002"

# Add FFmpeg options to reduce packet loss issues
cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Failed to open stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame not received. Waiting...")
        continue

    cv2.imshow("UDP Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
