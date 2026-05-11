import yaml

# ---- CONFIG ----

def load_thresholds():
    with open("config/thresholds.yaml") as f:
        return yaml.safe_load(f)

# ---- DISK ----

def evaluate_disk_usage(context, report, thresholds):
    disk_cfg = thresholds["disk_usage"]["root"]

    decisions = []

    for part in report.get("partitions", []):
        mount = part["mountpoint"]
        usage = part["percent_used"]

        state = context.get(mount, {})
        duration = state.get("duration", 0)

        sustained = (
            usage >= disk_cfg["critical"]
            and duration >= disk_cfg["min_duration_seconds"]
        )

        if sustained:
            decisions.append({
                "action": "cleanup_disk",
                "target": mount,
                "signal": {
                    "usage": usage,
                    "duration": duration
                }
            })

    return decisions

# ---- MEMORY ----

def evaluate_memory(context, report, thresholds):
    cfg = thresholds["memory"]

    usage = report["percent_used"]
    duration = context.get("memory", {}).get("duration", 0)

    decisions = []

    # ✅ LOGICAL (threshold-based)
    if (
        usage >= cfg["critical"] and
        duration >= cfg["min_duration_seconds"]
    ):
        decisions.append({
            "action": "cleanup_memory",
            "target": "system",
            "signal": {
                "usage": usage,
                "duration": duration
            }
        })

    return decisions

# ---- CPU ----

def evaluate_cpu(context, report, thresholds):
    cfg = thresholds["cpu"]

    usage = report["percent_used"]
    duration = context.get("cpu", {}).get("duration", 0)

    decisions = []

    if (
        usage >= cfg["critical"] and
        duration >= cfg["min_duration_seconds"]
    ):
        decisions.append({
            "action": "throttle_cpu",
            "target": "system",
            "signal": {
                "usage": usage,
                "duration": duration
            }
        })

    return decisions

# ---- NETWORK LATENCY ----

def evaluate_network(context, report, thresholds):
    cfg = thresholds["network_latency"]

    latency = report.get("latency_ms")
    duration = context.get("network", {}).get("duration", 0)

    decisions = []

    if (
        latency is not None and
        latency >= cfg["critical"] and
        duration >= cfg["min_duration_seconds"]
    ):
        decisions.append({
            "action": "investigate_network",
            "target": report.get("target", "unknown"),
            "signal": {
                "latency": latency,
                "duration": duration
            }
        })

    return decisions

# ---- SERVICES ----

def evaluate_services(context, report, thresholds):
    cfg = thresholds["services"]

    decisions = []

    for svc in report.get("services", []):
        name = svc["service"]
        healthy = svc.get("healthy", False)

        duration = context.get(name, {}).get("duration", 0)

        if (
            not healthy and
            duration >= cfg["unhealthy_duration"]
        ):
            decisions.append({
                "action": "restart_service",
                "target": name,
                "signal": {
                    "healthy": healthy,
                    "duration": duration,
                    "state": svc.get("active_state"),
                    "sub_state": svc.get("sub_state")
                }
            })

    return decisions

# ---- ENTRY POINT ----

def run_decision(context, reports, thresholds):
    decisions = []

    decisions.extend(evaluate_disk_usage(context, reports["disk"], thresholds))

    decisions.extend(evaluate_memory(context, reports["memory"], thresholds))
    
    decisions.extend(evaluate_cpu(context, reports["cpu"], thresholds))

    decisions.extend(evaluate_network(context, reports["network"], thresholds))

    decisions.extend(evaluate_services(context, reports["services"], thresholds))

    return decisions
