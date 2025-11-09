---
applyTo: "utils/**"
---

Util modules provide concise utility functions and helpers enhancing framework capabilities
- Purpose – deliver reusable helpers that extend the framework without embedding project-specific logic and support managers/plugins/MCPs/project's code with shared capabilities. e.g. math utilities, data transformations, common I/O operations, etc.
- Placement – store packages under `utils/<name>`, import via `utils.<name>`, and keep them decoupled from module-specific dependencies so they stay broadly reusable.
- Conventions – maintain minimal state, design concise typed APIs.