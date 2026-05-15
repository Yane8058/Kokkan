"""
Dry run handler
"""

def handle(decision, dry_run, executor):
    if dry_run:
        print(f"[DRY-RUN] {decision}")
        return

    return executor(decision)
