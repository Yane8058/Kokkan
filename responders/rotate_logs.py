import os


def rotate_logs(log_dir="/var/log", max_size_mb=100):
    try:
        for filename in os.listdir(log_dir):
            path = os.path.join(log_dir, filename)

            if not os.path.isfile(path):
                continue

            size_mb = os.path.getsize(path) / (1024 * 1024)

            if size_mb > max_size_mb:
                new_path = f"{path}.old"
                os.rename(path, new_path)

                # ricrea file vuoto
                open(path, "w").close()

                print(f"[OK] rotated log: {filename}")

    except Exception as e:
        raise RuntimeError(f"log rotation failed: {e}")
