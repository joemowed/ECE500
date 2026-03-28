import cv2
import sys
import os

os.environ["GST_DEBUG"] = "*:1"


def receive_stream():
    # GStreamer pipeline for receiving an H.264 UDP stream
    # 'appsink' is essential for OpenCV to capture frames from the pipeline
    # 'decodebin' automatically selects the right decoder
    # 'videoconvert ! video/x-raw,format=BGR' converts to a format OpenCV can use (BGR format)
    pipeline = (
        "udpsrc port=5001 ! "
        "application/x-rtp, media=video, encoding-name=H264 ! "
        "rtpjitterbuffer latency=0 ! "
        "rtpjpegdepay ! "
        "jpegdec ! "
        "videoconvert ! "
        "video/x-raw, format=BGR ! "
        "appsink max-buffers=1 drop=1"
    )

    return cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)


if __name__ == "main":
    cap = receive_stream()
    if not cap.isOpened():
        print("Cannot open video stream or file")
        sys.exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Empty frame received. Exiting...")

            continue
        # Display the resulting frame
        cv2.imshow("Received Stream", frame)

        # Press 'q' on the keyboard to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
