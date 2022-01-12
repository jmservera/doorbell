#!/bin/bash

# RTSP simple server from https://github.com/aler9/rtsp-simple-server
./rtsp-simple-server &

# ffmpeg connects to the EasyCAP deivce found in /dev/video0 and the audio in [2,0]
# as found with the command
# cat /proc/asound/devices
# we use the v4l2  library to import the video from easycap

ffmpeg -f v4l2 -thread_queue_size 512 \
-input_format yuv420p -video_size 640x480 -i /dev/video0 \
-f alsa -thread_queue_size 4096 -i plughw:1,0 \
-c:a aac -b:a 128k -ar 44100 \
-vf drawtext="expansion=strftime:fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf':fontsize=14:fontcolor=white:shadowcolor=black:shadowx=2:shadowy=1:text='%Y-%m-%d\ %H\:%M\:%S':x=8:y=8" \
-c:v h264_omx -b:v 2048k \
-f rtsp -rtsp_transport tcp rtsp://localhost:8554/mystream

 #-acodec pcm_s16le -ac 1 -ar 48000 -copytb 1 -use_wallclock_as_timestamps 1 -c:a aac -b:a 128k -ar 44100 \
#-b:v 4M -c:v h264_omx \


# this command waits for any of the previous processes to end
# so it will end the complete script and the service will restart if any of the
# processes failed
# wait -n
