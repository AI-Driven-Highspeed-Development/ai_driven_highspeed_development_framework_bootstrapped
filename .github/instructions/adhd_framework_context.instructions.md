# ADHD Framework Context

## Core Philosophy
1.  **Read Before Write**: NEVER guess. Read relevant docs and source code first.
2.  **Reuse, Don't Reinvent**: ALWAYS check for existing modules (`cores/`, `managers/`, `utils/`, `plugins/`, `mcps/`) before implement functionalities or logics.
3.  **Consistency**: MIMIC existing style, error handling, and structure exactly.

## Project Structure
-   **Directories**:
    -   `framework/`: Legacy core (DO NOT touch/call).
    -   `project/`: App-specific code.
    -   `project/data/`: App data storage (use Config-Manager paths).
    -   `cores/`, `managers/`, `utils/`, `plugins/`, `mcps/`: Modules of different types.
    -   `.temp_test/`, `.temp_debug/`: Temporary folders for testing/debugging.
    -   `.temp_agent_work/`: Temporary workspace for agents, you can write temporary code here during operations, MUST clean up after.
-   **Entry Points**:
    -   `adhd_cli.py`: Framework CLI (init/refresh/upgrade/install). Use `--help`.
    -   `<app_name>.py`: App entry point. (Name can vary by project).
-   **Module Assets**:
    Modules are in `<module_type>/<module_name>/` folders, containing:
    -   `__init__.py`: Init code.
    -   `init.yaml`: Metadata, read guidance in `.github/instructions/modules.init.yaml.instructions.md` for structure.
    -   `.config_template` (JSON): Default config schema.
    -   `data/`: Optional, module-specific data files.
    -   `refresh.py`: Optional, idempotent state regeneration (only when module manages data/state benefiting from regeneration).
    -   `<module_name>.instructions.md`: Module-specific AI instructions.
    -   `requirements.txt`: PyPI deps only (no ADHD module deps). NOTE: Don't put PyPI deps into init.yaml.
-   **Project Data Storage**: Use Config-Manager paths (Convention: `./project/data/<module_name>/**`).

## Module Types
-   **Core**: Fundamental building blocks (e.g., instruction_core, modules_controller_core).
-   **Manager**: High-level orchestrators, coordinating project-wide or external system interactions (e.g., config_manager, temp_files_manager).
-   **Util**: Reusable tiny tools or helpers (e.g., logger_util).
-   **Plugin**: Specific feature for projects (e.g., webcam_plugin, comfy_image_gen_plugin)
-   **MCP**: Model Context Protocol servers, facilitating LLM context management and retrieval. (adhd_mcp)
