# ADHD Framework Migration Report

This report compares the functionality of the legacy "Genesis" project (`~/PublicRepo/ADHD-Framework/AI-Driven-Highspeed-Development-Framework/`) with the new Bootstrapped Framework (`.`).

## 1. Migration Scope

The Legacy Genesis project was a standalone CLI tool used to create ADHD projects. It was **not** an ADHD project itself.
The New Bootstrapped Framework is a self-hosting ADHD project that contains the core logic to create and manage other projects (and itself).

## 2. Missing Functionality (From Legacy Genesis)

The following features existed in the Legacy Genesis CLI but are currently missing in the new system:

### A. Remote Module Listing
- **Legacy (`framework/listing.py`)**: Fetched and displayed available modules from `listing_public.yaml` and `listing_private.yaml` (remote repositories).
- **New System**: `adhd_framework.py list` only lists **locally installed** modules via `cores/modules_controller_core`.
- **Status**: 🔴 Unimplemented
- **Impact**: Users cannot discover new modules to install via the CLI yet.

### B. Automatic Virtual Environment Management
- **Legacy (`framework/venv_ensurer.py`)**: Automatically created and activated a `.adhd-venv` virtual environment.
- **New System**: Relies on the user or IDE to manage the Python environment.
- **Status**: ⚪ Deprecated (Intentional)
- **Reason**: Explicit environment management is preferred in modern development workflows (VS Code, Poetry, Conda, etc.).

## 3. Feature Mapping (Legacy Genesis -> New Cores)

| Feature | Legacy Component | New Component | Status |
| :--- | :--- | :--- | :--- |
| **CLI Entry Point** | `framework/cli.py` | `adhd_framework.py` | ✅ Migrated |
| **Project Creation** | `framework/project_creator.py` | `cores/project_creator_core` | ✅ Migrated |
| **Module Creation** | `framework/module_creator.py` | `cores/module_creator_core` | ✅ Migrated |
| **Git/User Utils** | `framework/utils.py` | `cores/creator_common_core` | ✅ Migrated |
| **Remote Listing** | `framework/listing.py` | *None* | 🔴 Missing |

## 4. New Capabilities (Self-Hosting)

The following features were **not** present in the Legacy Genesis CLI (they existed only in the *templates* it created). They are now native to the Bootstrapped Framework, enabling self-management:

| Feature | Description | Component |
| :--- | :--- | :--- |
| **Project Initialization** | Clones modules defined in `init.yaml`. | `cores/project_init_core` |
| **Requirements Install** | Installs `requirements.txt` from all modules. | `cores/project_init_core` |
| **Project Refresh** | Runs `refresh.py` scripts for modules. | `cores/modules_controller_core` |
| **Instruction Sync** | Syncs `*.instructions.md` to `.github/`. | `cores/instruction_core` |
| **Config Management** | Centralized configuration. | `managers/config_manager` |
| **Logging** | Centralized logging. | `utils/logger_util` |

## 5. Recommendations

1.  **Implement Remote Listing**:
    *   Create a new core (e.g., `cores/module_listing_core`) or extend `modules_controller_core` to support fetching and listing remote modules from a registry YAML.
    *   Port the logic from `framework/listing.py`.

2.  **Verify Self-Bootstrapping**:
    *   Ensure `adhd_framework.py` can successfully bootstrap a fresh environment without `project_init_core` pre-installed (Completed via `bootstrap()` function).
