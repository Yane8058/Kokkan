"""
Reads NIC statistics, active connections count, and measures ICMP latency
to a configurable set of probe targets.
"""

import json
import time
import socket
import platform
import psutil
from datetime import datetime, timezone

# Default probe targets — override via config/global.yaml in the full engine
DEFAULT_PROBE_TARGETS = [
    {"host": "8.8.8.8", "label": "google_dns"},
    {"host": "1.1.1.1", "label": "cloudflare_dns"},
]

PROBE_TIMEOUT = 2.0  # seconds


def _tcp_probe(host: str, port: int = 443, timeout: float = PROBE_TIMEOUT) -> dict:
    """Measure TCP handshake latency as a proxy for network RTT."""
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            return {"reachable": True, "latency_ms": elapsed_ms, "error": None}
    except OSError as exc:
        return {"reachable": False, "latency_ms": None, "error": str(exc)}


def detect(probe_targets: list = None) -> dict:
    targets = probe_targets or DEFAULT_PROBE_TARGETS

    # NIC stats (bytes/packets sent & received, errors, drops)
    net_io = psutil.net_io_counters(pernic=True)
    interfaces = {}
    for nic, stats in net_io.items():
        interfaces[nic] = {
            "bytes_sent": stats.bytes_sent,
            "bytes_recv": stats.bytes_recv,
            "packets_sent": stats.packets_sent,
            "packets_recv": stats.packets_recv,
            "errin": stats.errin,
            "errout": stats.errout,
            "dropin": stats.dropin,
            "dropout": stats.dropout,
        }

    # Interface addresses
    addrs = psutil.net_if_addrs()
    addresses = {}
    for nic, addr_list in addrs.items():
        addresses[nic] = [
            {
                "family": str(a.family),
                "address": a.address,
                "netmask": a.netmask,
                "broadcast": a.broadcast,
            }
            for a in addr_list
        ]

    # Active connection summary
    try:
        conns = psutil.net_connections(kind="inet")
        conn_summary = {
            "total": len(conns),
            "established": sum(1 for c in conns if c.status == "ESTABLISHED"),
            "listen": sum(1 for c in conns if c.status == "LISTEN"),
            "time_wait": sum(1 for c in conns if c.status == "TIME_WAIT"),
            "close_wait": sum(1 for c in conns if c.status == "CLOSE_WAIT"),
        }
    except (psutil.AccessDenied, AttributeError):
        conn_summary = None

    # Latency probes (TCP connect to port 443)
    probes = []
    for target in targets:
        result = _tcp_probe(target["host"])
        probes.append({
            "label": target.get("label", target["host"]),
            "host": target["host"],
            **result,
        })

    return {
        "detector": "network_latency",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": platform.system(),
        "interfaces": interfaces,
        "addresses": addresses,
        "connections": conn_summary,
        "latency_probes": probes,
    }