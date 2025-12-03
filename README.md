# ADHD Framework

This is the bootstrapped version of the ADHD (AI-Driven High-speed Development) Framework, featuring a modular core architecture.

## Core Philosophy

The **ADHD (AI-Driven High-speed Development) Framework** is built on a single premise: **AI agents are the new developers, and they need a workspace designed for them.**

### The "Vibe Coding" Trap
Modern "vibe coding" with LLMs is deceptively fast. You can generate a prototype in minutes. But as complexity grows, you hit the **Context Wall**:
-   **Objective Misalignment**: Agents misunderstand project goals without clear guidance.
-   **Forced solutions**: Agents hack around limitations instead of addressing root causes, causing more issues down the line.
-   **Hallucinations**: Agents lose track of large file structures.
-   **Regression**: Fixing one bug breaks three other features.
-   **Scalability**: "One giant script" architectures collapse under their own weight.

### The ADHD Solution
We treat the codebase as a **Structured Knowledge Graph** rather than just text files.

1.  **Fractal Modularity**:
    -   Everything is a module (Types: `Core`, `Manager`, `Util`, `Plugin`, `MCP`).
    -   Each module is self-contained with its own `init.yaml` (metadata), `refresh.py` (state management), and `instructions.md` (agent context).
    -   *Benefit*: Agents only need to load the specific module they are working on, fitting perfectly within context windows.

2.  **Deterministic Lifecycle**:
    -   **Init**: Standardized bootstrapping ensures every module starts in a known good state.
    -   **Refresh**: Idempotent self-healing scripts allow modules to repair their own state or data.
    -   *Benefit*: Agents can "reset" parts of the system without breaking the whole.

3.  **AI-Native Context**:
    -   Preset agents with specific roles to handle different tasks (e.g., `HyperArchitect`, `HyperSanityChecker`, `HyperIQGuard` etc.).
    -   The framework includes instruction files (`.instructions.md`) that teach agents *how* to use the code they are looking at.
    -   The `instruction_core` module syncs all agent definitions and instruction files from modules to `.github/` where VS Code's Copilot picks them up automatically.
    -   *Benefit*: Drastically reduces "Objective Misalignment" by providing ground-truth rules alongside the code.

## Structure

```
📦 Project-Root/
├── 📄 adhd_framework.py        # Main CLI interface
├── 📄 app.py                   # Main app entry point (name it to suit your project)
├── 📄 init.yaml                # Project configuration
├── 📁 project/                 # (Optional) Project-specific files 
│   ├── 📁 data/                # (Optional) Project data files, conventional location 
├── 📁 cores/                   # Core system modules
│   ├── 📁 project_init_core/   # Project initialization & cloning
│   ├── 📁 modules_controller_core/ # Module management
│   └── ...
├── 📁 managers/                # State & Config manager modules
├── 📁 utils/                   # Utility modules
├── 📁 plugins/                 # Plugin modules
├── 📁 mcps/                    # Model-Context-Protocol modules
├── 📁 .agent_plan/             # (Optional) Agent-generated plans and visions
├── 📄 requirements.txt         # Python dependencies
└── 📄 README.md                # This file
```

## Setup

### 1. Prerequisites
-   **Python 3.9+**
-   **Git** (Installed and configured)
-   **GitHub CLI (`gh`)** (Required for cloning modules)
    -   *Run `gh auth login` to authenticate.*
-   **Visual Studio Code** (Required)
    -   *Why?* The framework's `instruction_core` and agent workflows are deeply integrated with VS Code's agent capabilities.
    -   *Note*: While you *can* use other IDEs, you will lose the AI-native context features (agents & instructions) that are the core value proposition of this framework. Support for other IDEs is planned for the future.
    -   *Recommended Extension*: `samgiz.vscode-kanbn-boards` (Required for **HyperPM** Kanban visualization).

### 2. Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/AI-Driven-Highspeed-Development/ai_driven_highspeed_development_framework_bootstrapped.git
    cd ai_driven_highspeed_development_framework_bootstrapped
    ```

2.  **Set up Virtual Environment** (Critical)
    You **must** use a virtual environment.
    ```bash
    # Create venv
    python3 -m venv .venv
    
    # Activate (Linux/Mac)
    source .venv/bin/activate
    
    # Activate (Windows)
    .venv\Scripts\Activate
    ```

3.  **Bootstrap the Framework**
    Run the CLI for the first time. It will automatically clone core modules and install dependencies.
    ```bash
    python adhd_framework.py
    ```
    *Note: This may take a moment to clone all required repositories.*

4.  **Verify Installation**

    Check that everything is running correctly:

    Linux/Mac:
    ```bash
    ./adhd_framework.py list
    ```

    Windows:
    ```bash
    python adhd_framework.py list
    ```

    *Note: On Linux/Mac, the script will automatically attempt to make itself executable (`chmod +x`). Windows not supported.*

## Quick Start

The ADHD CLI provides a simple interface to all framework functionality.

If you can't run `./adhd_framework.py` directly, (e.g. on Windows), use: `python adhd_framework.py`

```bash
# Initialize a new project from init.yaml
./adhd_framework.py init

