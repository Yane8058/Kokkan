# detection of disk usage — returd Json data to parse with others scripts

import psutil
import platform
from datetime import datetime, timezone

def du():

    partitions =[]

    for part in psutil.disk_partitions(all=False):
        # Skip pseudo/virtual filesystems on Linux
        if platform.system() == 'Linux' and part.fstype in ("tmpfs", "devtmpfs", "squashfs", "overlay", "proc", "sysfs", "cgroup", 
         "cgroup2", "pstore", "debugfs", "tracefs", "hugetlbfs", "mqueue"):
            
            continue

        try:
            usage = psutil.disk_usage(part.mountpoint)

        except(PermissionError, OSError):
            continue

        partitions.append({
            "device": part.device,
            "mountpoint": part.mountpoint,
            "fstype": part.fstype,
            "total_bytes": usage.total,
            "used_bytes": usage.used,
            "free_bytes": usage.free,
            "percent_used": usage.percent,
        })

        # Aggregate disk I/O counters

        try:
            io = psutil.disk_io_counters()

            io_stats = {
                "read_count": io.read_count,
                "write_count": io.write_count,
                "read_bytes": io.read_bytes,
                "write_bytes": io.write_bytes,
                "read_time_ms": io.read_time,
                "write_time_ms": io.write_time,
                }

        except (AttributeError, RuntimeError):
            io_stats = None

        return {
        "detector": "disk_usage",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": platform.system(),
        "partitions": partitions,
        "io_stats": io_stats,
        }