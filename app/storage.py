import json
import threading
from typing import Dict, List
from pathlib import Path

from .models import Device
from config import DEVICES_FILE


class DeviceStorage:
    def __init__(self, path: Path = DEVICES_FILE):
        self.path = path
        self._lock = threading.RLock()
        self._devices: Dict[str, Device] = {}
        self._load()

    def _load(self) -> None:
        with self._lock:
            if not self.path.exists():
                self._devices = {}
                self._save_locked()
                return
            try:
                with self.path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                self._devices = {
                    ip: Device.from_dict(dev) for ip, dev in data.items()
                }
            except Exception:
                self._devices = {}
                self._save_locked()

    def _save_locked(self) -> None:
        data = {ip: dev.to_dict() for ip, dev in self._devices.items()}
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)

    def save(self) -> None:
        with self._lock:
            self._save_locked()

    def upsert_device(self, device: Device) -> None:
        with self._lock:
            existing = self._devices.get(device.ip)
            if existing:
                # preserve created_at
                if not device.created_at:
                    device.created_at = existing.created_at
            else:
                if not device.created_at:
                    device.created_at = Device.now_iso()
            self._devices[device.ip] = device
            self._save_locked()

    def mark_offline_missing(self, online_ips: List[str]) -> None:
        with self._lock:
            for ip, dev in self._devices.items():
                if ip not in online_ips:
                    dev.status = "offline"
            self._save_locked()

    def get_all(self) -> Dict[str, Device]:
        with self._lock:
            return dict(self._devices)

    def get_list(self) -> List[Device]:
        with self._lock:
            return list(self._devices.values())

    def get_device(self, ip: str) -> Device | None:
        with self._lock:
            return self._devices.get(ip)

    def export_json(self) -> Dict[str, dict]:
        with self._lock:
            return {ip: dev.to_dict() for ip, dev in self._devices.items()}
