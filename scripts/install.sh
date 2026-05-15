#!/bin/bash

set -e

echo "[*] Installing Kokkan..."

# make directory
sudo mkdir -p /opt/kokkan

# copy file
sudo cp -r ../* /opt/kokkan/

# copy systemd files
sudo cp ../systemd/kokkan.service /etc/systemd/system/
sudo cp ../systemd/kokkan.timer /etc/systemd/system/

# reload systemd
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

# enable timer
sudo systemctl enable kokkan.timer
sudo systemctl start kokkan.timer

echo "[OK] Kokkan installed and running"
