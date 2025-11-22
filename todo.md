# ADHD Framework Todo List

## 1. Prompt Management System
- [ ] **Update `instruction_core` to handle Prompts**
    - **Goal**: Create a `prompts/` folder in `cores/instruction_core/data/` and update `InstructionController` to sync these files to `.github/prompts/`.
    - **Context**: GitHub now supports `.github/prompts/` for reusable prompts (e.g., for Copilot Workspace or custom agent workflows).
    - **Implementation**:
        - Add `cores/instruction_core/data/prompts/`.
        - Update `InstructionController.sync_core_data()` to copy from `data/prompts` to `.github/prompts`.
        - Update `InstructionController.sync_module_instructions()` (or create a new method) to look for `*.prompt.md` in modules and sync them too.

## 2. Create Standard Prompts
- [ ] **Author useful prompt files for ADHD**
    - **Goal**: Provide reusable prompts that help agents/users work effectively with the framework.
    - **Suggestions**:
        - `architect.prompt.md`: "Act as a System Architect. Review the proposed changes against the ADHD Framework's modular architecture..."
        - `refactor.prompt.md`: "Refactor this code. Ensure strict adherence to `logger_util` and `ADHDError` patterns..."
        - `security_audit.prompt.md`: "Scan this module for common security pitfalls (hardcoded secrets, unvalidated paths)..."
        - `new_module.prompt.md`: "Generate a new module structure following the `init.yaml` and `README.md` standards..."

## 3. Remote Module Listing (Low Priority)
- [ ] **Implement Remote Module Discovery**
    - **Goal**: Allow `adhd_framework.py list` (or a new command) to show modules available in remote registries, not just locally installed ones.
    - **Context**: Legacy Genesis had `listing.py` which fetched `listing_public.yaml`.
    - **Suggestions**:
        - Create `cores/module_listing_core`.
        - Define a schema for `listing.yaml` (e.g., `module_name: repo_url`).
        - Add `adhd_framework.py search <query>` or `list --remote`.

## 4. Testing Strategy
- [ ] **Establish Testing Infrastructure**
    - **Goal**: Ensure stability of the self-bootstrapping framework.
    - **Suggestions**:
        - **Framework**: Use `pytest`.
        - **Structure**: Create a `tests/` directory at the root.
        - **CI/CD**: Add a GitHub Action to run tests on PRs.
        - **Key Tests**:
            - `test_bootstrap.py`: Verify `adhd_framework.py` can clone missing cores.
            - `test_project_init.py`: Verify a new project is created with correct structure.
            - `test_modules_controller.py`: Verify it correctly parses `init.yaml` and detects issues.
