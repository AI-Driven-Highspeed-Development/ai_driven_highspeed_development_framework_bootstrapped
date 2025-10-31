# Default Project Template for AI Driven Highspeed Development Framework

This is the default project template that gets cloned when creating new ADHD Framework projects.

## Structure

```
📦 Default-Project-Template/
├── 📄 adhd_cli.py              # Main CLI interface for project management
├── 📄 init.yaml                # Default module configuration
├── 📁 framework/               # Core framework modules
│   ├── 📄 __init__.py         # Package initialization
│   ├── 📄 modules_control.py  # Module discovery and management
│   ├── 📄 project_init.py     # Project initialization logic
│   └── 📄 project_refresh.py  # Module refresh functionality
└── 📄 README.md               # This file
```

## Usage

After your project is created using the main ADHD Framework, you can use the included CLI:

### Initialize Project
```bash
python adhd_cli.py init                    # Initialize with default init.yaml
python adhd_cli.py init --config my.yaml  # Use custom config file
```

### Manage Modules
```bash
python adhd_cli.py list                    # List all discovered modules
python adhd_cli.py refresh                 # Refresh all modules
python adhd_cli.py refresh --module logger # Refresh specific module
python adhd_cli.py info --module logger    # Show module details
```

### Get Help
```bash
python adhd_cli.py --help                  # Show main help
python adhd_cli.py init --help             # Show init command help
python adhd_cli.py refresh --help          # Show refresh command help
```

## Framework Modules

- **modules_control.py**: Discovers and manages project modules, providing information about their capabilities and configuration
- **project_init.py**: Handles initial project setup with advanced dependency resolution:
  - Clones repositories and resolves dependencies recursively
  - Implements smart module initialization with proper dependency order
  - Detects and handles circular dependencies gracefully
  - Tracks initialization state to prevent duplicate processing
- **project_refresh.py**: Manages refreshing existing modules by running their refresh scripts

## Dependency Resolution Features

The framework now includes sophisticated dependency management:

### 🔄 **Recursive Dependency Resolution**
- Automatically resolves module dependencies in the correct order
- Initializes required modules before dependent modules
- Supports multi-level dependency chains

### 🛡️ **Circular Dependency Detection**
- Detects circular dependencies during initialization
- Gracefully breaks cycles and continues initialization
- Provides clear warnings about dependency loops

### 📊 **Smart Initialization Tracking**
- Prevents duplicate module initialization
- Tracks successful and failed initializations
- Provides comprehensive initialization reports

### 🔗 **Flexible URL Matching**
- Matches dependency URLs with multiple formats (.git, case-insensitive)
- Supports repository name-based fallback matching
- Handles URL normalization automatically

## Module Structure

Each module should follow this structure:
```
📁 module-name/
├── 📄 __init__.py     # Python package (optional, enables ✅ Init)
├── 📄 refresh.py      # Refresh script (optional, enables 🔄 Refresh)  
├── 📄 init.yaml       # Module configuration (optional, enables ⚙️ Config)
└── 📄 [other files]   # Module-specific files
```

The `init.yaml` file should contain:
```yaml
name: "Module Name"
type: "module_type"  # e.g., "manager", "util", "plugin"
version: "1.0.0"
description: "Module description"
folder_path: "target/directory"  # Where to place this module
requirement:  # Dependencies (optional)
  - "https://github.com/user/dependency.git"
```

This is the default project template for the ADHD (AI-Driven High-speed Development) Framework. It provides a complete setup for rapid project initialization, module management, and development workflow automation.

## Features

- 🚀 **Project Initialization**: Automatically clone and set up project modules from git repositories
- 🔄 **Module Refresh**: Update and refresh existing modules with new versions
- 📦 **Module Management**: Discover, list, and manage project modules
- ⚙️ **Configuration-Driven**: YAML-based configuration for easy customization
- 🎯 **Dependency Resolution**: Recursive dependency handling for complex projects

## Quick Start

### Using the CLI

The ADHD CLI provides a simple interface to all framework functionality:

```bash
# Initialize a new project
python adhd_cli.py init

# Initialize with custom config
python adhd_cli.py init --config my-config.yaml

# List all discovered modules
python adhd_cli.py list

# Refresh all modules
python adhd_cli.py refresh

# Refresh specific module
python adhd_cli.py refresh --module config-manager

# Show detailed module information
python adhd_cli.py info --module config-manager

# Get help
python adhd_cli.py --help
python adhd_cli.py init --help
```

## Configuration

Create an `init.yaml` file in your project root to specify modules to install:

```yaml
modules:
  - https://github.com/AI-Driven-Highspeed-Development/Config-Manager.git
  - https://github.com/AI-Driven-Highspeed-Development/Logger-Util.git
  - https://github.com/AI-Driven-Highspeed-Development/Path-Resolver-Util.git
```

## Project Structure

After initialization, your project will have the following structure:

```
your-project/
├── adhd_cli.py           # Main CLI interface
├── init.yaml             # Project configuration
├── framework/            # Core framework modules
│   ├── __init__.py
│   ├── modules_control.py
│   ├── project_init.py
│   └── project_refresh.py
├── managers/             # Management modules
├── utils/                # Utility modules
└── plugins/              # Plugin modules
```

## Module Features

Each module can provide the following capabilities:

- ✅ **Init**: Automatic initialization via `__init__.py`
- 🔄 **Refresh**: Update capability via `refresh.py`
- ⚙️ **Config**: Configuration via `init.yaml`

## CLI Commands

### `init`
Initialize a new ADHD project by cloning and setting up modules from the configuration file.

**Options:**
- `--config, -c`: Path to YAML configuration file (default: init.yaml)
- `--clone-dir`: Directory for temporary clones (default: clone_temp)

### `refresh`
Refresh project modules to update them with the latest changes.

**Options:**
- `--module, -m`: Refresh specific module by name

### `list`
List all discovered modules and their capabilities.

### `info`
Show detailed information about a specific module.

**Options:**
- `--module, -m`: Module name to show information for (required)

## Examples

### Basic Project Setup
```bash
# 1. Create project directory
mkdir my-adhd-project
cd my-adhd-project

# 2. Copy this template
cp -r /path/to/Default-Project-Template/* .

# 3. Customize init.yaml with your modules
nano init.yaml

# 4. Initialize project
python adhd_cli.py init
```

### Working with Modules
```bash
# See what modules are available
python adhd_cli.py list

# Get detailed info about a module
python adhd_cli.py info --module config-manager

# Refresh a specific module after updates
python adhd_cli.py refresh --module config-manager

# Refresh all modules
python adhd_cli.py refresh
```

## Troubleshooting

### Import Errors
If you encounter import errors, ensure you're running commands from the project root directory where `adhd_cli.py` is located.

### Module Not Found
Use `python adhd_cli.py list` to see available modules and their exact names.

### Permission Issues
Make sure the CLI script is executable:
```bash
chmod +x adhd_cli.py
```

## Contributing

This template is part of the ADHD Framework ecosystem. For contributions and issues, please refer to the main framework repository.

## License

See LICENSE file for details.