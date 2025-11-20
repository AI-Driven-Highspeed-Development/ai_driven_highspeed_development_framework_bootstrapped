---
applyTo: "project/**,managers/**,plugins/**,utils/**,mcps/**,cores/**,**.py"
---

Config Manager:
- Purpose: Centralized config management for ADHD framework projects, structured access and modification for module settings.
- Usage:
```
from managers.config_manager.config_manager import ConfigManager
cm = ConfigManager()
config = cm.config.my_module_name
data_path = config.paths.data
```
- Update config: run `python adhd_cli.py refresh --module config-manager` to regenerate code after modifying .config, can omit `--module` to refresh all for convenience, remind user for manually sync instead of done by AI agent.
- <module_type>/<module_name>/.config_template: defines default config schema auto-generated into .config on module init. refresh after edits will not overwrite user changes to prevent data loss, manual sync to .config before refresh maybe needed.