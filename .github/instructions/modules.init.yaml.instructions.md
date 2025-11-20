---
applyTo: "cores/**/init.yaml, managers/**/init.yaml, plugins/**/init.yaml, utils/**/init.yaml, mcps/**/init.yaml"
---

# Module init.yaml Authoring Instructions

`init.yaml`: Metadata:
- version: str (e.g., 0.0.1)
- folder_path: str (e.g., managers/config_manager) # legacy, do not use or remove.
- type: str (e.g., manager / core / util / plugin / mcp)
- repo_url: str (url to module repo in GitHub)
- shows_in_workspace: bool (whether to show in ADHD workspace UI)
- requirements: list of str (urls of required ADHD modules)

## Instructions for Creating/Editing `init.yaml` Files

1. **Versioning**: Follow semantic versioning (MAJOR.MINOR.PATCH). Increment:
   - MAJOR for incompatible changes,
   - MINOR features,
   - PATCH for bug fixes.
   - Start at 0.0.1 for new modules.
   - No need to update version unless user explicitly requests.

2. **Folder Path**: Specify the module's folder path relative to the project root (e.g., `managers/config_manager`). This is for legacy purposes; new modules should not have this field, old modules should retain it, only user can manually remove it.

3. **Type**: Choose from predefined types:
   - `core`, `manager`, `util`, `plugin`, `mcp`.

