#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import sys
import os
import subprocess
import argparse
from pathlib import Path

try:
    import argcomplete
except ImportError:
    argcomplete = None

# -----------------------------------------------------------------------------
# Self-Bootstrapping Logic
# -----------------------------------------------------------------------------
BOOTSTRAP_MODULES = {
    "utils/logger_util": "https://github.com/AI-Driven-Highspeed-Development/Logger-Util.git",
    "managers/config_manager": "https://github.com/AI-Driven-Highspeed-Development/Config-Manager.git",
    "cores/exceptions_core": "https://github.com/AI-Driven-Highspeed-Development/exceptions_core.git",
    "cores/yaml_reading_core": "https://github.com/AI-Driven-Highspeed-Development/yaml_reading_core.git",
    "cores/modules_controller_core": "https://github.com/AI-Driven-Highspeed-Development/modules_controller_core.git",
    "managers/temp_files_manager": "https://github.com/AI-Driven-Highspeed-Development/temp_files_manager.git",
    "cores/github_api_core": "https://github.com/AI-Driven-Highspeed-Development/github_api_core.git",
    "cores/creator_common_core": "https://github.com/AI-Driven-Highspeed-Development/creator_common_core.git",
    "cores/module_creator_core": "https://github.com/AI-Driven-Highspeed-Development/module_creator_core.git",
    "cores/project_creator_core": "https://github.com/AI-Driven-Highspeed-Development/project_creator_core.git",
    "cores/questionary_core": "https://github.com/AI-Driven-Highspeed-Development/questionary_core.git",
    "cores/project_init_core": "https://github.com/AI-Driven-Highspeed-Development/project_init_core.git",
    "cores/workspace_core": "https://github.com/AI-Driven-Highspeed-Development/workspace_core.git",
}

def _clone_and_install(path: Path, repo_url: str) -> None:
    """Helper to clone a repo and install its requirements."""
    print(f"  - Cloning {path}...")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.check_call(
            ["git", "clone", repo_url, str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"    ✅ Cloned {path}")

        # Install requirements immediately
        req_file = path / "requirements.txt"
        if req_file.exists():
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"    ✅ Installed requirements for {path}")

    except Exception as e:
        print(f"    ❌ Error bootstrapping {path}: {e}")
        sys.exit(1)

def bootstrap():
    """
    Ensures that essential modules are present.
    If not, it clones them from the repositories.
    """
    # Check for venv
    if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
        print("❌ Error: Not running in a virtual environment. Please activate a venv before bootstrapping.")
        sys.exit(1)

    missing_modules = [(Path(p), url) for p, url in BOOTSTRAP_MODULES.items() if not Path(p).exists()]
    
    if missing_modules:
        print("🚀 Bootstrapping ADHD Framework...")
        print(f"Found {len(missing_modules)} missing essential modules.")

        for path, repo_url in missing_modules:
            _clone_and_install(path, repo_url)

    # Install root requirements
    if Path("requirements.txt").exists():
        # Check if we need to install (simple check: just do it, pip is fast if satisfied)
        # Or we could check if modules are missing. For now, let's keep it simple but quiet.
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"❌ Error installing requirements: {e}")
            sys.exit(1)
            
    if missing_modules:
        print("✅ Bootstrap complete. Starting Framework...\n")


