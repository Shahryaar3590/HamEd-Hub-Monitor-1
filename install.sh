#!/bin/bash

set -e

echo "=========================================="
echo " HamEd Hub Monitor - Auto Installer"
echo "=========================================="

APP_DIR="/opt/hamed_hub_monitor"
SERVICE_NAME="hamedhub"

echo "[1/8] Updating system..."
apt update -y && apt upgrade -y

echo "[2/8] Installing dependencies..."
apt install -y python3 python3-venv python3-pip git

echo "[3/8] Creating application directory..."
mkdir -p $APP_DIR
cp -r . $APP_DIR

echo "[4/8] Creating Python virtual environment..."
python3 -m venv $APP_DIR/venv
source $APP_DIR/venv/bin/activate

echo "[5/8] Installing Python requirements..."
pip install --upgrade pip
pip install -r $APP_DIR/requirements.txt

echo "[6/8] Creating systemd service..."
cat > /etc/systemd/system/$SERVICE_NAME.service << SERVICE
[Unit]
Description=HamEd Hub Monitor Service
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/gunicorn -w 4 -b 0.0.0.0:80 run:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

echo "[7/8] Enabling and starting service..."
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

echo "[8/8] Installation completed!"
echo "------------------------------------------"
echo " HamEd Hub Monitor is now running."
echo " Open in browser: http://<your-device-ip>"
echo "------------------------------------------"
