# Kokkan

**Kokkan** is a safety‑first operational decision layer for production systems.

<p align="left">
  <img src="asset/Designer.png" width="350" height="350" alt="Kokkan Logo">
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

## High‑Level Architecture

At a high level, Kokkan follows this flow:

```
Observation (detectors)
↓
Context & Correlation (engine)
↓
Policy Evaluation (config + safeguards)
↓
Optional Remediation (responders)
↓
Audit & Reporting
```

Policies define **what is allowed**.  
- Safeguards ensure **it is not abused**.  
- The engine decides **if acting makes sense at all**.

---

## Repository Structure

```
Kokkan/
├── README.md
├── LICENSE
├── .env-example
├── .gitignore
├── requirement.txt
│
├── asset/
|   ├── logo.png
|   └── Kokkan_flowchart.png
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
│
├── systemd/
│   ├── kokkan.service
│   └── kokkan.timer
│
├── scripts/
│   ├── install.sh
│   └── uninstall.sh

```

---

## Configuration Model

Kokkan configuration is **purely declarative** and stored in YAML.

- `global.yaml`  
  Runtime behavior and environment flags (e.g. dry‑run, audit).

- `thresholds.yaml`  
  Defines **when a condition becomes meaningful**.

- `actions.yaml`  
  Defines **which actions are allowed**, and within which limits.

YAML files act as **structured dictionaries**, not as a DSL or scripting language.  
All logic remains in the codebase.

---

## Detectors

Detectors observe system state and emit **neutral signals**.

They:
- do not read configuration files
- do not make decisions
- do not trigger actions

Examples:
- Disk usage pressure
- Service health degradation
- Memory pressure
- CPU spikes
- Network latency

A detector answers only one question:
> *“What do I observe right now?”*

---

## Decision Engine

The decision engine:
- builds contextual understanding
- correlates signals over time
- evaluates policies
- decides **whether an action is justified**

Importantly:
- it may decide **not to act**
- it never bypasses safeguards

---

## Safeguards

Safeguards enforce **hard safety boundaries**, regardless of decisions.

They include:
- rate limiting
- dry‑run enforcement
- action validation
- rollback protection

Safeguards are policy‑driven but **implemented in code**,  
ensuring enforcement even in edge cases.

---

## Responders

Responders perform **bounded remediation actions**, such as:
- disk cleanup
- service restart
- log rotation
- memory reclamation
- process throttling

Responders:
- never decide *when* to run
- never bypass safeguards
- must be auditable and reversible when possible

---

## Runbooks and Reports

Kokkan keeps humans in the loop.

- **Runbooks** document expected failure scenarios and responses.
- **Reports** provide structured, post‑incident visibility.

Automation without explanation is considered incomplete.

---

## Operational Model

Kokkan is typically deployed as a scheduled or event‑driven service,
often alongside existing monitoring systems.

A common pattern is:
- Monitoring detects anomalies
- Kokkan evaluates whether safe remediation is permitted
- Operators remain informed and in control

---

## Status

Kokkan is a **professional‑grade internal operations tool**.

It is designed to be:
- understandable
- extensible
- safe by default

It intentionally avoids premature complexity and product‑level abstractions.

---

## License

See the `LICENSE` file for details.