class ADHDFramework:
    """Main ADHD Framework CLI class"""

    def __init__(self):
        from managers.config_manager import ConfigManager
        from utils.logger_util.logger import Logger
        from cores.github_api_core.api import GithubApi
        from cores.questionary_core.questionary_core import QuestionaryCore

        self.logger = Logger(__class__.__name__)
        self.prompter = QuestionaryCore()

        try:
            self._gh_path = GithubApi.require_gh()
        except RuntimeError as e:
            self.logger.error(f"GitHub CLI setup not complete: {e}")
            sys.exit(1)

    def run(self, args):
        command_map = {
            'create-project': self.create_project_proc,
            'cp': self.create_project_proc,
            'create-module': self.create_module_proc,
            'cm': self.create_module_proc,
            'init': self.init_project,
            'i': self.init_project,
            'refresh': self.refresh_project,
            'r': self.refresh_project,
            'list': self.list_modules,
            'ls': self.list_modules,
            'info': self.show_module_info,
            'in': self.show_module_info,
            'req': self.install_requirements,
            'rq': self.install_requirements,
            'workspace': self.update_workspace,
            'ws': self.update_workspace,
        }

        handler = command_map.get(args.command)
        if handler:
            handler(args)

    def create_project_proc(self, args) -> None:
        from cores.project_creator_core.project_creation_wizard import run_project_creation_wizard
        run_project_creation_wizard(
            prompter=self.prompter,
            logger=self.logger,
        )

    def create_module_proc(self, args) -> None:
        """Enter the interactive module creation flow with templates."""
        from cores.module_creator_core.module_creation_wizard import run_module_creation_wizard
        run_module_creation_wizard(
            prompter=self.prompter,
            logger=self.logger,
        )

    def init_project(self, args) -> None:
        """Initialize project modules."""
        self.logger.info("Initializing project...")
        try:
            from cores.project_init_core.project_init import ProjectInit
            initializer = ProjectInit()
            initializer.init_project()
            self.logger.info("✅ Project initialization completed successfully!")
        except Exception as e:
            self.logger.error(f"❌ Project initialization failed: {e}")
            sys.exit(1)

    def refresh_project(self, args) -> None:
        """Refresh project modules."""
        from cores.modules_controller_core.modules_controller import ModulesController
        controller = ModulesController()
        if args.module:
            self.logger.info(f"Refreshing module: {args.module}")
            module = controller.get_module_by_name(args.module)
            if module:
                controller.run_module_refresh_script(module)
                self.logger.info(f"✅ Module {args.module} refreshed!")
            else:
                self.logger.error(f"❌ Module {args.module} not found.")
                sys.exit(1)
        else:
            self.logger.info("Refreshing all modules...")
            report = controller.list_all_modules()
            for module in report.modules:
                if module.has_refresh_script():
                    controller.run_module_refresh_script(module)
            self.logger.info("✅ Project refresh completed!")

    def list_modules(self, args) -> None:
        """List all modules."""
        from cores.modules_controller_core.modules_controller import ModulesController
        controller = ModulesController()
        report = controller.list_all_modules()
        
        print(f"\n📦 Found {len(report.modules)} modules:")
        for module in report.modules:
            status = "⚠️ " if module.issues else "✅"
            print(f"  {status} {module.name} ({module.module_type.name}) - v{module.version}")
            if module.issues:
                for issue in module.issues:
                    print(f"     - {issue.message}")

    def show_module_info(self, args) -> None:
        """Show module info."""
        from cores.modules_controller_core.modules_controller import ModulesController
        controller = ModulesController()
        module = controller.get_module_by_name(args.module)
        
        if not module:
            self.logger.error(f"❌ Module '{args.module}' not found")
            sys.exit(1)

        print(f"\n📦 MODULE INFORMATION: {module.name}")
        print(f"  📁 Path: {module.path}")
        print(f"  📂 Type: {module.module_type.name}")
        print(f"  🏷️  Version: {module.version}")
        print(f"  🔗 Repo URL: {module.repo_url or 'N/A'}")
        
        reqs = ", ".join(module.requirements) if module.requirements else "None"
        print(f"  🧱 Requirements: {reqs}")
        
        print(f"  🔄 Has Refresh Script: {'Yes' if module.has_refresh_script() else 'No'}")
        print(f"  🚀 Has Initializer: {'Yes' if module.has_initializer() else 'No'}")
        
        if module.issues:
            print("  ⚠️  Issues:")
            for issue in module.issues:
                print(f"    - {issue.message}")

    def install_requirements(self, args) -> None:
        """Install requirements."""
        from cores.project_init_core.requirements_installer import RequirementsInstaller
        installer = RequirementsInstaller()
        installer.install_all()

    def update_workspace(self, args) -> None:
        """Update VS Code workspace file."""
        from cores.modules_controller_core.modules_controller import ModulesController, WorkspaceGenerationMode
        
        controller = ModulesController()
        overrides = {}
        
        mode = WorkspaceGenerationMode.DEFAULT
        if args.all:
            mode = WorkspaceGenerationMode.INCLUDE_ALL
        elif args.ignore_overrides:
            mode = WorkspaceGenerationMode.IGNORE_OVERRIDES

        if args.module:
            module = controller.get_module_by_name(args.module)
            if not module:
                self.logger.error(f"❌ Module '{args.module}' not found")
                sys.exit(1)
            
            # Determine current visibility based on mode to toggle it
            current_visibility = False
            if mode == WorkspaceGenerationMode.INCLUDE_ALL:
                current_visibility = True
            elif mode == WorkspaceGenerationMode.IGNORE_OVERRIDES:
                current_visibility = module.module_type.shows_in_workspace
            else:
                current_visibility = module.shows_in_workspace
                if current_visibility is None:
                    current_visibility = module.module_type.shows_in_workspace
            
            new_visibility = not current_visibility
            overrides[module.name] = new_visibility
            self.logger.info(f"Temporarily toggling workspace visibility for {module.name} to {new_visibility}")

        path = controller.generate_workspace_file(mode=mode, overrides=overrides)
        self.logger.info(f"✅ Workspace file updated at: {path}")


