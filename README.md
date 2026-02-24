# HamEd Hub Monitor
### Enterprise‑Grade ASIC Miner Monitoring System

HamEd Hub Monitor یک سیستم کامل، پایدار و مقیاس‌پذیر برای مانیتورینگ ماینرهای ASIC در شبکه‌های صنعتی است.
این پروژه برای فارم‌های واقعی طراحی شده و شامل اسکن شبکه، تشخیص نوع دستگاه، دریافت API ماینرها، داشبورد حرفه‌ای، API داخلی و سیستم لاگ‌گیری است.

این نسخه شامل ۵ اصلاح مهم است:

1. ایجاد دایرکتوری‌های لازم در زمان نصب
2. اسکریپت نصب و حذف استاندارد و قابل‌اعتماد
3. README حرفه‌ای و هماهنگ با ساختار پروژه
4. عدم Listen روی 0.0.0.0 و استفاده از 127.0.0.1 برای امنیت
5. ارائه تمام فایل‌ها با cat EOF برای جلوگیری از خطای انسانی

---
## 🚀 Features

### 🔍 Network Scanning
- اسکن سریع هر 10 ثانیه
- اسکن کامل هر 1 ساعت
- بدون نیاز به nmap
- تشخیص نوع ماینر از طریق HTTP Header و HTML Title
- تشخیص آنلاین/آفلاین
- افزودن خودکار دستگاه‌های جدید

---

### ⚙️ Miner API (CGMiner)
- ارتباط مستقیم TCP با پورت 4028
- دریافت Hashrate، Temperature، Uptime
- مدیریت Timeout و خطا
- قابل توسعه برای مدل‌های جدید ماینر

---

### 🗂 Data Storage
- ذخیره دستگاه‌ها در devices.json
- لاگ‌گیری کامل در logs/
- Thread‑safe
- ساختار JSON تمیز و قابل توسعه

---
### 🌐 Internal REST API

| Endpoint | Description |
|---------|-------------|
| GET /devices | لیست کامل دستگاه‌ها |
| GET /api/miner?ip= | دریافت API ماینر |
| GET /scan | اسکن دستی |
| GET /export | خروجی کامل JSON |
| GET /health | وضعیت سرویس |

---

## 🖥 Enterprise‑Grade UI

- داشبورد مدرن و واکنش‌گرا
- تم تاریک
- جدول وضعیت با رنگ‌بندی
- آپدیت زنده هر 5 ثانیه
- Modal نمایش API
- صفحهٔ جزئیات دستگاه

---
# 📁 Project Structure

HamEd_Hub_Monitor_1/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── scanner.py
│   ├── miner_api.py
│   ├── storage.py
│   ├── scheduler.py
│   └── models.py
├── templates/
│   ├── layout.html
│   ├── dashboard.html
│   └── device.html
├── static/
│   ├── css/style.css
│   └── js/main.js
├── logs/
│   └── .gitkeep
├── config.py
├── requirements.txt
├── run.py
├── install.sh
├── uninstall.sh
├── devices.json
└── hamed_hub.log (runtime)

---
# 🔐 Security Notes

- Flask فقط روی 127.0.0.1:8000 اجرا می‌شود
- Gunicorn نیز فقط روی localhost اجرا می‌شود
- دسترسی خارجی فقط از طریق Reverse Proxy یا SSH Tunnel یا VPN

---

# 🛠 Installation (Auto Installer)

sudo bash install.sh

---

# 🧹 Uninstall

sudo bash uninstall.sh

---

# 🧩 Development Mode

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py

---

# 📌 File Creation Standard (Important)

تمام فایل‌ها باید با این روش ساخته شوند:

cat << 'EOF' > filename
...content...
EOF

---

# 📝 License

Private / Commercial Use Only  
All rights reserved.
