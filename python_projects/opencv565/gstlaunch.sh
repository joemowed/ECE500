gst-launch-1.0 -v v4l2src device=/dev/video0 !   image/jpeg,width=640,height=480,framerate=30/1 !   jpegparse ! rtpjpegpay !   udpsink host=10.137.88.165 port=5001 sync=false
