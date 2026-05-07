"""
Reads RAM and swap usage, plus top memory-consuming processes.
"""

import psutil
import platform
from datetime import datetime, timezone

def ram_pressure():

    sw = psutil.swap_memory()
    vm = psutil.virtual_memory()

    processes = []
    
    for proc in psutil.process_iter(["pid", "name", "memory_info", "memory_percent"]):

        try:
            mem_info = proc.info["memory_info"]
            processes.append({
                "pid": proc.info["pid"],
                "name": proc.info["name"],
                "rss_bytes": mem_info.rss if mem_info else 0,
                "vms_bytes": mem_info.vms if mem_info else 0,
                "memory_percent": round(proc.info["memory_percent"] or 0.0, 2),
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return {
        "detector": "memory_pressure",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": platform.system(),
        "virtual_memory": {
            "total_bytes": vm.total,
            "available_bytes": vm.available,
            "used_bytes": vm.used,
            "free_bytes": vm.free,
            "percent_used": vm.percent,
            "buffers_bytes": getattr(vm, "buffers", None),
            "cached_bytes": getattr(vm, "cached", None),
            "shared_bytes": getattr(vm, "shared", None),
        },
        "swap": {
            "total_bytes": sw.total,
            "used_bytes": sw.used,
            "free_bytes": sw.free,
            "percent_used": sw.percent,
            "sin_bytes": sw.sin,
            "sout_bytes": sw.sout,
        },
    }