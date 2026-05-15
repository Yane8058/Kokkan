#!/bin/bash

set -e

echo "[*] Removing Kokkan..."

sudo systemctl stop kokkan.timer
sudo systemctl disable kokkan.timer

sudo rm /etc/systemd/system/kokkan.timer
sudo rm /etc/systemd/system/kokkan.service

sudo systemctl daemon-reload

sudo rm -rf /opt/kokkan

echo "[OK] Kokkan removed"
