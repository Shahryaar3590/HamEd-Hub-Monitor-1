from flask import Blueprint, jsonify, render_template, request, abort

from .storage import DeviceStorage
from .scanner import scan_network, fast_scan
from .miner_api import get_miner_stats
from .models import Device
from config import APP_NAME

bp = Blueprint("main", __name__)

storage = DeviceStorage()


@bp.route("/")
def dashboard():
    devices = storage.get_list()
    total = len(devices)
    online = len([d for d in devices if d.status == "online"])
    offline = total - online
    unknown = len([d for d in devices if d.type == "Unknown"])
    return render_template(
        "dashboard.html",
        app_name=APP_NAME,
        devices=devices,
        total=total,
        online=online,
        offline=offline,
        unknown=unknown,
    )


@bp.route("/device/<ip>")
def device_page(ip: str):
    dev = storage.get_device(ip)
    if not dev:
        abort(404)
    return render_template("device.html", app_name=APP_NAME, device=dev)


# ---------- REST API ----------


@bp.route("/devices", methods=["GET"])
def api_devices():
    devices = [d.to_dict() for d in storage.get_list()]
    return jsonify({"devices": devices})


@bp.route("/api/miner", methods=["GET"])
def api_miner():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "missing_ip"}), 400
    stats = get_miner_stats(ip)
    return jsonify(stats)


@bp.route("/scan", methods=["GET"])
def api_scan():
    # manual full scan
    devices = scan_network()
    online_ips = []
    for dev in devices:
        online_ips.append(dev.ip)
        storage.upsert_device(dev)
    storage.mark_offline_missing(online_ips)
    return jsonify({"status": "ok", "updated": len(devices)})


@bp.route("/export", methods=["GET"])
def api_export():
    data = storage.export_json()
    return jsonify({"devices": data})


@bp.route("/health", methods=["GET"])
def api_health():
    return jsonify({"status": "ok", "app": APP_NAME})


# ---------- Helpers for scheduler ----------


def scheduled_full_scan():
    devices = scan_network()
    online_ips = []
    for dev in devices:
        online_ips.append(dev.ip)
        storage.upsert_device(dev)
    storage.mark_offline_missing(online_ips)


def scheduled_fast_scan():
    known_ips = [d.ip for d in storage.get_list()]
    devices = fast_scan(known_ips)
    online_ips = []
    for dev in devices:
        online_ips.append(dev.ip)
        storage.upsert_device(dev)
    if known_ips:
        storage.mark_offline_missing(online_ips)
