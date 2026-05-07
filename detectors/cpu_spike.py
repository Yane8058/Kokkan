"""
Reads CPU utilisation (overall + per-core), load average, and top CPU processes.
"""

import psutil
import platform
from datetime import datetime, timezone

def cpu_spike():

    # Block for `interval` seconds to get a meaningful reading
    cpu_percent_total = psutil.cpu_percent(interval=0.5)
    per_core = psutil.cpu_percent(percpu=True)  # non-blocking after first call

    freq = psutil.cpu_freq()
    cpu_freq = {
        "current_mhz": round(freq.current, 1) if freq else None,
        "min_mhz": round(freq.min, 1) if freq else None,
        "max_mhz": round(freq.max, 1) if freq else None,
    }

    # Load average (Unix only)
    try:
        load1, load5, load15 = psutil.getloadavg()
        load_avg = {"1m": round(load1, 2), "5m": round(load5, 2), "15m": round(load15, 2)}

    except (AttributeError, OSError):
        load_avg = None
 
    # CPU times breakdown
    ct = psutil.cpu_times_percent(interval=None)
    cpu_times = {
        "user": ct.user,
        "system": ct.system,
        "idle": ct.idle,
        "iowait": getattr(ct, "iowait", None),
        "steal": getattr(ct, "steal", None),
        "nice": getattr(ct, "nice", None),
    }

    return {
        "detector": "cpu_spike",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": platform.system(),
        "logical_cores": psutil.cpu_count(logical=True),
        "physical_cores": psutil.cpu_count(logical=False),
        "cpu_percent_total": cpu_percent_total,
        "cpu_percent_per_core": per_core,
        "cpu_times_percent": cpu_times,
        "cpu_freq": cpu_freq,
        "load_avg": load_avg,
    }