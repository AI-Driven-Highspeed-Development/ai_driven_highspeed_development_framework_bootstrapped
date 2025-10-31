# ADHD Framework Agent Instructions (Concise)

## Project overview
- Directories: `framework/` (core), `project/` (app code), `managers/`, `utils/`, `plugins/`, `mcps/` (4 types of modules)
- Entry points: `adhd_cli.py` (framework CLI), `app.py` (application for the specific project)
- Module files: `__init__.py`, `init.yaml`, optional `.config_template` (JSON), optional `refresh.py`
- Module types: `manager`, `plugin`, `util`, `mcp`

## Agent response lifecycle (always use these headings)
1) Initial
- Read Instructions; if a module is targeted, read its instructions
- Context Analysis: request type + relevant context (active file, workspace, OS)
- Goal Alignment (DO NOT assume user is always right):
  - Does request make sense? continue vs clarify
  - Better approach? propose alternatives; challenge assumptions politely
  - Need clarification? ask up to 3 targeted questions if needed (scope, paths, module type, acceptance criteria)
  - Safety check (API leakage, security, permissions); then Decision: Proceed / Ask / Suggest Alternative

2) Planning
- Suggest Plan: concise steps
- Workspace Awareness: verify target paths and module placement
- Read Source Code as needed

3) Implementation
- Generate Code / Answer Question
- Optional: tests/debug/docs/demo if enabled
- Small, low‑risk adjacent improvements allowed
- No major changes or rewrites without explicit permission

4) Finishing
- Recap: what changed and why
- Suggestions: next steps
- Traceback to Decision (from Initial)

## Clarifying triggers (ask before proceeding when unclear)
- Target file/module path, module type, naming
- External credentials/config expectations
- Acceptance criteria, performance, or test coverage

## Key workflows (general across ADHD projects)
- Project ops via `adhd_cli.py` (init/refresh/upgrade/install); use `--help` to discover commands
- Modules live under `managers/`, `plugins/`, `utils/`, `mcps/`; import via package paths under `project/`

## Agent defaults
- OOP; minimal docstrings, always include type hints
- No rapid prototyping; legacy compatibility off
- Auto Demo/Testing/Debugging/Documentation off