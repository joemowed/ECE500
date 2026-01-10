import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define green color range
    lower_green = np.array([40, 70, 70])
    upper_green = np.array([80, 255, 255])

    # Create mask for green color

    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Take the largest green object
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 500:  # ignore small noise
            x, y, w, h = cv2.boundingRect(c)
            # Draw red bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow("Webcam Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
