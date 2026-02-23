# HamEd Hub Monitor  
### Enterprise‑Grade Miner Monitoring System

HamEd Hub Monitor یک سیستم کامل، پایدار و مقیاس‌پذیر برای مانیتورینگ ماینرهای ASIC در شبکه‌های صنعتی است.  
این پروژه برای فارم‌های واقعی طراحی شده و شامل اسکن شبکه، تشخیص نوع دستگاه، دریافت API ماینرها، داشبورد حرفه‌ای، API داخلی و سیستم لاگ‌گیری است.

---

## 🚀 Features

### 🔍 Network Scanning
- اسکن سریع هر 10 ثانیه  
- اسکن کامل هر 1 ساعت  
- بدون نیاز به nmap  
- تشخیص نوع ماینر از طریق:
  - HTTP Server Header  
  - HTML Title  
- تشخیص آنلاین/آفلاین  
- افزودن خودکار دستگاه‌های جدید  

### ⚙️ Miner API (CGMiner)
- ارتباط مستقیم TCP با پورت 4028  
- دریافت:
  - Hashrate (5s)
  - Temperature
  - Uptime  
- مدیریت خطا، Timeout و پاسخ‌های ناقص  
- قابل توسعه برای مدل‌های جدید ماینر  

### 🗂 Data Storage
- ذخیره دستگاه‌ها در `devices.json`  
- لاگ‌گیری کامل در `hamed_hub.log`  
- Thread‑safe  

### 🌐 Internal REST API
| Endpoint | Description |
|---------|-------------|
| `GET /devices` | لیست کامل دستگاه‌ها |
| `GET /api/miner?ip=` | دریافت API ماینر |
| `GET /scan` | اسکن دستی |
| `GET /export` | خروجی کامل JSON |
| `GET /health` | وضعیت سرویس |

### 🖥 Enterprise UI
- داشبورد مدرن و واکنش‌گرا  
- تم تاریک  
- جدول دستگاه‌ها با رنگ وضعیت  
- آپدیت زنده هر 5 ثانیه  
- Modal برای نمایش API  
- صفحهٔ جزئیات دستگاه  

---

## 📦 Project Structure

hamed_hub_monitor/
├── app/
│   ├── init.py
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
├── config.py
├── requirements.txt
├── run.py
├── devices.json
└── hamed_hub.log

---

## 🛠 Installation

### 1) Clone & Setup
```bash
git clone https://github.com/hamed/hub-monitor.git
cd hub-monitor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2) Run Development Server
sudo python run.py
3) Run Production (Gunicorn)
gunicorn -w 4 -b 0.0.0.0:8000 run:app

Network Requirements

    Network: 172.16.1.0/24

    Server IP: 172.16.1.105

    Ports:

        HTTP: 80

        CGMiner API: 4028
Extendability

HamEd Hub Monitor طوری طراحی شده که بتوانید:

    مدل‌های جدید ماینر اضافه کنید

    UI را گسترش دهید

    APIهای جدید اضافه کنید

    اسکنر را برای شبکه‌های بزرگ‌تر تنظیم کنید

📝 License

Private / Commercial Use Only

