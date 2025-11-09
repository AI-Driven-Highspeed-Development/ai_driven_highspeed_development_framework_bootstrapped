"""
Framework Upgrade Module for ADHD Framework

This module handles upgrading the framework and CLI from the self-template repository.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Optional
from .cli_format import TableFormatter, TableRow, StaticPrintout
from .yaml_util import YamlUtil, YamlFile


class FrameworkUpgrader:
    """Handles upgrading the framework from the self-template repository."""
    
    def __init__(self, init_yaml_path: str = "init.yaml"):
        self.init_yaml_path = init_yaml_path
        self.temp_dir = "temp_upgrade"
        self.current_dir = Path.cwd()
        self.self_template_repo = None
        self._load_yaml()
    
    def _load_yaml(self):
        """Load configuration from init.yaml to get template_repo."""
        yaml_file = YamlUtil.read_yaml(self.init_yaml_path)
        self.self_template_repo = yaml_file.get('template_repo')

        if not isinstance(self.self_template_repo, str):
            raise ValueError("Invalid 'template_repo' format in init.yaml")
    
    def _clone_template_repo(self) -> bool:
        """Clone the self-template repository to the temp directory."""
        print(f"🔄 Cloning template repository from {self.self_template_repo}...")
        
        try:
            # Remove existing temp directory if it exists
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            
            # Clone the repository
            result = subprocess.run(
                ['git', 'clone', self.self_template_repo, self.temp_dir],
                capture_output=True,
                text=True,
                check=True
            )
            
            print(f"✅ Successfully cloned template repository")
            return True
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else "Unknown error"
            print(f"❌ Failed to clone repository: {error_msg}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during clone: {str(e)}")
            return False
    
    def _backup_current_files(self) -> bool:
        """Create backups of current framework and CLI files."""
        print("💾 Creating backups of current files...")
        
        try:
            backup_dir = Path(".backup_" + str(int(os.path.getmtime("framework"))))
            backup_dir.mkdir(exist_ok=True)
            
            # Backup framework directory
            if os.path.exists("framework"):
                shutil.copytree("framework", backup_dir / "framework", dirs_exist_ok=True)
                print(f"   📁 Framework backed up to {backup_dir}/framework")
            
            # Backup adhd_cli.py
            if os.path.exists("adhd_cli.py"):
                shutil.copy2("adhd_cli.py", backup_dir / "adhd_cli.py")
                print(f"   📄 CLI backed up to {backup_dir}/adhd_cli.py")
            
            # Backup .github/copilot-instructions.md if present
            copilot_src = Path(".github") / "copilot-instructions.md"
            if copilot_src.exists():
                (backup_dir / ".github").mkdir(parents=True, exist_ok=True)
                shutil.copy2(copilot_src, backup_dir / ".github" / "copilot-instructions.md")
                print(f"   📄 Copilot instructions backed up to {backup_dir}/.github/copilot-instructions.md")
            
            print(f"✅ Backup created in {backup_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create backup: {str(e)}")
            return False
    
    def _upgrade_framework(self) -> bool:
        """Replace the framework directory with the new one."""
        return self._upgrade_path(
            source_rel=Path("framework"),
            target=Path("framework"),
            is_dir=True,
            human_name="Framework directory",
        )
    
    def _upgrade_cli(self) -> bool:
        """Replace the adhd_cli.py file with the new one."""
        return self._upgrade_path(
            source_rel=Path("adhd_cli.py"),
            target=Path("adhd_cli.py"),
            is_dir=False,
            human_name="CLI file",
        )
    
    def _upgrade_copilot_instructions(self) -> bool:
        """Replace the Copilot instructions file and .github/instructions directory."""
        copilot_ok = self._upgrade_path(
            source_rel=Path(".github") / "copilot-instructions.md",
            target=Path(".github") / "copilot-instructions.md",
            is_dir=False,
            human_name="Copilot instructions",
        )

        instructions_ok = self._upgrade_path(
            source_rel=Path(".github") / "instructions",
            target=Path(".github") / "instructions",
            is_dir=True,
            human_name=".github instructions directory",
        )

        return copilot_ok and instructions_ok

    def _upgrade_path(self, source_rel: Path, target: Path, is_dir: bool, human_name: str) -> bool:
        """Generic upgrade helper to replace a file or directory from the template clone.

        Args:
            source_rel: Path relative to temp clone root (self.temp_dir)
            target: Absolute or project-relative path to replace
            is_dir: Whether the path is a directory
            human_name: Human-readable label for logs
        """
        print(f"🔄 Upgrading {human_name}...")
        try:
            source = Path(self.temp_dir) / source_rel
            if not source.exists():
                print(f"❌ {human_name} not found in cloned repository")
                return False

            if is_dir:
                # Replace directory
                if target.exists():
                    shutil.rmtree(target)
                    print(f"   🗑️  Removed old {human_name.lower()}")
                shutil.copytree(source, target)
                print(f"   📁 Copied new {human_name.lower()}")
            else:
                # Replace file
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    target.unlink()
                    print(f"   🗑️  Removed old {human_name.lower()}")
                shutil.copy2(source, target)
                print(f"   📄 Copied new {human_name.lower()}")

            print(f"✅ {human_name} upgraded successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to upgrade {human_name}: {str(e)}")
            return False
    
    def _cleanup_temp_dir(self):
        """Remove the temporary directory."""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                print("🧹 Cleaned up temporary files")
        except Exception as e:
            print(f"⚠️  Warning: Failed to cleanup temp directory: {str(e)}")
    
    def _display_upgrade_summary(self, success: bool):
        """Display a summary of the upgrade process using StaticPrintout."""
        StaticPrintout.upgrade_summary_header()
        
        if success:
            StaticPrintout.upgrade_success_message()
        else:
            StaticPrintout.upgrade_failure_message()
    
    def upgrade_framework(self, create_backup: bool = True) -> bool:
        """
        Main method to upgrade the framework.
        
        Args:
            create_backup: Whether to create backups before upgrading
            
        Returns:
            bool: True if upgrade was successful, False otherwise
        """
        StaticPrintout.framework_upgrade_header()
        
        try:
            # Display current configuration
            formatter = TableFormatter()
            formatter.set_title("🔧 UPGRADE CONFIGURATION")
            formatter.add_row(TableRow(f"📁 Current Directory: {str(self.current_dir)}"))
            formatter.add_row(TableRow(f"🌐 Template Repository: {self.self_template_repo}"))
            formatter.add_row(TableRow(f"📂 Temp Directory: {self.temp_dir}"))
            formatter.add_row(TableRow(f"💾 Create Backup: {'Yes' if create_backup else 'No'}"))
            
            print(f"\n{formatter.render('normal', 70)}")
            
            # Step 1: Clone template repository
            if not self._clone_template_repo():
                self._display_upgrade_summary(False)
                return False
            
            # Step 2: Create backup (optional)
            if create_backup:
                if not self._backup_current_files():
                    print("⚠️  Backup failed, but continuing with upgrade...")
            
            # Step 3: Update framework directory
            if not self._upgrade_framework():
                self._display_upgrade_summary(False)
                return False
            
            # Step 4: Update CLI file
            if not self._upgrade_cli():
                self._display_upgrade_summary(False)
                return False
            
            # Step 5: Update Copilot instructions file
            if not self._upgrade_copilot_instructions():
                self._display_upgrade_summary(False)
                return False
            
            # Step 5: Cleanup
            self._cleanup_temp_dir()
            
            # Step 6: Display summary
            self._display_upgrade_summary(True)
            return True
            
        except Exception as e:
            print(f"❌ Unexpected error during upgrade: {str(e)}")
            self._cleanup_temp_dir()
            self._display_upgrade_summary(False)
            return False


def upgrade_framework(init_yaml_path: str = "init.yaml", create_backup: bool = True) -> bool:
    """
    Convenience function to upgrade the framework.
    
    Args:
        init_yaml_path: Path to the init.yaml file
        create_backup: Whether to create backups before upgrading
        
    Returns:
        bool: True if upgrade was successful, False otherwise
    """
    upgrader = FrameworkUpgrader(init_yaml_path)
    return upgrader.upgrade_framework(create_backup)


if __name__ == "__main__":
    # For testing purposes
    success = upgrade_framework()
    sys.exit(0 if success else 1)
