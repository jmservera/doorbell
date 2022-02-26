#!/bin/sh

sudo systemctl stop videostream.service

sudo mkdir -p /opt/videostream/thumbnail

# install rtsp-simple-server

wget -q https://github.com/aler9/rtsp-simple-server/releases/download/v0.17.17/rtsp-simple-server_v0.17.17_linux_armv7.tar.gz -O - | tar xzvf - -C /opt/videostream
sudo cp rtsp-simple-server.yml /opt/videostream

sudo \cp videostream.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/videostream.service
sudo systemctl daemon-reload
sudo systemctl enable videostream.service
sudo systemctl restart videostream.service

sleep 1
journalctl -u videostream -n 50
