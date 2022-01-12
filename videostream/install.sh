#!/bin/sh

sudo \cp videostream.service /lib/systemd/system/
sudo systemctl enable videostream.service
sudo systemctl restart videostream.service