# List all discovered modules
./adhd_framework.py list

# Refresh all modules (pull updates & run refresh scripts)
./adhd_framework.py refresh

# Show detailed info about a specific module
./adhd_framework.py info -m config-manager
```

The ADHD Framework supports **Tab Completion**, see [Tips & Tricks](#tips--tricks) for setup instructions.

## CLI Reference

The framework is controlled via the `adhd_framework.py` script.

### `create-project` (cp)
Launch the interactive wizard to create a new ADHD project.
```bash
./adhd_framework.py cp
```

### `create-module` (cm)
Launch the interactive wizard to create a new module from templates.
```bash
./adhd_framework.py cm
```

### `init` (i)
Initialize a new ADHD project by cloning and setting up modules from the configuration file.
```bash
./adhd_framework.py i
```

### `refresh` (r)
Refresh project modules to update them with the latest changes.
```bash
./adhd_framework.py r
./adhd_framework.py r -m logger  # Refresh specific module
```

### `list` (ls)
List all discovered modules and their capabilities.
```bash
./adhd_framework.py ls
```

### `info` (in)
Show detailed information about a specific module.
```bash
./adhd_framework.py in -m logger
```

### `req` (rq)
Install requirements from all `requirements.txt` files found in the project and its modules.
```bash
./adhd_framework.py rq
```

## Configuration

Edit the `init.yaml` file in your project root to specify modules to install:

```yaml
name: "My ADHD Project"
description: "An example ADHD project"
modules:
  - https://github.com/AI-Driven-Highspeed-Development/Config-Manager.git
  - https://github.com/AI-Driven-Highspeed-Development/Logger-Util.git
```

## Module Architecture

### Module Types

Modules are categorized by their role in the system. This separation prevents "Swiss Army Knife" modules and helps agents understand the purpose of each module at a glance.

| Type | Folder | Purpose | Examples |
| :--- | :--- | :--- | :--- |
| **Core** | `cores/` | Framework internals. Bootstrapping, module lifecycle, agent sync. Rarely modified by users. | `instruction_core`, `modules_controller_core` |
| **Manager** | `managers/` | Stateful resource management with lifecycle. Typically singletons that persist configuration or state. | `config_manager`, `temp_files_manager` |
| **Util** | `utils/` | Stateless helper functions/classes. Pure utilities with no side effects, highly reusable. | `logger_util` |
| **Plugin** | `plugins/` | Project-specific extensions. When something is *too specific* to be reusable across projects. | `my_app_plugin` |
| **MCP** | `mcps/` | Model Context Protocol servers. Extends AI agent capabilities with external tools and APIs. | `github_mcp`, `database_mcp` |

> **Why these 5 types?**
> - Fewer types → Everything becomes a generic "module" (Swiss Army Knife problem)
> - More types → Analysis paralysis, over-categorization
> - These 5 cover the spectrum from "framework core" to "project-specific" with clear, non-overlapping boundaries.

### Module Structure

Each module follows a strict structure to ensure compatibility with the framework and agents:

```
📁 module_type/                         # i.e. managers / utils / plugins / cores / mcps
└──📁 module_name/
    ├── 📁 data/                        # Module-specific data (Optional)
    ├── 📄 __init__.py                  # Python package (Optional, enables ✅ Init)
    ├── 📄 refresh.py                   # Refresh script (Optional, enables 🔄 Refresh)  
    ├── 📄 init.yaml                    # Module configuration (Required)
    ├── 📄 module_name.instructions.md  # Agent instructions (Optional)
    ├── 📄 module_name.py               # Main module code (name it to suit your module)
    ├── 📄 requirements.txt             # Python dependencies for the module
    └── 📄 [other files]                # Module-specific files
```

The `init.yaml` file should contain:
```yaml
name: "Module Name"
type: "module_type"  # e.g., "manager", "util", "plugin", "core", "mcp"
version: "1.0.0"
description: "Module description"
repo_url: "https://github.com/user/repo.git"
requirements:  # ADHD modules Dependencies, URLs (optional)
  - http://example.com/dependency.git
  - http://example.com/another-dependency.git
