"""
Healer - Kokkan main orchestrator
"""

import yaml
import time

# ---- DETECTORS ----

from detectors.disk_usage import du
from detectors.memory_pressure import memory_pressure
from detectors.cpu_usage import cpu_usage
from detectors.network_latency import network_latency
from detectors.service_health import detect as detect_services

# ---- SAFEGUARDS ----
from safeguards.action_validator import validate_action

# ---- ENGINE ----

from engine.context_builder import update_context
from engine.decision_engine import run_decision


# ---- CONFIG ----

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_config():
    return {
        "global": load_yaml("config/global.yaml"),
        "thresholds": load_yaml("config/thresholds.yaml"),
        "actions": load_yaml("config/actions.yaml"),
    }


# ---- EXECUTION ----

def execute(decision, dry_run):
    if dry_run:
        print(f"[DRY-RUN] {decision}")
        return

    # placeholder
    print(f"[EXECUTE] {decision}")


# ---- MAIN LOOP ----

def run_cycle(context):
    cfg = load_config()

    thresholds = cfg["thresholds"]
    actions_cfg = cfg["actions"]
    global_cfg = cfg["global"]

    # ---- DETECTORS ----
    reports = {
        "disk": du(),
        "memory": memory_pressure(),
        "cpu": cpu_usage(),
        "network": network_latency(),
        "services": detect_services()
    }

    # ---- CONTEXT ----
    context = update_context(context, reports, thresholds)

    # ---- DECISION ----
    decisions = run_decision(context, reports, thresholds)

    # ---- VALIDATION + EXECUTION ----
    for d in decisions:
        allowed, reason = validate_action(d, actions_cfg)

        if not allowed:
            print(f"[SKIP] {reason} → {d}")
            continue

        execute(d, global_cfg.get("dry_run", True))

    return context


# ---- ENTRY POINT ----

if __name__ == "__main__":
    context = {}

    while True:
        context = run_cycle(context)
        time.sleep(10)
