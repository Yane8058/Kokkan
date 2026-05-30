## Configuration Model

Kokkan configuration is **purely declarative** and stored in YAML.

- `global.yaml`  
  Runtime behavior and environment flags (e.g. dry‑run, audit).

- `thresholds.yaml`  
  Defines **when a condition becomes meaningful**.

- `actions.yaml`  
  Defines **which actions are allowed**, and within which limits.

- `correlation.yaml`  
  Defines **the correlation between the threshold**.

- `loki_config.yaml`
  Defines **Loki aggregation policies**.

- `promtail.yaml`
  Defines **promtail log exportation policies**.

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