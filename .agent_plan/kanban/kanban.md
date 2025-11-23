# ADHD Framework Kanban Board

## Backlog

### Prompt Management System

  - due: 2025-12-31
  - tags: [core, prompts]
  - priority: high
  - defaultExpanded: true
  - steps:
      - [ ] Add `cores/instruction_core/data/prompts/`
      - [ ] Sync core prompts to `.github/prompts/`
      - [ ] Decide on module-level prompt syncing
    ```md
    Create a `prompts/` folder under `cores/instruction_core/data/` and update `InstructionController` to sync prompt files into `.github/prompts/`.
    ```

### Create Standard Prompts

  - tags: [prompts, ergonomics]
  - priority: medium
  - steps:
      - [ ] Draft `architect.prompt.md`
      - [ ] Draft `refactor.prompt.md`
      - [ ] Draft `security_audit.prompt.md`
      - [ ] Draft `new_module.prompt.md`
    ```md
    Author reusable prompt files that help agents and users work effectively with the ADHD Framework (architect, refactor, security audit, new module).
    ```

### Remote Module Listing

  - tags: [modules, discovery, low-priority]
  - priority: low
    ```md
    Implement Remote Module Discovery so `adhd_framework.py` can list modules from remote registries (using a `listing.yaml` schema and CLI commands like `list --remote` or `search`).
    ```

### Testing Strategy

  - tags: [testing, ci]
  - priority: high
  - defaultExpanded: true
  - steps:
      - [ ] Choose pytest layout
      - [ ] Create `tests/` tree
      - [ ] Add bootstrap tests
      - [ ] Add project init tests
      - [ ] Add modules controller tests
    ```md
    Establish a pytest-based testing infrastructure with a `tests/` directory and CI (GitHub Actions) covering bootstrap, project initialization, and module controller behavior.
    ```

### Ignore Manager

  - tags: [manager, gitignore]
  - priority: medium
    ```md
    Implement `ignore_manager` to programmatically ensure required patterns are present in `.gitignore` (and optionally `.dockerignore`) using an idempotent API like `IgnoreManager.ensure_ignored`.
    ```

### Secrets Manager

  - tags: [manager, secrets]
  - priority: medium
    ```md
    Implement `secrets_manager` (formerly `api_key_manager`) to manage API keys and secrets via `.env` and optional `secrets.yaml`, ensuring these files are always ignored using `ignore_manager`.
    ```

## In Progress

## Done

### HyperAgentSmith Agent

  - tags: [agents, tooling]
  - priority: medium
    ```md
    Create the `HyperAgentSmith` Agent Creator that interactively defines new agents, generates `*.agent.md` files in the correct locations, and validates them against framework standards.
    ```

### HyperPM Agent

  - tags: [agents, planning]
  - priority: medium
    ```md
    Create the `HyperPM` Project Manager agent that generates and manages advanced todo/kanban boards (for example `.agent_plan/kanban/kanban.md`) and parses `todo.md` to visualize progress.
    ```

