# ADHD Framework (Bootstrapped)

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
    -   *Benefit*: Drastically reduces "Objective Misalignment" by providing ground-truth rules alongside the code.

## Structure

```
📦 Project-Root/
├── 📄 adhd_framework.py        # Main CLI interface
├── 📄 app.py                   # Main app entry point (change filename to suit your project)
├── 📄 init.yaml                # Project configuration
├── 📁 cores/                   # Core system modules
│   ├── 📁 project_init_core/   # Project initialization & cloning
│   ├── 📁 modules_controller_core/ # Module management
│   └── ...
├── 📁 managers/                # State & Config manager modules
├── 📁 utils/                   # Utility modules
├── 📁 plugins/                 # Plugin modules
├── 📁 mcps/                    # Model-Context-Protocol modules
└── 📄 README.md                # This file
```

## Setup

### 1. Prerequisites
-   **Python 3.8+**
-   **Git** (Installed and configured)
-   **GitHub CLI (`gh`)** (Required for cloning modules)
    -   *Run `gh auth login` to authenticate.*
-   **Visual Studio Code** (Required)
    -   *Why?* The framework's `instruction_core` and agent workflows are deeply integrated with VS Code's agent capabilities.
    -   *Note*: While you *can* use other IDEs, you will lose the AI-native context features (agents & instructions) that are the core value proposition of this framework. Support for other IDEs is planned for the future.

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
    *Note: On Linux/Mac, the script will automatically attempt to make itself executable (`chmod +x`).*

4.  **Enable Tab Completion** (Recommended)
    The CLI supports tab completion for commands and module names.
    -   On the first run, the script will prompt you to automatically add completion support to your virtual environment's activation script.
    -   **Action**: Type `y` when prompted.
    -   **Apply**: Deactivate and re-activate your virtual environment for changes to take effect.

    *Note: Also only supported on Linux/Mac at this time. Windows support may not be possible due to shell limitations.*

5.  **Verify Installation**
    Check that everything is running correctly:
    ```bash
    ./adhd_framework.py list
    ```

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

Each module follows a strict structure to ensure compatibility with the framework and agents:

```
📁 module_type/                         # i.e. managers / utils / plugins / cores / mcps
└──📁 module_name/
    ├── 📁 data/                        # Module-specific data (optional)
    ├── 📄 __init__.py                  # Python package (optional, enables ✅ Init)
    ├── 📄 refresh.py                   # Refresh script (optional, enables 🔄 Refresh)  
    ├── 📄 init.yaml                    # Module configuration (required)
    ├── 📄 module_name.instructions.md  # Agent instructions (optional)
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
shows_in_workspace: true # Override default visibility
```

## Agents

The framework comes with specialized AI agents, each with a distinct role and "personality" to handle different aspects of the development lifecycle.

| Agent | Role | Description |
| :--- | :--- | :--- |
| **HyperArchitect** | Lead Developer | The primary builder. Implements features, modifies code, and ensures strict adherence to the ADHD framework's architecture and patterns. |
| **HyperSanityChecker** | QA & Auditor | Meticulous code reviewer. Audits plans and code for logic flaws, security risks, and architectural violations before implementation. |
| **HyperIQGuard** | Code Quality Guardian | Identifies and fixes objectively poor coding practices (anti-patterns), redundancy, and inefficiencies. Focuses on pragmatic, safe, local fixes. |
| **HyperPM** | Project Manager | Manages Kanban boards and planning using **kanbn**. Creates and maintains kanbn boards in `.kanbn/`. |
| **HyperDayDreamer** | Visionary Architect | Focuses on long-term planning and conceptualization. Documents visions and future possibilities without modifying the codebase. |
| **HyperAgentSmith** | Agent Creator | Designs, generates, and validates new agent definitions (`.agent.md`). Ensures strict adherence to framework standards and safety protocols. |

## Typical Workflows

### 1. Install this Framework

Follow the [Setup](#setup) instructions to clone and bootstrap the ADHD Framework.

### 2. Create a New ADHD Project

  ```bash
  ./adhd_framework.py cp
  ```
  - Follow the interactive prompts to set up your new project. 

  - Select the option to create a repository in your GitHub account / organization is recommended.

### 3. Initialize the Project

  ```bash
  ./adhd_framework.py init
  ```
  - This will clone and set up all specified modules from `init.yaml`.

### 4. Plan your modules

  - ADHD Framework is module-centric. Plan out which and what modules you need for your project.

  - `Public Modules Repository` is coming soon with pre-built modules, you will be able to select from a list.

  - For now, you can:

    1. Go to `https://github.com/orgs/AI-Driven-Highspeed-Development/repositories` to shop for modules (WARNING: Many are under development or outdated and may be unstable, this framework is an one man army project after all). Or;

    2. Build your own modules:

        ```bash
        ./adhd_framework.py cm
        ```

  - To fully utilize the ADHD Framework, you should aim to:
  
    Break your project down into as many small, **single-responsibility modules** as possible. 
  
    **Do not create Swiss Army Knife modules that try to do everything!**

  - After created your modules, add their URL(s) to your project's `init.yaml`, under `modules` as a list, and run `./adhd_framework.py init` again to install them.

### 5.Module Management

  - For configuration, each module has its own `.config_template` file that you can edit to add default configuration values, which will be copied to the project's root `.config` file on initialization or refresh.
    ```bash
    ./adhd_framework.py r -m managers/config_-_manager
    # or just refresh all modules when you are lazy
    ./adhd_framework.py r
    ```
    You can also directly edit the project's root `.config` file to override any configuration values.

  - Each module contains its own `instructions.md` file that teaches agents how to work with that specific module. Read [The VS code doc](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) For more information on how to write effective instructions for AI agents, or, just ask the `HyperAgentSmith` agent to help you write one!
  
    Then also refresh:
    ```bash
    ./adhd_framework.py r -m cores/instruction_core
    # or 
    ./adhd_framework.py r
    ```


### 5. Develop with AI Agents

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

### 6. Stuck? Tech debt piling up? Smelling delicious spaghetti in your codebase?

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


### 7. Be aware of Limitations

  - The ADHD Framework is still in early development. Many modules are experimental and may contain bugs or incomplete features.

  - Always review and test code generated by AI agents thoroughly.

    > **You are the ultimate decision maker and quality controller, you have the responsibility on the project quality, not the AI agents.**

    > **This is not a vibe coding Framework, objective alignment and safeguarding are always dependent on you.**


## Troubleshooting

### Import Errors
If you encounter import errors, ensure you're running commands from the project root directory where `adhd_framework.py` is located.

### Module Not Found
Use `./adhd_framework.py ls` to see available modules and their exact names.

## License

See LICENSE file for details.