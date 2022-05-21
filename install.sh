#!/bin/sh

echo stopping service
sudo systemctl stop doorbell-control.service

echo install requirements
sudo pip3 install -r requirements.txt

echo install needed libs
sudo apt-get install libavahi-compat-libdnssd-dev

echo install service
sudo mkdir -p /opt/doorbell
sudo cp -r controller /opt/doorbell
sudo cp config.ini /opt/doorbell
sudo \cp doorbell-control.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/doorbell-control.service
sudo systemctl daemon-reload
sudo systemctl enable doorbell-control.service
sudo systemctl restart doorbell-control.service

echo waiting for service start
sleep 8

journalctl -u doorbell-control -n 10
