---
applyTo: "managers/**,plugins/**,utils/**,mcps/**"
---

Shared module guidance (all module types).

Module assets:
- `__init__.py` – initialization code on import.
- `init.yaml` – metadata (name, version, dependencies); see `managers/config_manager/init.yaml` for reference.
- Optional `.config_template` (JSON) – default config schema Config-Manager materializes into `.config`.
- Optional `refresh.py` – idempotent refresh/update invoked by `python adhd_cli.py refresh`.
- Optional `<module_name>.instructions.md` – module-specific AI agent instructions auto-cloned to `.github/instructions/`.

Entry points:
- Expose focused APIs via standalone modules (e.g., `[module_name].py`) or small packages importable by other modules or `app.py`.
- Keep executable logic behind function/class boundaries; no workflow execution on import.
- Avoid import-time side effects (network calls, file I/O, heavy computation).

Refresh routines:
- Include `refresh.py` only when module manages data/state benefiting from regeneration.
- Ensure refresh logic is rerun-safe and validates prerequisites before mutating state.

Module requirements:
- Declare required ADHD modules in `<module_type>/<module_name>/init.yaml` under `requirements`.
- Prompt users to manually add undeclared dependencies to avoid runtime import errors (pending automated dependency management).

Module data storage:
- Use Config-Manager path settings; no hardcoded paths. Convention: `./project/data/<module_name>/**`.