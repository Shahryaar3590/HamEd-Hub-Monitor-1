cd hamed_hub_monitor
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

sudo python run.py

