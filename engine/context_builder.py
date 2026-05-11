"""
Context Builder

It maintains the temporal state of signals between cycles.
It does NOT make decisions.
It does NOT apply policy.
It is only used to track the duration of events.
"""

# ---- DISK ----

def update_disk_context(context, report, thresholds):
    cfg = thresholds["disk_usage"]["root"]

    for part in report.get("partitions", []):
        mount = part["mountpoint"]
        usage = part["percent_used"]

        prev = context.get(mount, {}).get("duration", 0)

        if usage >= cfg["critical"]:
            duration = prev + 1
        else:
            duration = 0

        context[mount] = {
            "duration": duration
        }

    return context


# ---- MEMORY ----

def update_memory_context(context, report, thresholds):
    cfg = thresholds["memory"]

    usage = report["percent_used"]
    prev = context.get("memory", {}).get("duration", 0)

    if usage >= cfg["critical"]:
        duration = prev + 1
    else:
        duration = 0

    context["memory"] = {
        "duration": duration
    }

    return context


# ---- CPU ----

def update_cpu_context(context, report, thresholds):
    cfg = thresholds["cpu"]

    usage = report["percent_used"]
    prev = context.get("cpu", {}).get("duration", 0)

    if usage >= cfg["critical"]:
        duration = prev + 1
    else:
        duration = 0

    context["cpu"] = {
        "duration": duration
    }

    return context


# ---- NETWORK LATENCY ----

def update_network_context(context, report, thresholds):
    cfg = thresholds["network_latency"]

    latency = report.get("latency_ms")
    prev = context.get("network", {}).get("duration", 0)

    if latency is not None and latency >= cfg["critical"]:
        duration = prev + 1
    else:
        duration = 0

    context["network"] = {
        "duration": duration
    }

    return context


# ---- SERVICES ----

def update_service_context(context, report, thresholds):
    cfg = thresholds["services"]

    for svc in report.get("services", []):
        name = f"service:{svc['service']}"
        healthy = svc.get("healthy", False)

        prev = context.get(name, {}).get("duration", 0)

        if not healthy:
            duration = prev + 1
        else:
            duration = 0

        context[name] = {
            "duration": duration
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
