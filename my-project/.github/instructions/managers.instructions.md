---
applyTo: "managers/**"
---

Managers modules coordinate external/project-wide internal services and shared resources.
- Purpose - integrate external systems (e.g. database, APIs) or internal services (e.g. specific centralized management for all modules), so siblings can stay focused on their core logic.
- Placement – implement under `managers/<name>`, expose via `managers.<name>`.