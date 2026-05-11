import yaml

# ---- CONFIG ----

def load_thresholds():
    with open("config/thresholds.yaml") as f:
        return yaml.safe_load(f)

# ---- DECISION ENGINE ----

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
