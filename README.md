# Kokkan

**Kokkan** is a safety‑first operational decision layer for production systems.

<p align="left">
  <img src="asset/logo.png" width="350" height="350" alt="Kokkan Logo">
</p>

It observes system conditions, evaluates them against explicit policies,  
and **decides whether a bounded, conservative remediation is allowed**.

Kokkan is **not** a monitoring system, not an orchestration platform,  
and not a fully autonomous self‑healing engine.

Its primary goal is **reducing unnecessary human intervention**  
*without increasing operational risk*.

---

## Design Principles

Kokkan is built around a few strict principles:

- **Policy before action**  
  All limits, thresholds and permissions are defined outside the code.

- **Safety over automation**  
  Acting is always optional. Doing nothing is often the safest outcome.

- **Separation of responsibilities**  
  Observation, decision, enforcement and execution are isolated concerns.

- **Human‑in‑the‑loop by design**  
  Kokkan supports operators. It does not replace them.

- **Auditability and transparency**  
  Every decision and action can be explained after the fact.

---

## What Kokkan Is (and Is Not)

### ✅ Kokkan *is*
- A policy‑driven decision engine for operational remediation
- A framework for **controlled self‑healing**
- A tool for reducing repetitive, low‑risk operational work
- Designed for real production environments

### ❌ Kokkan *is not*
- A monitoring or alerting system  
- A replacement for Prometheus or Alertmanager
- A generic automation or orchestration platform
- A zero‑touch autonomous remediation system

---

## Repository Structure

```
Kokkan/
├── README.md
├── LICENSE
├── .env.example
├── .gitignore
├── requirement.txt
│
├── ansible/
│   ├── ansible.cfg
│   ├── hosts.yml
│   │
│   ├── group_vars/
│   │   ├── all.yml
│   │   ├── docker.yml
│   │   └── python.yml
│   │
│   ├── playbooks/
│   │   └── deploy.yml
│   │
│   └── roles/
│       ├── common/
│       │   └── tasks/
│       │       └── main.yml
│       ├── docker/
│       │   └── tasks/
│       │       └── main.yml
│       └── kokkan/
│           ├── tasks/
│           │   └── main.yml
│           └── handlers/
│               └── main.yml
│
├── asset/
│   ├── logo.png
│   └── Kokkan_flowchart.png
│
├── config/
│   ├── global.yaml
│   ├── thresholds.yaml
│   ├── correlation.yaml
│   ├── loki_config.yaml
│   ├── promtail.yaml
│   └── actions.yaml
│
├── detectors/
│   ├── disk_usage.py
│   ├── service_health.py
│   ├── memory_pressure.py
│   ├── cpu_spike.py
│   └── network_latency.py
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose-OBS.yaml
│   └── .dockerignore
│
├── docs/
│   └── architecture.md
│
├── engine/
│   ├── healer.py
│   ├── decision_engine.py
│   ├── context_builder.py
│   └── audit_logger.py
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
├── scripts/
│   ├── install.sh
│   └── uninstall.sh
│
└── systemd/
    ├── loki.service
    ├── promtail.service
    ├── kokkan.service
    └── kokkan.timer

```
---

## License

MIT License — open source, use freely.