shows_in_workspace: true # Override default visibility in VS Code multi-root workspace
```

### Configuration Management

The `config_manager` module handles project and module configuration:
-   Each module can have a `.config_template` file with default values.
-   On refresh, templates are merged into the project's root `.config` file.
-   See `managers/config_manager/README.md` for detailed usage.

## Agents

The framework comes with specialized AI agents, each with a distinct role and "personality" to handle different aspects of the development lifecycle.

| Agent | Role | Description |
| :--- | :--- | :--- |
| **HyperArchitect** | Lead Developer | The primary builder. Implements features, modifies code, and ensures strict adherence to the ADHD framework's architecture and patterns. |
| **HyperSanityChecker** | QA & Auditor | Meticulous code reviewer. Audits plans and code for logic flaws, security risks, and architectural violations before implementation. |
| **HyperIQGuard** | Code Quality Guardian | Identifies and fixes objectively poor coding practices (anti-patterns), redundancy, and inefficiencies. Focuses on pragmatic, safe, local fixes. |
| **HyperPM** | Project Manager | Manages Kanban boards and planning using **kanbn**. Creates and maintains kanbn boards in `.kanbn/`. **Requires `samgiz.vscode-kanbn-boards` extension.** |
| **HyperDayDreamer** | Visionary Architect | Focuses on long-term planning and conceptualization. Documents visions and future possibilities without modifying the codebase. |
| **HyperAgentSmith** | Agent Creator | Designs, generates, and validates new agent definitions (`.agent.md`). Ensures strict adherence to framework standards and safety protocols. |

### How Agents Work

Agent definitions (`.adhd.agent.md`) and instruction files (`.instructions.md`) are stored in:
-   `cores/instruction_core/data/agents/` — Framework-provided agents
-   `cores/instruction_core/data/instructions/` — Framework-wide instructions  
-   `cores/instruction_core/data/prompts/` — Reusable prompts (coming soon)
-   `<module_folder>/<module_name>.instructions.md` — Module-specific instructions

When you run `./adhd_framework.py refresh`, the `instruction_core` copies all these files to `.github/instructions/`, `.github/agents/`, and `.github/prompts/`. VS Code's Copilot automatically picks up files from `.github/` for custom instructions.

**To use an agent**: In VS Code Copilot Chat, type `@` followed by the agent name (e.g., `@hyper_architect`).

## Typical Workflows

### 1. Install this Framework

Follow the [Setup](#setup) instructions to clone and bootstrap the ADHD Framework.

**NOTE**: Use `python adhd_framework.py` if you can't run `./adhd_framework.py` directly (e.g., on Windows).

### 2. Create a New ADHD Project

  ```bash
  ./adhd_framework.py cp
  ```
  - Follow the interactive prompts to set up your new project. 

  - Select the option to create a repository in your GitHub account / organization is recommended.

### 3. Initialize the Project

  Go to your newly created project folder by opening it in VS Code:

  1. File -> Open workspace...
  2. Select the project folder you just created.
  3. Select the .code-workspace file inside it.

  Then create the .venv for your **NEW** project (**NOT** for this framework repo):

  By terminal:

  Linux/Mac: 
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate  # Linux/Mac
  ```

  Windows:
  ```bash
  python -m venv .venv
  .venv\Scripts\Activate    # Windows
  ```

  **OR** via VS Code Command Palette:

  1. Toggle the Command Palette (Linux/Windows: `Ctrl+Shift+P`, Mac: `Cmd+Shift+P`)
  2. Type and select `Python: Create Environment`
  3. Select `Venv` as environment type
  4. Select the suitable Python version (3.9+)
  5. Select the option to create the environment in the project folder
  6. Create a new terminal in VS Code to activate the new virtual environment automatically.

  Finally, in the new venv, run:

  ```bash
  ./adhd_framework.py init
  ```
  - This will clone and set up all specified modules from `init.yaml`.

### 4. Plan your modules

  - ADHD Framework is module-centric. Plan out which and what modules you need for your project.

  - `Public Modules Repository` is coming soon with pre-built modules, you will be able to select from a list.

  - For now, you can:

    1. Go to `https://github.com/orgs/AI-Driven-Highspeed-Development/repositories` to shop for modules (WARNING: Many are under development or outdated and may be unstable, this framework is an one man army project after all 🤣). Or;

    2. Build your own modules:

        ```bash
        ./adhd_framework.py cm
        ```

  - To fully utilize the ADHD Framework, you should aim to:
  
    Break your project down into as many small, **single-responsibility modules** as possible. 
      
      **Do not create Swiss Army Knife modules that try to do everything!**

      > A small example toy scenario:
      >
      >>You are building a web app that needs user **authentication**, **data storage**, and **email notifications**.
      >
      > Instead of creating one giant "WebApp" module, create three focused modules:
      > 1. `oauth2_auth_manager` module for handling user authentication.
      > 2. `mysql_database_manager` module for data storage and retrieval.
      > 3. `smtp_email_plugin` module for sending email notifications.
      > 4. Any other modules as needed for specific features...
      >
      > **Pro Tip**: Name your modules specifically (e.g., `mysql_database_manager` instead of just `database_manager`). This ensures they are reusable across different projects. If a module *must* be specific to only this project, it is usually best to categorize it as a `plugin`.
      >
      > Each module has its own purpose, allowing agents to work on them independently without overwhelming context.

  - After created your modules, add their URL(s) to your project's `init.yaml`, under `modules` as a list, and run `./adhd_framework.py init` again to install them.

