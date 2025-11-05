---
applyTo: "cores/**/README.md, managers/**/README.md, plugins/**/README.md, utils/**/README.md, mcps/**/README.md"
---

# Modules README Authoring Instructions

## Goals
- Keep READMEs short, skimmable, and useful to users of the module.
- Use consistent sections and tone across all modules.
- Provide a working Quickstart and minimal API reference.
- Cross-link related modules to help discovery.

## Required section order
Each README MUST include sections in this exact order (omit a section only if truly not applicable):
1) Title — `# <Human-friendly Module Name>` with a one-sentence intro below it
2) Overview — 3–5 concise bullets on purpose and usage
3) Features — bulleted key capabilities
4) Quickstart — one or two code snippets showing the happy path
5) API — minimal surface outline of public classes and main methods
6) Notes (optional) — implementation or behavioral caveats
7) Requirements & prerequisites — external packages only
8) Troubleshooting — 3–6 common issues with fixes
9) Module structure — short tree of files with one-line comments
10) See also — 2–4 related modules

## Tone and style
- Single-sentence intro under the title starting with a succinct phrase (e.g., “Small,” “Lightweight,” etc.).
- Short sentences, concrete language; minimize buzzwords.
- Present tense.
- Prefer code over prose where helpful.

## Import rules for examples
- Cores: prefer `from cores.<module_name> import <ExportedClass>` if `__init__.py` exports it; otherwise import from the implementation file (e.g., `from cores.<module_name>.<file> import Class`).
- Managers: prefer `from managers.<module_name> import Class` if exported; otherwise `from managers.<module_name>.<module_name> import Class`.
- Utils: same rule; prefer top-level exports if present.
- Mcps/Plugins: follow the package’s export; if none, import the primary class/function from its implementation file.

When in doubt, check `__init__.py` for `__all__` or explicit exports. Avoid star imports.

## Requirements guidance
- Module-level `requirements.txt` MUST list only dependencies specific to that module.
- No version pins unless a strict version is required to avoid known breakage.
- Root-level `requirements.txt` may include shared deps used across modules.

## Cross-linking
- In “See also”, reference sibling modules by human name (e.g., “YAML Reading Core”, “Temp Files Manager”, “GitHub API Core”).
- Use file links only when it clarifies navigation; plain names are fine within the repo.

## Template
Copy and adapt this template for any module README.

``````markdown
# <Module Name>

<one-line description>.

## Overview
- <What it is>
- <When to use>
- <Key behavior>

## Features
- <Feature 1>
- <Feature 2>

## Quickstart
```python
from <package_import_path> import <MainClass>

obj = <MainClass>(...)
obj.do_work(...)
```

## API
```python
class <MainClass>:
	def __init__(...): ...
	def do_work(self, arg: Type) -> Return: ...
```

Notes
- <Optional note>

## Requirements & prerequisites
- <dependency-one>

## Troubleshooting
- <Issue>: <Fix>

## Module structure
```
<folder_name>/
├─ __init__.py          # exports
├─ <file>.py            # main implementation
└─ README.md            # this file
```

## See also
- <Related A>
- <Related B>
``````

## Validation checklist (for PRs and agents)
- Title + one-line intro present and concise.
- Sections follow the required order.
- Quickstart imports are correct and runnable.
- API section reflects current public surface.
- Requirements match module `requirements.txt`; no version pins unless necessary.
- Module structure matches actual files.
- “See also” lists 2–4 relevant modules.

## Maintenance
- Update the README when public APIs change or when adding/removing key features if auto update is enabled.
- Keep examples aligned with exported import paths; adjust `__init__.py` exports where it improves DX.
- Keep cross-links fresh when modules are added/renamed.
