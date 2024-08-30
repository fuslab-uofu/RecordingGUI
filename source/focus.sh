#!/bin/bash
# gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -s:v 1920x1080  -threads 0 -f v4l2 /dev/video0
gphoto2 --capture-movie --stdout | /home2/tester/Desktop/recordingGui-master/gphoto2-liveview-example-master/gphoto2-liveview-example