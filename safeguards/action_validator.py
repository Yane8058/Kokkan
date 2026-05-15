"""
Action Validator
Check if an action can be executed.
"""

from safeguards.rate_limiter import is_allowed


def validate_action(decision, actions_cfg):
    action = decision.get("action")
    target = decision.get("target")

    if not action:
        return False, "missing_action"

    cfg = actions_cfg.get(action)

    if not cfg:
        return False, "undefined_action"

    if not cfg.get("enabled", False):
        return False, "disabled"

    # ---- TARGET CHECK ----
    allowed_targets = cfg.get("targets")

    if allowed_targets and target not in allowed_targets:
        return False, "target_not_allowed"

    # ---- RATE LIMIT ----
    cooldown = cfg.get("rate_limit", 0)

    if cooldown > 0:
        if not is_allowed(action, target, cooldown):
            return False, "rate_limited"

    return True, "allowed"
``
