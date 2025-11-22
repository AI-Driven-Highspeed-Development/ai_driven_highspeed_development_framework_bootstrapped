---
applyTo: "managers/**/*.instructions.md,plugins/**/*.instructions.md,utils/**/*.instructions.md,mcps/**/*.instructions.md,cores/**/*.instructions.md"
---

# Module Instructions Authoring Guidelines

## Goals
- Provide AI agents with high-density, low-noise context about a module.
- Standardize how modules expose their usage patterns and constraints to the AI.
- Ensure every module has a corresponding `<module_name>.instructions.md` file.

## Required section order
Each instruction file MUST include sections in this exact order:
1) **Frontmatter** — YAML block defining the file scope (`applyTo`).
2) **Header** — `<Module Name>:` (e.g., `Config Manager:`).
3) **Purpose** — One or two sentences describing the module's role.
4) **Usage** — Code blocks showing correct import and usage patterns.
5) **Key Concepts/Rules** — Bullet points on configuration, singletons, specific behaviors, or constraints.

## Tone and style
- **Target Audience**: AI Agents (not humans). Be extremely concise.
- **Format**: Use bullet points and code blocks primarily.
- **Imports**: ALWAYS use full absolute imports in examples (e.g., `from managers.config_manager import ConfigManager`).
- **No Fluff**: Avoid "This module is designed to...", just say "Handles X".

## Frontmatter Rules
- The `applyTo` field is mandatory.
- It should target the Python files where this module might be used.
- **Scope**: If the module is used globally, target all module types. If it's a helper for specific modules, scope it tightly.
- **File Types**: Target `.py` files specifically. Avoid targeting non-code files (like `managers/**`).
- **Root Files**: Include `*.py` to cover entry points like `adhd_framework.py`.
- Standard pattern (Global): `applyTo: "project/**/*.py,managers/**/*.py,plugins/**/*.py,utils/**/*.py,mcps/**/*.py,cores/**/*.py,*.py"`
- Standard pattern (Module-specific): `applyTo: "managers/specific_manager/**/*.py"`
- Note: Adjust paths based on actual needs of the specific module, askuser if unsure.

## Template
Copy and adapt this template for any module instruction file.

````markdown
---
applyTo: "project/**/*.py,managers/**/*.py,plugins/**/*.py,utils/**/*.py,mcps/**/*.py,cores/**/*.py,*.py"
---

<Module Name>:
- Purpose: <Concise description of what the module does>.
- Usage:
```python
from <package_import_path> import <MainClass>

# <Comment explaining the pattern>
obj = <MainClass>(...)
obj.do_work(...)
```
- <Key Concept 1>: <Explanation>
- <Key Concept 2>: <Explanation>
````

## Validation checklist
- Frontmatter is present and valid YAML.
- Header ends with a colon (`:`).
- Usage examples use correct, absolute imports.
- Content is concise and devoid of conversational filler.

## Maintenance
- Update the instruction file when public APIs change.
- Ensure usage examples remain valid after refactors.
