from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class Device:
    ip: str
    type: str = "Unknown"
    title: str = ""
    status: str = "offline"  # "online" / "offline"
    last_seen: Optional[str] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Device":
        return Device(
            ip=data.get("ip", ""),
            type=data.get("type", "Unknown"),
            title=data.get("title", ""),
            status=data.get("status", "offline"),
            last_seen=data.get("last_seen"),
            created_at=data.get("created_at"),
        )

    @staticmethod
    def now_iso() -> str:
        return datetime.utcnow().isoformat() + "Z"
