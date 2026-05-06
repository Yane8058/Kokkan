# Architecture

Kokkan is a **policy‑driven operational decision layer** designed to enable  
**safe, bounded remediation** in production environments.

It does not replace monitoring systems, nor does it act as a general automation platform.  
Instead, it introduces a controlled decision boundary between observation and action.

---

## Core Architecture

Kokkan is structured as a pipeline of clearly separated components:

> Detectors → Context → Decision Engine → Safeguards → Responders → Audit

Each layer has a single responsibility and must not bleed into others.

flowchart TD

    A[Start Cycle] --> B[Run Detectors]

    B --> C[Build Context]

    C --> D[Evaluate Decision]

    D -->|No action needed| E[Log Decision]
    E --> Z[End Cycle]

    D -->|Action candidate| F[Load Action Policy]

    F --> G[Validate Action]

    G -->|Invalid| H[Reject + Log]
    H --> Z

    G -->|Valid| I[Apply Safeguards]

    I -->|Blocked| J[Blocked by Safeguards + Log]
    J --> Z

    I -->|Allowed| K[Execute Responder]

    K --> L[Record Action]

    L --> Z[End Cycle]


> Note: Most cycles end without executing any action.
> This is intentional and aligned with Kokkan’s safety-first design.

---

## Component Breakdown

### 1. Detectors (`detectors/`)

Detectors are responsible for **observing system state**  
and emitting **neutral, structured signals**.

They must:
- be stateless (or externally managed state)
- not read configuration files
- not trigger actions
- not infer intent

A detector answers only:
> *What is currently happening in the system?*

Examples:
- disk usage pressure
- service availability
- memory pressure
- CPU spikes
- network latency

Output is always structured, machine‑readable data.

---

### 2. Context Builder (`engine/context_builder.py`)

The context builder enriches raw detector signals with  
**temporal and situational awareness**.

It may:
- preserve previous states
- compute duration of conditions
- correlate repeated signals
- reduce transient noise

This layer transforms:

> **event → situation**

No actions are taken at this stage.

---

### 3. Decision Engine (`engine/decision_engine.py`)

The decision engine evaluates whether **any action is justified**.

It:
- consumes detector signals + context
- evaluates against policy (config)
- determines if action is:
  - unnecessary
  - unsafe
  - or allowed

Important constraints:
- deciding *not to act* is a valid outcome
- decisions are deterministic and explainable
- no safeguard is bypassed

This is the **core reasoning layer** of Kokkan.

---

### 4. Safeguards (`safeguards/`)

Safeguards enforce **hard operational limits**.

They operate independently from the decision engine  
and act as a final control barrier before execution.

Examples:
- rate limiting
- dry‑run enforcement
- action validation
- rollback protection

Safeguards:
- read policy from config
- enforce it in code
- cannot be overridden by decisions

They answer:
> *Even if allowed in theory, is it safe to act now?*

---

### 5. Responders (`responders/`)

Responders perform **bounded remediation actions**.

They:
- execute only when allowed
- receive fully validated inputs
- do not contain policy logic
- do not decide when to run

Examples:
- cleanup disk
- restart a service
- rotate logs
- reclaim memory
- throttle processes

A responder answers:
> *How is the action executed?*

---

### 6. Audit Logger (`engine/audit_logger.py`)

All decisions and actions are recorded.

Audit logs must include:
- detected condition
- decision outcome
- applied safeguards
- executed action (if any)
- timestamp

This ensures:
- traceability
- post‑incident analysis
- accountability

---

## Configuration Model

All policies are defined in `config/` as YAML files.

### `global.yaml`
Defines runtime behavior:
- environment
- dry‑run mode
- audit configuration

### `thresholds.yaml`
Defines **when a condition becomes relevant**.

Example:
- disk usage percentage
- memory pressure level
- duration thresholds

### `actions.yaml`
Defines **what actions are allowed and how they are constrained**.

Example:
- enabled / disabled actions
- rate limits
- scope restrictions

---

## Design Rules

### 1. Policy is external

No policy is hardcoded.  
All limits and permissions must come from configuration.

---

### 2. Detectors are pure

Detectors:
- observe only
- do not decide
- do not act
- do not read configuration

---

### 3. Decisions are explicit

The decision engine:
- does not hide logic in data
- does not infer ambiguous rules
- produces explainable outcomes

---

### 4. Safeguards are authoritative

Safeguards:
- enforce hard boundaries
- operate regardless of intent
- cannot be bypassed

---

### 5. Actions are bounded

Responders:
- do not exceed defined limits
- do not escalate scope
- are safe by default

---

### 6. Inaction is acceptable

Kokkan does not optimize for action.  
It optimizes for **correctness under uncertainty**.

---

## Execution Model

Kokkan is typically executed as a scheduled process (e.g. via systemd timer).

At each iteration:

1. Detectors collect signals
2. Context is built or updated
3. Decision engine evaluates signals
4. Safeguards enforce limits
5. Responders may execute actions
6. Results are logged and reported

This cycle is **idempotent and repeatable**.

---

## Relationship with Monitoring

Kokkan is not a monitoring system.

It is designed to operate alongside tools such as:
- Prometheus
- Alertmanager
- system metrics collectors

Monitoring detects anomalies.  
Kokkan evaluates whether **safe remediation is justified**.

---

## Failure Model

Kokkan assumes:
- incomplete information
- transient anomalies
- partial observability

Therefore:
- actions are conservative
- safeguards are strict
- decisions favor stability over intervention

---

## Summary

Kokkan is designed as a **controlled boundary between detection and action**.

Its value lies not in automation itself, but in:
- **deciding when not to automate**
- **enforcing safety under uncertainty**
- **making remediation predictable and auditable**

It is intentionally:
- minimal in scope
- explicit in behavior
- conservative by design
