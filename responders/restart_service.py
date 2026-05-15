import subprocess


def restart_service(service_name):
    try:
        subprocess.run(
            ["systemctl", "restart", service_name],
            check=True
        )
        print(f"[OK] restarted service: {service_name}")

    except Exception as e:
        raise RuntimeError(f"failed to restart {service_name}: {e}")
