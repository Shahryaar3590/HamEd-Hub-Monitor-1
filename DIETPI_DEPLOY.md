# HamEd Hub Monitor – Deployment Guide for DietPi
این راهنما به شما کمک می‌کند HamEd Hub Monitor را روی سیستم‌های سبک مانند **DietPi** به‌صورت پایدار، امن و دائمی اجرا کنید.

---

# 📌 Requirements
- DietPi (Debian-based)
- Python 3.10+
- Network: `172.16.1.0/24`
- Server IP: `172.16.1.105`
- Ports:
  - HTTP → 80
  - CGMiner API → 4028

---

# 🧰 1) Update System
```bash
sudo apt update && sudo apt upgrade -y

 2) Install Python & Tools
bash

sudo apt install -y python3 python3-venv python3-pip git

 3) Clone Project

cd /opt
sudo git clone https://github.com/hamed/hub-monitor.git
sudo chown -R $USER:$USER hub-monitor
cd hub-monitor

 4) Create Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

 5) Test Run (Optional)
sudo python run.py
🛠 6) Create Systemd Service
sudo tee /etc/systemd/system/hamedhub.service > /dev/null << 'SERVICE'
[Unit]
Description=HamEd Hub Monitor Service
After=network.target

[Service]
User=root
WorkingDirectory=/opt/hub-monitor
ExecStart=/opt/hub-monitor/venv/bin/gunicorn -w 4 -b 0.0.0.0:80 run:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

▶️ 7) Enable & Start Service
sudo systemctl daemon-reload
sudo systemctl enable hamedhub
sudo systemctl start hamedhub
وضعیت سرویس
sudo systemctl status hamedhub

 8) Security Hardening (Recommended)
Disable SSH Password Login
sudo nano /etc/ssh/sshd_config
تغییر دهید:
PasswordAuthentication no

سپس

sudo systemctl restart ssh

Firewall (UFW)
sudo apt install ufw -y
sudo ufw allow 80/tcp
sudo ufw allow 22/tcp
sudo ufw enable
 9) Log Location

    Application logs → hamed_hub.log

    Systemd logs → journalctl -u hamedhub -f

🔄 10) Restart Service
sudo systemctl restart hamedhub
 11) Updating the App
cd /opt/hub-monitor
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart hamedhub
Deployment Complete!

HamEd Hub Monitor اکنون روی DietPi به‌صورت پایدار، امن و آمادهٔ استفاده اجرا می‌شود.

