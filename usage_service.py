import json
import os
from datetime import date

DAILY_LIMIT = 20
USAGE_FILE = os.path.join(os.path.dirname(__file__), "usage.json")


def _today_str():
    return date.today().isoformat()


def _default_data():
    return {"date": _today_str(), "count": 0}


def _read_usage_data():
    if not os.path.exists(USAGE_FILE):
        return _default_data()

    try:
        with open(USAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return _default_data()

    if not isinstance(data, dict):
        return _default_data()

    saved_date = str(data.get("date", ""))
    saved_count = data.get("count", 0)

    try:
        saved_count = int(saved_count)
    except Exception:
        saved_count = 0

    if saved_count < 0:
        saved_count = 0

    normalized = {"date": saved_date, "count": saved_count}
    if saved_date != _today_str():
        normalized = _default_data()

    return normalized


def _write_usage_data(data):
    with open(USAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_usage_status():
    data = _read_usage_data()
    _write_usage_data(data)

    count = data["count"]
    remaining = max(0, DAILY_LIMIT - count)
    return {
        "date": data["date"],
        "count": count,
        "remaining": remaining,
        "limit": DAILY_LIMIT,
    }


def can_use_ai():
    status = get_usage_status()
    return status["remaining"] > 0


def register_ai_use():
    data = _read_usage_data()

    if data["count"] < DAILY_LIMIT:
        data["count"] += 1

    _write_usage_data(data)
    return get_usage_status()
