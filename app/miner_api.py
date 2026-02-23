import socket
import json
import logging
from typing import Any, Dict

from config import CGMINER_PORT, SOCKET_TIMEOUT

logger = logging.getLogger(__name__)


def _send_cgminer_command(ip: str, command: str) -> str:
    payload = json.dumps({"command": command})
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(SOCKET_TIMEOUT)
        s.connect((ip, CGMINER_PORT))
        s.sendall(payload.encode("utf-8"))
        chunks = []
        while True:
            try:
                data = s.recv(4096)
            except socket.timeout:
                break
            if not data:
                break
            chunks.append(data)
    return b"".join(chunks).decode("utf-8", errors="ignore")


def _normalize_response(raw: str) -> Dict[str, Any]:
    """
    CGMiner API معمولاً JSON مانند است؛ این تابع تلاش می‌کند آن را به JSON تبدیل کند.
    """
    try:
        # بسیاری از ماینرها JSON معتبر برمی‌گردانند
        return json.loads(raw)
    except Exception:
        pass

    # تلاش ساده برای تبدیل ساختار key=value| به dict
    result: Dict[str, Any] = {}
    try:
        parts = raw.split("|")
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                result[k.strip()] = v.strip()
    except Exception:
        logger.exception("Failed to normalize CGMiner response")
    return result


def get_miner_stats(ip: str) -> Dict[str, Any]:
    """
    برگرداندن خلاصه‌ای از وضعیت ماینر (hashrate, temperature, uptime).
    """
    try:
        summary_raw = _send_cgminer_command(ip, "summary")
        devs_raw = _send_cgminer_command(ip, "devs")
    except Exception as e:
        logger.warning("CGMiner connection error for %s: %s", ip, e)
        return {
            "ip": ip,
            "error": "connection_failed",
            "details": str(e),
        }

    summary = _normalize_response(summary_raw)
    devs = _normalize_response(devs_raw)

    hashrate_5s = None
    uptime = None
    temperature = None

    # summary parsing
    try:
        if isinstance(summary, dict):
            # common keys: "SUMMARY": [{"MHS 5s": ..., "Elapsed": ...}]
            if "SUMMARY" in summary and isinstance(summary["SUMMARY"], list):
                s0 = summary["SUMMARY"][0]
                hashrate_5s = s0.get("MHS 5s") or s0.get("GHS 5s")
                uptime = s0.get("Elapsed")
            else:
                hashrate_5s = summary.get("MHS 5s") or summary.get("GHS 5s")
                uptime = summary.get("Elapsed")
    except Exception:
        logger.exception("Error parsing summary for %s", ip)

    # devs parsing (take max temp)
    try:
        temps = []
        if isinstance(devs, dict):
            if "DEVS" in devs and isinstance(devs["DEVS"], list):
                for d in devs["DEVS"]:
                    for key in ("Temperature", "Temp", "Chip Temp"):
                        if key in d:
                            temps.append(d[key])
            else:
                for key in ("Temperature", "Temp", "Chip Temp"):
                    if key in devs:
                        temps.append(devs[key])
        if temps:
            temperature = max(temps)
    except Exception:
        logger.exception("Error parsing devs for %s", ip)

    return {
        "ip": ip,
        "hashrate_5s": hashrate_5s,
        "uptime": uptime,
        "temperature": temperature,
        "raw": {
            "summary": summary,
            "devs": devs,
        },
    }
