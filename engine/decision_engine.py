import yaml


# ---- CONFIG ----

def load_thresholds():
    with open("config/thresholds.yaml") as f:
        return yaml.safe_load(f)


# ---- DECISION ENGINE ----

def evaluate_disk_usage(context, report, thresholds):
    disk_cfg = thresholds["disk_usage"]["root"]

    decisions = []

    for partition in report.get("partitions", []):
        mount = partition["mountpoint"]
        usage = partition["percent_used"]

        prev = context.get(mount, {"duration": 0})

        # Update state (time above limit)
        if usage >= disk_cfg["critical"]:
            duration = prev["duration"] + 1
        else:
            duration = 0

        context[mount] = {
            "duration": duration
        }

        sustained = duration >= disk_cfg["min_duration_seconds"]

        # ✅ SOLO TARGETING
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


# ---- ORCHESTRATION ENTRY ----

def run_decision(context, report):
    thresholds = load_thresholds()

    decisions = []

    disk_decisions = evaluate_disk_usage(context, report, thresholds)
    decisions.extend(disk_decisions)

    return decisions
