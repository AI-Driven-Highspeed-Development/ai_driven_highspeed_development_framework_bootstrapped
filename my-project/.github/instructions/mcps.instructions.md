---
applyTo: "mcps/**"
---

MCP modules implement Model Context Protocol servers/adapters.
- Purpose – expose protocol-compliant surfaces for external tools without leaking framework internals.
- Placement – implement under `mcps/<name>`; import via `mcps.<name>`; keep protocol handlers separate from shared utilities.

Additional guidance:
- Maintain strict isolation between protocol messages and framework internals; define clear request/response schemas.
- Include lightweight self-check endpoint/routine to validate server health when appropriate.
- When testing MCP connectivity, call the MCP server endpoint as an AI agent's tool with suitable test parameters.