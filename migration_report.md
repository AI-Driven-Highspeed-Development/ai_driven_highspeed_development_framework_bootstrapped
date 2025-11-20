# ADHD Framework Migration Report

This report compares the functionality of the legacy `framework/` directory with the new modularized core system (`cores/`, `managers/`, etc.) and identifies unimplemented functionality.

## 1. Missing Functionality

The following features exist in the legacy framework but are currently missing or incomplete in the new modules:

### A. Automatic Requirements Installation
- **Legacy (`framework/install_requirements.py`)**: Scans the entire project for `requirements.txt` files and installs them using `pip`.
- **New System**: `cores/project_init_core/requirements_installer.py` implements this functionality.
- **Status**: ✅ Implemented

### B. Project Refresh Mechanism
- **Legacy (`framework/project_refresh.py`)**: Scans for modules with a `refresh.py` script and executes them. This is used to update module configurations or state.
- **New System**: `cores/modules_controller_core` now supports `refresh.py` discovery and execution via `run_module_refresh_script`.
- **Status**: ✅ Implemented

### C. Framework Upgrade System
- **Legacy (`framework/upgrade.py`)**: Handles self-updating of the framework by cloning the template repository, backing up current files, and replacing the `framework/` directory and CLI tools.
- **New System**: No equivalent core module exists.
- **Status**: ⚪ Deprecated (Superseded by Module System)
- **Reason**: Users/Devs can now update individual modules via `git pull` or the module management tools, making a monolithic framework upgrade unnecessary.

### D. Instructions Cloning
- **Legacy (`framework/project_init.py`)**: Automatically finds `*.instructions.md` files in cloned modules and copies them to `.github/instructions/` for AI context.
- **New System**: `cores/project_init_core` clones the modules but does **not** copy the instruction files to the central `.github` location.
- **Status**: 🔴 Unimplemented

### E. Version Checking & Updating during Init
- **Legacy (`framework/project_init.py`)**: When initializing, if a module already exists, it compares the local version with the remote version (from `init.yaml`) and updates it if the remote is newer.
- **New System**: `cores/project_init_core/modules_cloner.py` simply skips cloning if the destination directory already exists.
- **Status**: ⚪ Deprecated (Superseded by Git)
- **Reason**: Git is the source of truth for versions.
- **Future Consideration**: We may add branch/tag selection to `init.yaml` in the future to allow pinning specific versions (e.g., for breaking changes), but this is not currently planned.

### F. Explicit SSH Configuration
- **Legacy (`framework/project_init.py`)**: Had explicit handling for `ADHD_USE_SSH` and `ADHD_SSH_KEY` environment variables to configure Git SSH access.
- **New System**: Relies on the underlying system's Git configuration via `cores/github_api_core`.
- **Status**: ⚪ Deprecated (Superseded by GitHub CLI/System Git)
- **Reason**: The `gh` CLI and system-level Git configuration handle authentication securely and effectively, removing the need for custom SSH key handling in the framework.

## 2. Feature Mapping Summary

| Feature | Legacy Component | New Component | Status |
| :--- | :--- | :--- | :--- |
| **Project Initialization** | `framework/project_init.py` | `cores/project_init_core` | ✅ Implemented |
| **Module Management** | `framework/modules_control.py` | `cores/modules_controller_core` | ✅ Implemented |
| **YAML Handling** | `framework/yaml_util.py` | `cores/yaml_reading_core` | ✅ Implemented |
| **Logging/Formatting** | `framework/cli_format.py` | `utils/logger_util` | ✅ Implemented |
| **Requirements Install** | `framework/install_requirements.py` | `cores/project_init_core` | ✅ Implemented |
| **Project Refresh** | `framework/project_refresh.py` | `cores/modules_controller_core` | ✅ Implemented |
| **Framework Upgrade** | `framework/upgrade.py` | *None* | ⚪ Deprecated |
| **Instructions Sync** | `framework/project_init.py` | *None* | 🔴 Missing |

## 3. Recommendations

1.  **Update `project_init_core`**:
    *   Add a step to copy `*.instructions.md` files after cloning.

## 4. CLI Migration Status

The main entry point `adhd_framework.py` has been updated to utilize the new modular cores, replacing the functionality of the legacy `adhd_cli.py`.

| Command | Legacy `adhd_cli.py` | New `adhd_framework.py` | Status |
| :--- | :--- | :--- | :--- |
| **Init Project** | `init` | `init` | ✅ Migrated |
| **Refresh Project** | `refresh` | `refresh` | ✅ Migrated |
| **List Modules** | `list` | `list` | ✅ Migrated |
| **Module Info** | `info` | `info` | ✅ Migrated |
| **Install Req.** | `req` | `req` | ✅ Migrated |
| **Create Project** | *N/A* | `create-project` | ✅ Preserved |
| **Create Module** | *N/A* | `create-module` | ✅ Preserved |
| **Upgrade** | `upgrade` | *None* | ⚪ Deprecated |
