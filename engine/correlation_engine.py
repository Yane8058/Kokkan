"""
correlation_engine.py - Evaluates correlation rules against active threshold signals.
Reads stability state from context (produced by context_builder).
"""

from datetime import datetime


# Maps correlation.yaml source keys → context keys (as built by context_builder)
_SOURCE_TO_CONTEXT = {
    "disk_usage":       "disk",
    "memory_pressure":  "memory",
    "cpu_spike":        "cpu",
    "network_latency":  "network",
    "service_health":   "services",
}


# ── INTERNAL HELPERS ──────────────────────────────────────────────────────────

def _context_key(source):
    """Resolve a correlation source string to its context key.
    Handles dot-notation (e.g. 'disk_usage.root' → 'disk').
    """
    base = source.split(".")[0]
    return _SOURCE_TO_CONTEXT.get(base, base)


def _is_stable(context, source):
    """Return True if the signal for this source has passed noise suppression."""
    key = _context_key(source)

    # services are tracked per-service: check if any service entry is stable
    if key == "services":
        return any(
            v.get("stable", False)
            for k, v in context.items()
            if k.startswith("service:")
        )

    return context.get(key, {}).get("stable", False)


def _is_breached(reports, thresholds, source, level):
    """Check if a given source+level is currently breached (raw signal check)."""
    base = source.split(".")[0]

    if base == "disk_usage":
        val   = reports.get("disk", {}).get("usage_percent", 0)
        limit = thresholds["disk_usage"]["root"].get(
            level if level != "breach" else "warn", 0
        )
        return val >= limit

    elif base == "memory_pressure":
        val   = reports.get("memory", {}).get("percent_used", 0)
        limit = thresholds["memory_pressure"].get(level, 0)
        return val >= limit

    elif base == "cpu_spike":
        val   = reports.get("cpu", {}).get("percent_used", 0)
        limit = thresholds["cpu_spike"].get(level, 0)
        return val >= limit

    elif base == "network_latency":
        val   = reports.get("network", {}).get("latency_ms", 0)
        key   = "warn_ms" if level == "warn" else "critical_ms"
        limit = thresholds["network_latency"].get(key, 0)
        return val >= limit

    elif base == "service_health":
        failures = reports.get("services", {}).get("failure_count", 0)
        limit    = thresholds["service_health"].get("restart_threshold", 5)
        return failures >= limit

    return False


def _is_inhibited(reports, thresholds, correlations, responder):
    """Return True if a responder is currently blocked by an inhibition rule."""
    for rule in correlations:
        if rule.get("type") != "inhibition":
            continue
        if rule.get("inhibit_responder") != responder:
            continue
        when = rule.get("when_threshold_active", {})
        if _is_breached(reports, thresholds, when["source"], when["level"]):
            print(f"[INHIBIT] '{responder}' blocked → {rule['reason']}")
            return True
    return False


def _involved_sources(rule):
    """Extract all threshold source strings from a rule."""
    return [t["source"] for t in rule.get("thresholds", [])]


# ── RULE EVALUATORS ───────────────────────────────────────────────────────────

def _eval_compound(rule, reports, thresholds, context):
    """AND rule: all thresholds must be breached AND stable."""
    for t in rule.get("thresholds", []):
        if not _is_breached(reports, thresholds, t["source"], t["level"]):
            return False, rule
        if not _is_stable(context, t["source"]):
            print(f"[NOISE] '{rule['id']}' skipped — '{t['source']}' not yet stable")
            return False, rule
    return True, rule


def _eval_composite(rule, reports, thresholds, context):
    """OR rule with min_breached: enough stable signals must be active."""
    threshold_list = rule.get("thresholds", [])
    stable_breached = sum(
        1 for t in threshold_list
        if _is_breached(reports, thresholds, t["source"], t["level"])
        and _is_stable(context, t["source"])
    )

    required = rule.get("min_breached", 1)
    if stable_breached < required:
        if stable_breached > 0:
            print(f"[NOISE] '{rule['id']}' skipped — only {stable_breached}/{required} stable signals")
        return False, rule

    # escalate severity if enough stable signals fire
    escalate_at = rule.get("escalate_if_breached")
    if escalate_at and stable_breached >= escalate_at:
        rule = {**rule, "severity": rule.get("escalated_severity", rule.get("base_severity", "high"))}
        print(f"[ESCALATE] '{rule['id']}' severity raised to '{rule['severity']}'")

    return True, rule


def _eval_escalation(rule, reports, thresholds, context):
    """Log/notify when a signal persists at a given level."""
    source = rule["source"]
    level  = rule["source_level"]

    if _is_breached(reports, thresholds, source, level) and _is_stable(context, source):
        if rule.get("notify"):
            print(
                f"[ESCALATION] '{rule['id']}': '{source}' stable at '{level}'"
                f" → escalate to '{rule['escalate_to_level']}'"
            )


# ── MAIN ENTRY POINT ──────────────────────────────────────────────────────────

def evaluate_correlations(reports, thresholds, correlation_cfg, context=None):
    """
    Evaluate all correlation rules against current reports and context.

    Returns a list of decisions, each containing:
        action, target, severity, correlation_id, source, timestamp
    """
    context      = context or {}
    correlations = correlation_cfg.get("correlations", [])
    decisions    = []

    for rule in correlations:
        rule_type = rule.get("type")
        rule_id   = rule.get("id")

        # ── INHIBITION: checked at emit time, not here
        if rule_type == "inhibition":
            continue

        # ── ESCALATION: side-effect only (log/notify), no decision emitted
        if rule_type == "escalation":
            _eval_escalation(rule, reports, thresholds, context)
            continue

        # ── COMPOUND
        if rule_type == "compound":
            passed, rule = _eval_compound(rule, reports, thresholds, context)
            if not passed:
                continue

        # ── COMPOSITE
        elif rule_type == "composite":
            passed, rule = _eval_composite(rule, reports, thresholds, context)
            if not passed:
                continue

        else:
            print(f"[WARN] unknown correlation type '{rule_type}' in rule '{rule_id}' — skipping")
            continue

        # ── EMIT one decision per allowed responder
        for responder in rule.get("allowed_responders", []):
            if _is_inhibited(reports, thresholds, correlations, responder):
                continue

            decision = {
                "action":         responder,
                "target":         None,
                "severity":       rule.get("severity", "high"),
                "correlation_id": rule_id,
                "source":         "correlation_engine",
                "timestamp":      datetime.utcnow().isoformat(),
            }
            decisions.append(decision)
            print(f"[CORRELATION] '{rule_id}' → '{responder}' (severity: {rule.get('severity')})")

    return decisions