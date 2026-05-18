"""
Context Builder

It maintains the temporal state of signals between cycles.
It does NOT make decisions.
It does NOT apply policy.
It is only used to track the duration of events.
"""

# Minimum consecutive cycles before a signal is considered stable (noise suppression).
# services = 1 because failures are always significant and should never be ignored.
STABILITY_REQUIRED = {
    "disk":     3,
    "memory":   2,
    "cpu":      3,
    "network":  2,
    "services": 1,
}


# ---- DISK ----

def update_disk_context(context, report, thresholds):
    cfg = thresholds["disk_usage"]["root"]

    for part in report.get("partitions", []):
        mount = part["mountpoint"]
        usage = part["percent_used"]

        prev_warn     = context.get(mount, {}).get("warn_duration", 0)
        prev_critical = context.get(mount, {}).get("critical_duration", 0)

        warn_duration     = prev_warn + 1     if usage >= cfg["warn"]     else 0
        critical_duration = prev_critical + 1 if usage >= cfg["critical"] else 0

        context[mount] = {
            "warn_duration":     warn_duration,
            "critical_duration": critical_duration,
            "stable": warn_duration >= STABILITY_REQUIRED["disk"],
        }

    return context


# ---- MEMORY ----

def update_memory_context(context, report, thresholds):
    cfg = thresholds["memory_pressure"]

    usage         = report["percent_used"]
    prev_warn     = context.get("memory", {}).get("warn_duration", 0)
    prev_critical = context.get("memory", {}).get("critical_duration", 0)

    warn_duration     = prev_warn + 1     if usage >= cfg["warn"]     else 0
    critical_duration = prev_critical + 1 if usage >= cfg["critical"] else 0

    context["memory"] = {
        "warn_duration":     warn_duration,
        "critical_duration": critical_duration,
        "stable": warn_duration >= STABILITY_REQUIRED["memory"],
    }

    return context


# ---- CPU ----

def update_cpu_context(context, report, thresholds):
    cfg = thresholds["cpu_spike"]

    usage         = report["percent_used"]
    prev_warn     = context.get("cpu", {}).get("warn_duration", 0)
    prev_critical = context.get("cpu", {}).get("critical_duration", 0)

    warn_duration     = prev_warn + 1     if usage >= cfg["warn"]     else 0
    critical_duration = prev_critical + 1 if usage >= cfg["critical"] else 0

    context["cpu"] = {
        "warn_duration":     warn_duration,
        "critical_duration": critical_duration,
        "stable": warn_duration >= STABILITY_REQUIRED["cpu"],
    }

    return context


# ---- NETWORK LATENCY ----

def update_network_context(context, report, thresholds):
    cfg = thresholds["network_latency"]

    latency       = report.get("latency_ms", 0)
    prev_warn     = context.get("network", {}).get("warn_duration", 0)
    prev_critical = context.get("network", {}).get("critical_duration", 0)

    warn_duration     = prev_warn + 1     if latency >= cfg["warn_ms"]     else 0
    critical_duration = prev_critical + 1 if latency >= cfg["critical_ms"] else 0

    context["network"] = {
        "warn_duration":     warn_duration,
        "critical_duration": critical_duration,
        "stable": warn_duration >= STABILITY_REQUIRED["network"],
    }

    return context


# ---- SERVICES ----

def update_service_context(context, report, thresholds):
    cfg = thresholds["service_health"]

    for svc in report.get("services", []):
        name    = f"service:{svc['service']}"
        healthy = svc.get("healthy", False)

        prev_duration = context.get(name, {}).get("duration", 0)
        duration      = prev_duration + 1 if not healthy else 0

        context[name] = {
            "duration": duration,
            "stable":   duration >= STABILITY_REQUIRED["services"],
        }

    return context


# ---- ENTRY POINT ----

def update_context(context, reports, thresholds):
    """
    Entrypoint for context update.
    """
    context = update_disk_context(context, reports["disk"], thresholds)
    context = update_memory_context(context, reports["memory"], thresholds)
    context = update_cpu_context(context, reports["cpu"], thresholds)
    context = update_network_context(context, reports["network"], thresholds)
    context = update_service_context(context, reports["services"], thresholds)

    return context