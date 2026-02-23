#!/bin/bash

set -e

SERVICE_NAME="hamedhub"
APP_DIR="/opt/hamed_hub_monitor"

echo "=========================================="
echo " HamEd Hub Monitor - Uninstaller"
echo "=========================================="

echo "[1/6] Stopping service..."
systemctl stop $SERVICE_NAME || true

echo "[2/6] Disabling service..."
systemctl disable $SERVICE_NAME || true

echo "[3/6] Removing systemd service file..."
rm -f /etc/systemd/system/$SERVICE_NAME.service
systemctl daemon-reload

echo "[4/6] Removing application directory..."
rm -rf $APP_DIR

echo "[5/6] Removing logs..."
rm -f /var/log/hamed_hub.log || true
rm -f $APP_DIR/hamed_hub.log || true

echo "[6/6] Uninstall completed!"
echo "------------------------------------------"
echo " HamEd Hub Monitor has been fully removed."
echo "------------------------------------------"
