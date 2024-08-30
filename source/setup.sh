#!/bin/bash
sudo chmod 777 /dev/ttyACM0
sudo chmod 777 /dev/video0
sudo modprobe v4l2loopback exclusive_caps=1 card_label="GPhoto2 Webcam"/dev/video0

echo Setup Down! 
echo Hit "ENTER" to exit!

read