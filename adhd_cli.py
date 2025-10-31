#!/usr/bin/env python3
"""
ADHD CLI - Command Line Interface for AI-Driven High-speed Development Framework

This CLI provides easy access to the ADHD framework's core functionality including
project initialization, module management, and project refresh operations.
"""
# Add the current directory to Python path to allow imports
import argparse
import subprocess
import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def import_libs():
    global ProjectInitializer, ModulesRefresher, refresh_specific_module, get_modules_controller, upgrade_framework, find_and_install_requirements

    from framework import (
        ProjectInitializer,
        ModulesRefresher,
        refresh_specific_module,
        get_modules_controller
    )
    from framework.install_requirements import find_and_install_requirements
    from framework.upgrade import upgrade_framework

try:
    import_libs()
except ImportError as e:    
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        print(f"📦 Installing python requirements from {requirements_file}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                    check=True)
    import_libs()


def init_project(args):
    """Initialize a new ADHD project."""
    print("🚀 Initializing ADHD project...")
    
    # Handle force flag with confirmation
    force_update = False
    if args.force:
        print("\n⚠️  WARNING: Force mode will update ALL modules regardless of version!")
        print("   This will overwrite existing modules even if they are newer.")
        response = input("   Are you sure you want to continue? (yes/no): ")
        if response.lower() in ['yes', 'y']:
            force_update = True
            print("✅ Force mode confirmed.")
        else:
            print("❌ Operation cancelled.")
            return
    
    yaml_file = args.config if args.config else "init.yaml"
    
    try:            
        initializer = ProjectInitializer(yaml_file=yaml_file, force_update=force_update)
        print("✅ Project initialization completed successfully!")
    except Exception as e:
        print(f"❌ Project initialization failed: {str(e)}")
        sys.exit(1)


def refresh_project(args):
    """Refresh the project modules."""
    if args.module:
        print(f"🔄 Refreshing specific module: {args.module}")
        refresh_specific_module(args.module)
    else:
        print("🔄 Refreshing all project modules...")
        try:
            refresher = ModulesRefresher()
            refresher.refresh_all_modules()
            print("✅ Project refresh completed!")
        except Exception as e:
            print(f"❌ Project refresh failed: {str(e)}")
            sys.exit(1)


def list_modules(args):
    """List all discovered modules and their information."""
    try:
        controller = get_modules_controller()
        controller.list_modules()
    except Exception as e:
        print(f"❌ Failed to list modules: {str(e)}")
        sys.exit(1)


def show_module_info(args):
    """Show detailed information about a specific module."""
    if not args.module:
        print("❌ Module name is required. Use --module MODULE_NAME")
        sys.exit(1)
    
    try:
        controller = get_modules_controller()
        all_modules = controller.get_all_modules()
        
        # Find the module
        found_module = None
        found_path = None
        for path, module_info in all_modules.items():
            if module_info.name == args.module:
                found_module = module_info
                found_path = path
                break
        
        if not found_module:
            print(f"❌ Module '{args.module}' not found")
            print("Available modules:")
            for path, module_info in all_modules.items():
                print(f"  • {module_info.name}")
            sys.exit(1)
        
        # Display detailed module information using table formatter
        from framework.cli_format import TableFormatter, TableRow
        
        formatter = TableFormatter()
        rows = [
            TableRow("📁", "Path", found_path),
            TableRow("📂", "Type", found_module.type or 'Not specified'),
            TableRow("🏷️", "Version", found_module.version),
            TableRow("📃", "Description", found_module.description or 'No description available')
        ]
        
        if found_module.folder_path:
            rows.append(TableRow("🎯", "Target Path", found_module.folder_path))
        
        if found_module.requirements:
            req_text = ", ".join(found_module.requirements)
            if len(req_text) > 50:  # Truncate if too long
                req_text = req_text[:47] + "..."
            rows.append(TableRow("🔗", "Requirements", req_text))
        
        # Show features
        features = found_module.features
        if features:
            features_text = ", ".join(features)
            rows.append(TableRow("🔧", "Features", features_text))
        else:
            rows.append(TableRow("🔧", "Features", "None"))
        
        table = formatter.create_info_table(rows, f"📦 MODULE INFORMATION: {found_module.name}")
        print(f"\n{table}")
        
    except Exception as e:
        print(f"❌ Failed to get module information: {str(e)}")
        sys.exit(1)


def upgrade_framework_cmd(args):
    """Upgrade the framework from the self-template repository."""
    print("🚀 Upgrading ADHD Framework...")
    
    # Handle no-backup flag
    create_backup = not args.no_backup
    
    if not create_backup:
        print("\n⚠️  WARNING: No backup will be created!")
        print("   Your current framework and CLI files will be overwritten.")
        response = input("   Are you sure you want to continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("❌ Upgrade cancelled.")
            return
    
    yaml_file = args.config if args.config else "init.yaml"
    
    try:
        success = upgrade_framework(yaml_file, create_backup)
        if success:
            print("✅ Framework upgrade completed successfully!")
        else:
            print("❌ Framework upgrade failed.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Framework upgrade failed: {str(e)}")
        sys.exit(1)


def install_requirements(args):
    """Install requirements from all requirements.txt files in the project."""
    print("📦 Installing requirements from all requirements.txt files...")
    
    try:
        success = find_and_install_requirements()
        if success:
            print("✅ Requirements installation completed successfully!")
        else:
            print("❌ Some requirements failed to install.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Requirements installation failed: {str(e)}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ADHD Framework CLI - AI-Driven High-speed Development Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s init                    # Initialize project with default init.yaml
  %(prog)s init --config my.yaml  # Initialize with custom config file
  %(prog)s init --force            # Force update all modules (with confirmation)
  %(prog)s refresh                 # Refresh all modules
  %(prog)s refresh --module logger # Refresh specific module
  %(prog)s list                    # List all modules
  %(prog)s info --module logger    # Show info about specific module
  %(prog)s req                      # Install all requirements.txt files in project
  %(prog)s upgrade                 # Upgrade framework from self-template repository
  %(prog)s upgrade --no-backup     # Upgrade without creating backup
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new ADHD project')
    init_parser.add_argument('--config', '-c', 
                           help='Path to YAML configuration file (default: init.yaml)')
    init_parser.add_argument('--force', '-f', action='store_true',
                           help='Force update all modules regardless of version (requires confirmation)')
    init_parser.set_defaults(func=init_project)
    
    # Refresh command
    refresh_parser = subparsers.add_parser('refresh', help='Refresh project modules')
    refresh_parser.add_argument('--module', '-m', 
                               help='Refresh specific module by name')
    refresh_parser.set_defaults(func=refresh_project)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all discovered modules')
    list_parser.set_defaults(func=list_modules)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show detailed module information')
    info_parser.add_argument('--module', '-m', required=True,
                            help='Module name to show information for')
    info_parser.set_defaults(func=show_module_info)
    
    # Install command
    install_parser = subparsers.add_parser('req', help='Install requirements from all requirements.txt files')
    install_parser.set_defaults(func=install_requirements)
    
    # Upgrade command
    upgrade_parser = subparsers.add_parser('upgrade', help='Upgrade framework from self-template repository')
    upgrade_parser.add_argument('--config', '-c', 
                              help='Path to YAML configuration file (default: init.yaml)')
    upgrade_parser.add_argument('--no-backup', action='store_true',
                              help='Skip creating backup before upgrade (requires confirmation)')
    upgrade_parser.set_defaults(func=upgrade_framework_cmd)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Call the appropriate function
    args.func(args)


if __name__ == "__main__":
    main()
