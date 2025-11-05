---
applyTo: "project/**,app.py,managers/**,plugins/**,utils/**,mcps/**,cores/**"
---

Logger Utility (AI note)

- Purpose: Centralized logging helpers for modules; prefer over print and ad‑hoc logging once bootstrapped.

- Usage:
```
from utils.logger_util.logger import Logger, get_central_logger, set_logger_style
from utils.logger_util.logger_style import NormalStyle

# Per-name singleton: constructing with the same name returns the same wrapper
log = Logger(name="MyModule")
log.info("ready")

# Reuse and reconfigure on construction (only provided params are applied)
Logger(name="MyModule", verbose=True)  # now DEBUG level

# Change console style (wrapper or std logging.Logger accepted)
set_logger_style(log, NormalStyle())

# File logging
Logger(name="Service", log_to_file=True).info("to file")

# Central logger (returns std logging.Logger)
get_central_logger().info("central message")
```

- Modules Convention:
	- Use same logger name in the same module for consistency.


- Specifics:
	- One wrapper per name (singleton). Reconstructing with params will update that logger's config.
	- For file logs use Logger(..., log_to_file=True, log_file_path=...). Default path is ./logs/<name>_YYYYMMDD.log.
	- Keep verbose=False in production; pass verbose=True only when diagnosing.