### 5. Module Management

  - **Configuration**: Modules use `.config_template` files for default values, merged into the project's `.config` on refresh. See `managers/config_manager/README.md`.

  - **Instructions**: Each module can have a `<module_name>.instructions.md` file to teach agents how to use it. Run `./adhd_framework.py refresh` to sync instructions to `.github/`. See [VS Code Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) for writing tips, or ask `HyperAgentSmith` to help!

### 6. Develop with AI Agents

  - Use the built-in ADHD agents to plan, code, review, and manage your project.
  - I can only give some general guidelines here, the project quality ultimately depends on:

    > **How well you can fundamentally understand and organize your own thoughts, and logically express them to others, human or AI agents.**

  - You can start by asking the:
  - `HyperDayDreamer` agent to help you brainstorm and document your project vision. Then have the:
  - `HyperSanityChecker` review it for clarity, sanity, and completeness, before passing it to the:
  - `HyperPM` agent to create tasks and manage your kanbn board, finally, have the:
  - `HyperArchitect` implement the features, with
  - `HyperIQGuard` ensuring code quality along the way. And if you need new agents, just ask:
  - `HyperAgentSmith` to create them for you!
  - Rinse and repeat!

### 7. Stuck? Tech debt piling up? Smelling delicious spaghetti in your codebase?

Try these methods:

  - Ask the `HyperSanityChecker` agent to audit your codebase for logic flaws, security risks, and architectural violations.

  - Ask the `HyperIQGuard` agent to identify and fix objectively poor coding practices (anti-patterns), redundancy, and inefficiencies.

  - If nothing works, **NUKE** the affected module(s)!

    1. Delete the module folder(s) from your project.

    2. Remove their URL(s) from `init.yaml` under `modules`.

    3. Run:
        ```bash
        ./adhd_framework.py i
        ```
       This will set up the remaining modules if needed.

    > That is why **modularity** is important. You can always rebuild from scratch without affecting the rest of the project, And AI agents can help you re-implement the lost functionality extremely rapidly! (But this time watch it closely to avoid repeating the same mistakes!)


### 8. Be aware of Limitations

  - The ADHD Framework is still in early development. Many modules are experimental and may contain bugs or incomplete features.

  - Always review and test code generated by AI agents thoroughly.

    > **You are the ultimate decision maker and quality controller, you have the responsibility on the project quality, not the AI agents.**

    > **This is not a vibe coding Framework, objective alignment and safeguarding are always dependent on you.**

## Tips & Tricks

### Tab Completion (Linux/Mac)

The CLI supports tab completion for commands and module names:
1.  On the first run, the script will prompt you to add completion support to your venv's activation script.
2.  Type `y` when prompted.
3.  Deactivate and re-activate your virtual environment.

*Note: Windows is not supported due to shell limitations.*

Example usage:
```bash
./adhd_framework.py <TAB>  # Auto shows available commands
./adhd_framework.py info -m <TAB>  # Auto shows available module names
./adhd_framework.py info -m managers<TAB>  # Auto shows modules starting with "managers"
./adhd_framework.py info -m managers/c<TAB>  
# Auto-completes to "managers/config_manager" if it is the only match starting with "c"
```

### Setting `shows_in_workspace` in `init.yaml`

Controls whether a module appears as a folder in VS Code's multi-root workspace:
-   `true` — Module folder is visible (default for `managers`, `utils`, `plugins`)
-   `false` — Module folder is hidden (default for `cores`, `mcps`)

Useful for hiding implementation details from day-to-day development while keeping them accessible.

## Troubleshooting

### Import Errors
If you encounter import errors, ensure you're running commands from the project root directory where `adhd_framework.py` is located.

### Module Not Found
Use `./adhd_framework.py ls` to see available modules and their exact names.

### Ask for Help
If you are using this, you probably know the developer personally, just reach out to me on Signal or Whatsapp and tell me my stupid thingy doesn't work 😂

Or, very fortunately, you don't know me personally but somehow found this project and want to reach out, you can open an issue on GitHub to ask for help.


## License

See LICENSE file for details.