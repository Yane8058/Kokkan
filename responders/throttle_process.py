import os

def throttle_process(pid, nice_value=10):
    try:
        os.setpriority(os.PRIO_PROCESS, pid, nice_value)

        print(f"[OK] throttled PID {pid} (nice={nice_value})")

    except Exception as e:
        raise RuntimeError(f"throttling failed for PID {pid}: {e}")
