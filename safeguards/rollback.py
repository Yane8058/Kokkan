"""
Rollback handler
Hadling specific rollback when possible.
"""

def rollback(decision):
    action = decision.get("action")
    target = decision.get("target")

    print(f"[ROLLBACK] attempting rollback for {action} → {target}")

    # ---- SERVICE ----
    if action == "restart_service":
        # rollback unsecure  → log only
        print("[ROLLBACK] restart_service: no safe rollback available")

    # ---- DISK ----
    elif action == "cleanup_disk":
        print("[ROLLBACK] cleanup_disk: irreversible action")

    # ---- MEMORY ----
    elif action == "cleanup_memory":
        print("[ROLLBACK] reclaim_memory: no rollback needed")

    # ---- LOG ROTATION ----
    elif action == "rotate_logs":
        print("[ROLLBACK] rotate_logs: partial rollback possible")

    # ---- CPU ----
    elif action == "throttle_cpu":
        print("[ROLLBACK] restoring default priority")

        try:
            import os
            os.setpriority(os.PRIO_PROCESS, target, 0)
            print("[ROLLBACK] priority restored")

        except Exception as e:
            print(f"[ROLLBACK ERROR] {e}")

    # ---- DEFAULT ----
    else:
        print(f"[ROLLBACK] no handler for action: {action}")
