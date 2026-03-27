ffmpeg -f v4l2 -i /dev/video0 \
-vcodec mjpeg \
-q:v 5 \
-s 640x480 \
-f mpegts udp://10.137.88.153:5002

