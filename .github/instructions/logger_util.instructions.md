---
applyTo: "project/**,managers/**,plugins/**,utils/**,mcps/**,cores/**,app.py"
---

Logger Util:
- Purpose: Centralized logging helpers that standardize formatting, verbose toggles, and optional file handlers across the framework using Python's `logging` module.
- Usage:
```
from utils.logger_util.logger import Logger, get_central_logger, set_logger_style
from utils.logger_util.logger_style import NormalStyle

log = Logger(name="MyModule", verbose=True)
log.debug("Compact style output")

set_logger_style(log, NormalStyle())
log.info("Now using the normal style")

get_central_logger(verbose=True).debug("Central diagnostics")
```
- Verbose handling: pass `verbose=True` (or set `level`) when constructing `Logger` or retrieving the central logger to enable DEBUG output; defaults to INFO.
- Handler safety: `Logger` instances are singletons per name; rely on provided helpers for style/level changes to avoid duplicate handlers.