def module_completer(prefix, parsed_args, **kwargs):
    """Autocomplete module names with type grouping."""
    # Suppress logging to prevent corrupting shell completion output
    os.environ["ADHD_LOG_LEVEL"] = "CRITICAL"
    try:
        from cores.modules_controller_core.modules_controller import ModulesController
        controller = ModulesController()
        report = controller.list_all_modules()
        
        # Return modules in 'type/name' format for better organization
        # e.g. 'managers/config_manager', 'cores/project_init_core'
        options = []
        for m in report.modules:
            # Use plural name for grouping (e.g. 'managers', 'cores')
            type_name = m.module_type.plural_name.lower()
            option = f"{type_name}/{m.name}"
            options.append(option)
            
        return [o for o in options if o.startswith(prefix)]
    except Exception:
        return []


def setup_parser() -> argparse.ArgumentParser:
    """Configure and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="ADHD Framework CLI - AI-Driven High-speed Development Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    subparsers.add_parser('create-project', aliases=['cp'], help='Create a new ADHD project')
    subparsers.add_parser('create-module', aliases=['cm'], help='Create a new module')
    subparsers.add_parser('init', aliases=['i'], help='Initialize project modules')
    
    refresh_parser = subparsers.add_parser('refresh', aliases=['r'], help='Refresh project modules')
    refresh_arg = refresh_parser.add_argument('--module', '-m', help='Refresh specific module by name')
    if argcomplete:
        refresh_arg.completer = module_completer

    subparsers.add_parser('list', aliases=['ls'], help='List all discovered modules')
    
    info_parser = subparsers.add_parser('info', aliases=['in'], help='Show detailed module information')
    info_arg = info_parser.add_argument('--module', '-m', required=True, help='Module name to show information for')
    if argcomplete:
        info_arg.completer = module_completer

    subparsers.add_parser('req', aliases=['rq'], help='Install requirements from all requirements.txt files')
    
    workspace_parser = subparsers.add_parser('workspace', aliases=['ws'], help='Update VS Code workspace file')
    workspace_parser.add_argument('--all', action='store_true', help='Include all modules regardless of settings')
    workspace_parser.add_argument('--ignore-overrides', action='store_true', help='Ignore module-level overrides')
    workspace_arg = workspace_parser.add_argument('--module', '-m', help='Toggle workspace visibility for a specific module')
    if argcomplete:
        workspace_arg.completer = module_completer

    if argcomplete:
        argcomplete.autocomplete(parser)
        
    return parser


if __name__ == "__main__":
    # Ensure environment is ready before anything else
    bootstrap()

    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
    else:
        framework = ADHDFramework()
        framework.run(args)
