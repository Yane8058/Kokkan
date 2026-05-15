import os
import shutil


def cleanup_disk(path="/tmp"):
    try:
        if not os.path.exists(path):
            raise RuntimeError(f"path not found: {path}")

        removed = 0

        for filename in os.listdir(path):
            full_path = os.path.join(path, filename)

            try:
                if os.path.isfile(full_path) or os.path.islink(full_path):
                    os.remove(full_path)
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)

                removed += 1

            except Exception:
                continue

        print(f"[OK] cleaned {removed} items in {path}")

    except Exception as e:
        raise RuntimeError(f"cleanup failed: {e}")
