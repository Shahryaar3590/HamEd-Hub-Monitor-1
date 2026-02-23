import ipaddress
import logging
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional

import requests

from config import (
    NETWORK_CIDR,
    HTTP_PORT,
    CGMINER_PORT,
    HTTP_TIMEOUT,
    MINER_PATTERNS,
)
from .models import Device

logger = logging.getLogger(__name__)


def _probe_http(ip: str) -> Tuple[Optional[str], Optional[str]]:
    url = f"http://{ip}:{HTTP_PORT}/"
    try:
        resp = requests.get(url, timeout=HTTP_TIMEOUT)
        server = resp.headers.get("Server", "")
        title = ""
        if "<title>" in resp.text.lower():
            lower = resp.text.lower()
            start = lower.find("<title>")
            end = lower.find("</title>", start)
            if start != -1 and end != -1:
                title = resp.text[start + 7 : end].strip()
        return server, title
    except Exception:
        return None, None


def _probe_cgminer(ip: str) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)
            s.connect((ip, CGMINER_PORT))
        return True
    except Exception:
        return False


def _detect_type(server: str, title: str) -> str:
    text = f"{server} {title}".lower()
    for miner_type, patterns in MINER_PATTERNS.items():
        for p in patterns:
            if p.lower() in text:
                return miner_type
    return "Unknown"


def _scan_ip(ip: str) -> Optional[Device]:
    server, title = _probe_http(ip)
    cg = _probe_cgminer(ip)

    if not server and not title and not cg:
        return None

    dtype = _detect_type(server or "", title or "")
    dev = Device(
        ip=ip,
        type=dtype,
        title=title or "",
        status="online",
        last_seen=Device.now_iso(),
    )
    return dev


def iter_network_ips() -> List[str]:
    net = ipaddress.ip_network(NETWORK_CIDR, strict=False)
    ips = [str(ip) for ip in net.hosts()]
    return ips


def scan_network(max_workers: int = 64) -> List[Device]:
    logger.info("Starting full network scan on %s", NETWORK_CIDR)
    ips = iter_network_ips()
    devices: List[Device] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_scan_ip, ip): ip for ip in ips}
        for fut in as_completed(futures):
            dev = fut.result()
            if dev:
                devices.append(dev)

    logger.info("Full scan completed. Found %d devices", len(devices))
    return devices


def fast_scan(known_ips: List[str], max_workers: int = 32) -> List[Device]:
    """
    اسکن سریع فقط روی IPهای شناخته‌شده.
    """
    logger.debug("Starting fast scan on %d known devices", len(known_ips))
    devices: List[Device] = []
    if not known_ips:
        return devices

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_scan_ip, ip): ip for ip in known_ips}
        for fut in as_completed(futures):
            dev = fut.result()
            if dev:
                devices.append(dev)

    logger.debug("Fast scan completed. Updated %d devices", len(devices))
    return devices
