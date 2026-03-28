ffmpeg -f v4l2 -framerate 30 -video_size 240x140 -i /dev/video0 \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -x264-params "sliced-threads=1:slices=4" \
  -g 15 \
  -f mpegts "udp://10.137.88.153:5002?pkt_size=1316"
