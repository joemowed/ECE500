ffmpeg -f v4l2 -i /dev/video0 \
-vcodec mjpeg \
-s 640x480 \
-f mjpeg udp://10.137.88.153:80

