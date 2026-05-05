```
Kokkan/
├── README.md
├── LICENSE
│
├── docs/
│   ├── architecture.md
│
├── config/
│   ├── global.yaml
│   ├── thresholds.yaml
│   └── actions.yaml
│
├── detectors/
│   ├── disk_usage.py
│   ├── service_health.py
│   ├── memory_pressure.py
│   ├── cpu_spike.py
│   └── network_latency.py
│
├── responders/
│   ├── cleanup_disk.py
│   ├── restart_service.py
│   ├── rotate_logs.py
│   ├── reclaim_memory.py
│   └── throttle_process.py
│
├── safeguards/
│   ├── rate_limiter.py
│   ├── dry_run.py
│   ├── rollback.py
│   └── action_validator.py
│
├── engine/
│   ├── healer.py
│   ├── decision_engine.py
│   ├── context_builder.py
│   └── audit_logger.py
│
├── runbooks/
│   ├── disk_full.md
│   ├── service_down.md
│   ├── high_memory.md
│   └── cpu_spike.md
│
├── reports/
│   └── example-incident-report.json
│
├── systemd/
│   ├── self-healing-ops.service
│   └── self-healing-ops.timer
│
├── scripts/
│   ├── install.sh
│   └── uninstall.sh
│
├── tests/
│   ├── test_detectors.py
│   ├── test_responders.py
│   └── test_safeguards.py


```
