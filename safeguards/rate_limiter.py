import time

_last_exec = {}

def is_allowed(action, target, cooldown):
    key = f"{action}:{target}"

    now = time.time()
    last = _last_exec.get(key, 0)

    if now - last < cooldown:
        return False

    _last_exec[key] = now
    return True
