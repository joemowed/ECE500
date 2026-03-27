ffmpeg -f v4l2 -i /dev/video0 \
-vcodec libx264 \
-preset ultrafast \
-tune zerolatency \
-g 1 \
-bf 0 \
-f mpegts udp://<receiver_ip>:5002

