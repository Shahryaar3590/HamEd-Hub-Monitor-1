import logging
from pathlib import Path

# Network configuration
NETWORK_CIDR = "172.16.1.0/24"
SERVER_IP = "172.16.1.105"
HTTP_PORT = 80
CGMINER_PORT = 4028

# Scan intervals (seconds)
FAST_SCAN_INTERVAL = 10
FULL_SCAN_INTERVAL = 3600

# Paths
BASE_DIR = Path(__file__).resolve().parent
DEVICES_FILE = BASE_DIR / "devices.json"
LOG_FILE = BASE_DIR / "hamed_hub.log"

# Logging configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"

# HTTP / socket timeouts
HTTP_TIMEOUT = 2
SOCKET_TIMEOUT = 3

# Miner detection patterns (extensible)
MINER_PATTERNS = {
    "Whatsminer": ["whatsminer", "whatsminer controller"],
    "Antminer": ["antminer", "bitmain"],
    "Avalon": ["avalon", "canaan"],
}

# UI configuration
APP_NAME = "HamEd Hub Monitor"
