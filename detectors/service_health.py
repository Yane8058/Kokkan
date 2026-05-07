"""
Checks systemd unit status (Linux) or process-based health (cross-platform).
Returns structured JSON with per-service state, PID, and resource usage.
"""

import os
import subprocess
import platform
import psutil
from datetime import datetime, timezone
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

_raw = os.getenv("KOKKAN_SERVICES", "nginx,sshd,postgresql,redis,docker,cron")
DEFAULT_SERVICES = [s.strip() for s in _raw.split(",") if s.strip()]


# ── Linux / systemd helpers ──────────────────────────────────────────────────

def _systemctl_status(unit: str) -> dict:
    """Query systemd for a unit's state, sub-state, PID, and description."""
    props = ["ActiveState", "SubState", "MainPID", "Description", "LoadState", "Result"]
    cmd = ["systemctl", "show", unit, "--no-pager"] + [f"--property={p}" for p in props]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return {"available": False}

    data: dict = {"available": True}
    for line in out.splitlines():
        if "=" in line:
            key, _, val = line.partition("=")
            data[key] = val

    return {
        "available": True,
        "active_state": data.get("ActiveState"),        # active | inactive | failed | ...
        "sub_state": data.get("SubState"),              # running | dead | exited | ...
        "load_state": data.get("LoadState"),            # loaded | not-found | masked
        "result": data.get("Result"),                   # success | exit-code | ...
        "description": data.get("Description"),
        "main_pid": int(data["MainPID"]) if data.get("MainPID", "0").isdigit() else None,
    }


# ── Process-level resource snapshot ─────────────────────────────────────────

def _proc_snapshot(pid: Optional[int]) -> Optional[dict]:
    if not pid:
        return None
    try:
        proc = psutil.Process(pid)
        with proc.oneshot():
            mem = proc.memory_info()
            return {
                "pid": pid,
                "status": proc.status(),
                "cpu_percent": proc.cpu_percent(interval=0.1),
                "rss_bytes": mem.rss,
                "vms_bytes": mem.vms,
                "num_threads": proc.num_threads(),
                "create_time": proc.create_time(),
            }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


# ── Cross-platform fallback: find process by name ───────────────────────────

def _find_process(name: str) -> Optional[dict]:
    """Return the first matching process snapshot or None."""
    for proc in psutil.process_iter(["pid", "name", "status"]):
        try:
            if name.lower() in proc.info["name"].lower():
                return _proc_snapshot(proc.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


# ── Main detector ────────────────────────────────────────────────────────────

def detect(services: list = None) -> dict:
    targets = services or DEFAULT_SERVICES
    is_linux = platform.system() == "Linux"
    results = []

    for svc in targets:
        entry: dict = {"service": svc}

        if is_linux:
            sd = _systemctl_status(svc)
            entry.update(sd)

            pid = entry.get("main_pid")
            entry["process"] = _proc_snapshot(pid) if pid else _find_process(svc)

            # Derive simple healthy flag
            entry["healthy"] = (
                entry.get("active_state") == "active"
                and entry.get("sub_state") == "running"
            )
        else:
            # Non-Linux: rely purely on process presence
            snap = _find_process(svc)
            entry["process"] = snap
            entry["healthy"] = snap is not None

        results.append(entry)

    return {
        "detector": "service_health",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": platform.system(),
        "services": results,
    }
