ffmpeg -f v4l2 -framerate 30 -video_size 640x480 -i /dev/video0 \
  -c:v libx264 -preset ultrafast -tune zerolatency -g 30\
  -f mpegts udp://10.137.88.153:5002
