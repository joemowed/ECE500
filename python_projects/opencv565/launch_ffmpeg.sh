ffmpeg -f v4l2 -framerate 20 -video_size 640x480 -i /dev/video0 \
-c:v mjpeg -q:v 7 -fflags nobuffer \
-f mjpeg udp://10.137.88.153:5002?pkt_size=1316

