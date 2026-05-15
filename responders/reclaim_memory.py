import subprocess


def reclaim_memory():
    try:
        subprocess.run(["sync"], check=True)

        subprocess.run(
            ["bash", "-c", "echo 3 > /proc/sys/vm/drop_caches"],
            check=True
        )

        print("[OK] memory caches cleared")

    except Exception as e:
        raise RuntimeError(f"memory reclaim failed: {e}")
