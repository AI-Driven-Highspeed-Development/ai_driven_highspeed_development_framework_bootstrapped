---
applyTo: "**"
---
# ADHD Framework Exception Handling Policy

This policy ensures robust, predictable, and debuggable code across all modules.

### Tier 1: User & Config Errors -> Use Standard Python Exceptions

-   **What**: Invalid user input, misconfiguration, or bad data.
-   **Action**: **Always** use standard Python exceptions (`ValueError`, `KeyError`, `FileNotFoundError`, etc.).
-   **Example**: `raise ValueError("Module name contains invalid characters.")`
-   **Why**: Predictable, universally understood, requires no extra code.

### Tier 2: Application & Service Errors -> Use `ADHDError`

-   **What**: Anticipated failures in application logic or external systems (APIs, shell commands).
-   **Action**: Catch the specific low-level exception and re-raise `ADHDError` using `from`.
-   **Import**: `from cores.exceptions_core.adhd_exceptions import ADHDError`
-   **Example**:
    ```python
    try:
        requests.get("...").raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ADHDError(f"API request failed: {e}") from e
    ```
-   **Why**: Allows the application to catch all *known* operational failures with a single `except ADHDError:`, distinguishing them from unexpected bugs.

### Tier 3: Bugs & Unexpected Errors -> Do Nothing

-   **What**: Unanticipated problems (`AttributeError`, `IndexError`, `TypeError`, etc.). These are bugs in our code.
-   **Action**: **Do not catch these exceptions.** Let the program crash.
-   **Why**: A crash provides a full, unmodified traceback, which is essential for debugging. Silencing these errors hides bugs and makes the code harder to maintain.
