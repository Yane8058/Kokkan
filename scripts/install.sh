#!/bin/bash

set -e

echo "[*] Installing Kokkan..."

# System Update & package management
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip unzip wget apt-transport-https software-properties-common -y

# make directory
sudo mkdir -p /opt/kokkan

# copy file
sudo cp -r ../* /opt/kokkan/

# Install python dependecies
pip3 install -r /opt/kokkan/requirements.txt

# Permissions
sudo chmod +x /opt/kokkan/engine/healer.py

# copy systemd files
sudo cp ../systemd/kokkan.service /etc/systemd/system/
sudo cp ../systemd/kokkan.timer /etc/systemd/system/

echo "[OK] Kokkan installed"

# -----------------------------
# Promtail installation
# -----------------------------

echo "[*] Installing Promtail..." 

if [ ! -d /etc/promtail ]; then
  sudo mkdir -p /etc/promtail
fi

# Manual installation — latest version
wget https://github.com/grafana/loki/releases/latest/download/promtail-linux-amd64.zip
unzip promtail-linux-amd64.zip
chmod +x promtail-linux-amd64
sudo mv promtail-linux-amd64 /usr/local/bin/promtail

# copy config file
sudo cp ../config/promtail.yaml /etc/promtail/promtail.yaml

# copy systemd file
sudo cp ../systemd/promtail.service /etc/systemd/system/

echo "[OK] Promtail installed"

# -----------------------------
# Loki installation
# -----------------------------

echo "[*] Installing Loki..." 

if [ ! -d /etc/loki ]; then
  sudo mkdir -p /etc/loki
fi

# Manual installation — latest version
wget https://github.com/grafana/loki/releases/latest/download/loki-linux-amd64.zip
unzip loki-linux-amd64.zip
chmod +x loki-linux-amd64
sudo mv loki-linux-amd64 /usr/local/bin/loki

# copy config file
sudo cp ../config/loki_config.yaml /etc/loki/loki_config.yaml

# copy systemd file
sudo cp ../systemd/loki.service /etc/systemd/system/

echo "[OK] Loki installed"

# -----------------------------
# Grafana installation
# -----------------------------

echo "[*] Installing Grafana..." 

if [ ! -d /etc/apt/keyrings ]; then
  sudo mkdir -p /etc/apt/keyrings
fi

# Add GPG key
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null

# Add repo
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | \
sudo tee /etc/apt/sources.list.d/grafana.list

# Install Grafana
sudo apt update
sudo apt install grafana -y

echo "[OK] Grafana installed"


# -----------------------------
# Services
# -----------------------------

echo "[*] Running them as a Services..." 
# reload systemd

echo "[*] Starting services..."

sudo systemctl daemon-reload

# Kokkan (timer-based)
sudo systemctl enable kokkan.timer
sudo systemctl start kokkan.timer

# Promtail (always-on)
sudo systemctl enable promtail.service
sudo systemctl start promtail.service

# Loki (always-on)
sudo systemctl enable loki.service
sudo systemctl start loki.service

# Grafana (always-on)
sudo systemctl enable grafana-server
sudo systemctl start grafana-server

echo "[OK] All services running"
