"""
🌲 Forest Fire Alert Agent — Sensor Simulator
================================================
Simulates realistic heat sensor readings from different
forest zones. In a real deployment, replace this with
actual API calls to your physical sensor network.
"""

import random
from datetime import datetime


# ── Sensor Zone Definitions ──────────────────────────────────────────────────
SENSOR_ZONES = [
    {"id": "ZONE-A", "name": "North Ridge Forest",   "base_temp": 28.0},
    {"id": "ZONE-B", "name": "Valley Stream Area",    "base_temp": 24.0},
    {"id": "ZONE-C", "name": "East Slope Woodland",   "base_temp": 30.0},
    {"id": "ZONE-D", "name": "South Pine Cluster",    "base_temp": 26.0},
    {"id": "ZONE-E", "name": "Central Grove Station", "base_temp": 27.5},
]

# Alert thresholds (°C)
THRESHOLD_WARNING  = 45.0   # Elevated — monitor closely
THRESHOLD_DANGER   = 60.0   # High risk — prepare response
THRESHOLD_CRITICAL = 80.0   # FIRE DETECTED — immediate action!


# ── Simulated Reading ─────────────────────────────────────────────────────────
def get_sensor_readings(scenario: str = "normal") -> list[dict]:
    """
    Return simulated sensor readings for all zones.

    Parameters
    ----------
    scenario : str
        "normal"   — typical forest temperatures
        "elevated" — one zone heating up (early warning)
        "fire"     — one zone at critical level (fire active)
    """
    readings = []
    fire_zone = random.choice(SENSOR_ZONES)

    for zone in SENSOR_ZONES:
        base = zone["base_temp"]

        if scenario == "normal":
            temp = round(base + random.uniform(-2.0, 4.0), 1)
        elif scenario == "elevated":
            if zone["id"] == fire_zone["id"]:
                temp = round(random.uniform(45.0, 62.0), 1)
            else:
                temp = round(base + random.uniform(-2.0, 5.0), 1)
        elif scenario == "fire":
            if zone["id"] == fire_zone["id"]:
                temp = round(random.uniform(78.0, 120.0), 1)
            else:
                temp = round(base + random.uniform(-1.0, 8.0), 1)
        else:
            temp = round(base + random.uniform(-2.0, 4.0), 1)

        # Determine alert level
        if temp >= THRESHOLD_CRITICAL:
            level = "🔴 CRITICAL"
        elif temp >= THRESHOLD_DANGER:
            level = "🟠 DANGER"
        elif temp >= THRESHOLD_WARNING:
            level = "🟡 WARNING"
        else:
            level = "🟢 NORMAL"

        readings.append({
            "zone_id":   zone["id"],
            "zone_name": zone["name"],
            "temp_c":    temp,
            "alert":     level,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    return readings


def format_readings_for_ai(readings: list[dict]) -> str:
    """Format sensor readings into a clean text block for the AI prompt."""
    lines = ["🌲 LIVE FOREST HEAT SENSOR READINGS", "=" * 40]
    for r in readings:
        lines.append(
            f"  {r['alert']}  |  {r['zone_name']} ({r['zone_id']})"
            f"  →  {r['temp_c']}°C  |  {r['timestamp']}"
        )
    lines.append("=" * 40)
    return "\n".join(lines)
