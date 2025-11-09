from dataclasses import dataclass
from typing import List, Optional
from wcwidth import wcswidth
import os

line_styles = {
    "normal": {"┌": "┌", "─": "─", "┐": "┐", "│": "│", "├": "├", "┤": "┤", "└": "└", "┘": "┘"},
    "bold": {"┌": "┏", "─": "━", "┐": "┓", "│": "┃", "├": "┣", "┤": "┫", "└": "┗", "┘": "┛"},
    "double": {"┌": "╔", "─": "═", "┐": "╗", "│": "║", "├": "╠", "┤": "╣", "└": "╚", "┘": "╝"},
    "dotted": {"┌": "┌", "─": "╌", "┐": "┐", "│": "╎", "├": "┤", "┤": "┤", "└": "└", "┘": "┘"},
    "curly": {"┌": "╭", "─": "─", "┐": "╮", "│": "│", "├": "├", "┤": "┤", "└": "╰", "┘": "╯"}
}

@dataclass
class TableRow:
    """Data class to represent a row in a table."""
    row: str = ""
    padding_adjust: int = 0

    def get_raw_len(self) -> int:
        """Get the raw length of the row without any formatting."""
        return len(self.row)

    def get_wcswidth(self) -> int:
        """Get the width of the row considering wide characters."""
        return wcswidth(self.row)

    def get_padding_len(self, table_width: int) -> int:
        """Calculate the padding length for the row based on the table width."""
        width = self.get_wcswidth()
        if self.get_wcswidth() < self.get_raw_len():
            width = self.get_wcswidth() + (self.get_raw_len() - self.get_wcswidth()) + 2 + self.padding_adjust
        return table_width - width

    def get_left_justified_row(self, table_width: int) -> str:
        """Get the row left-justified within the specified table width."""
        padding = self.get_padding_len(table_width - 2)  # Subtract 2 for the side borders
        return f"{self.row}{' '* padding}"
    
    def get_centered_row(self, table_width: int) -> str:
        """Get the row centered within the specified table width."""
        padding = self.get_padding_len(table_width - 2)  # Subtract 2 for the side borders
        left_padding = padding // 2
        right_padding = padding - left_padding
        return f"{' ' * left_padding}{self.row}{' ' * right_padding}"

class TableFormatter:
    """A class to format data into a table-like structure."""

    def __init__(self):
        self.table_row: List[TableRow] = []
        self.title: TableRow = TableRow()

    def add_row(self, row: TableRow, pos: Optional[int] = None):
        """Add a row to the table."""
        if pos is not None:
            self.table_row.insert(pos, row)
        else:
            self.table_row.append(row)
    
    def set_title(self, title: str):
        """Set the title of the table."""
        self.title = TableRow(title)
        
    def render(self, line_style_name: str = "normal", pref_table_width: int = 80) -> str:
        """Render the table as a string."""
        if line_style_name not in line_styles:
            raise ValueError(f"Invalid style: {line_style_name}. Available styles: {', '.join(line_styles.keys())}")
        
        pref_table_width = max(pref_table_width, 20)  # Ensure a minimum width
        pref_table_width = max(pref_table_width, self.title.get_wcswidth() + 8)  # Ensure title fits
        pref_table_width = max(pref_table_width, max((row.get_wcswidth() + 8) for row in self.table_row))  # Ensure rows fit

        lines = []
        style = line_styles[line_style_name]
        
        lines.append(f"{style['┌']}{style['─'] * (pref_table_width - 2)}{style['┐']}")
        
        # Title
        if self.title:
            title_line = f"{style['│']}{self.title.get_centered_row(pref_table_width)}{style['│']}"
            lines.append(title_line)
            lines.append(f"{style['├']}{style['─'] * (pref_table_width - 2)}{style['┤']}")

        # Rows
        for table_row in self.table_row:
            lines.append(f"{style['│']}{table_row.get_left_justified_row(pref_table_width)}{style['│']}")

        # Footer
        footer_line = f"{style['└']}{style['─'] * (pref_table_width - 2)}{style['┘']}"
        lines.append(footer_line)
        
        return "\n".join(lines)
    
class StaticPrintout:
    """
    Print out static text that used by the CLI.
    Zero logic included, just static text.
    """
    
    @staticmethod
    def project_init_header():
        """Print the project initialization header."""
        print(f"\n{'='*60}")
        print("🚀 ADHD PROJECT INITIALIZATION")
        print(f"{'='*60}")
    
    @staticmethod
    def project_init_complete():
        """Print the project initialization completion message."""
        print(f"\n{'='*60}")
        print("🎉 PROJECT INITIALIZATION COMPLETE!")
        print(f"{'='*60}")
        print("🎯 Your ADHD project template is ready to use!")
        print("📝 Check the modules above for available functionality.")
        print(f"{'='*60}")
        print("💡 Next steps:")
        print("   • Review the initialized modules")
        print("   • Configure settings as needed")
        print("   • Start building your project!")
        print(f"{'='*60}")
        print("📍 Navigation:")
        print(f"   • If not in project directory: cd '{os.getcwd()}'")
        print("🔄 Re-initialization:")
        print("   • After changing init.yaml: ")
        print("       python adhd_cli.py init")
        print("   • To refresh existing project: ")
        print("       python adhd_cli.py refresh")
        print("   • To list all modules: ")
        print("       python adhd_cli.py list")
        print(f"{'='*60}")
    
    @staticmethod
    def modules_scan_header():
        """Print the modules scanning header."""
        print(f"\n{'='*60}")
        print("🔍 SCANNING MODULES AND CAPABILITIES")
        print(f"{'='*60}")
    
    @staticmethod
    def initialization_summary_header():
        """Print the initialization summary header."""
        print(f"\n{'='*60}")
        print("📊 INITIALIZATION SUMMARY")
        print(f"{'='*60}")
    
    @staticmethod
    def final_module_status_header():
        """Print the final module status header."""
        print(f"\n{'='*60}")
        print("📋 FINAL MODULE STATUS")
        print(f"{'='*60}")
    
    @staticmethod
    def module_placement_header():
        """Print the module placement header."""
        print(f"\n{'='*60}")
        print("📦 MODULE PLACEMENT")
        print(f"{'='*60}")
    
    @staticmethod
    def configuration_loading_header():
        """Print the configuration loading header."""
        print(f"\n{'='*60}")
        print("📄 LOADING CONFIGURATION")
        print(f"{'='*60}")
    
    @staticmethod
    def recursive_cloning_header():
        """Print the recursive cloning header."""
        print(f"\n{'='*60}")
        print("⬇️  RECURSIVE REPOSITORY CLONING")
        print(f"{'='*60}")
    
    @staticmethod
    def recursive_cloning_summary_header():
        """Print the recursive cloning summary header."""
        print(f"\n{'='*60}")
        print("📊 RECURSIVE CLONING SUMMARY")
        print(f"{'='*60}")
    
    @staticmethod
    def dependency_level_header(level: int):
        """Print the dependency level header."""
        print(f"\n{'='*60}")
        print(f"📦 DEPENDENCY LEVEL {level}")
        print(f"{'='*60}")
    
    @staticmethod
    def circular_dependency_warning(cycle_names: List[str], module_name: str):
        """Print circular dependency warning."""
        print(f"\n⚠️  CIRCULAR DEPENDENCY DETECTED!")
        print(f"   🔄 Cycle: {' → '.join(cycle_names)}")
        print(f"   🛑 Breaking cycle at {module_name}")
        print(f"   ℹ️  Will attempt to initialize {module_name} without its dependencies")
    
    @staticmethod
    def framework_upgrade_header():
        """Print the framework upgrade header."""
        print(f"\n{'='*60}")
        print("🚀 FRAMEWORK UPGRADE")
        print(f"{'='*60}")
        print("Upgrading from self-template repository")
        print(f"{'='*60}")
    
    @staticmethod
    def upgrade_summary_header():
        """Print the upgrade summary header."""
        print(f"\n{'='*60}")
        print("📊 UPGRADE SUMMARY")
        print(f"{'='*60}")
    
    @staticmethod
    def upgrade_success_message():
        """Print upgrade success message."""
        print("🎉 Framework upgrade completed successfully!")
        print()
        print("✅ Upgraded components:")
        print("   • Framework directory (framework/)")
        print("   • CLI script (adhd_cli.py)")
        print("   • Copilot instructions (.github/copilot-instructions.md)")
        print("   • Agent instructions directory (.github/instructions/)")
        print()
        print("💡 What's next:")
        print("   • Check for any new dependencies in requirements.txt")
        print("   • Run 'python adhd_cli.py req' to install new requirements")
        print("   • Test your project to ensure everything works")
        print(f"{'='*60}")
    
    @staticmethod
    def upgrade_failure_message():
        """Print upgrade failure message."""
        print("❌ Framework upgrade failed!")
        print()
        print("🔄 Troubleshooting:")
        print("   • Check your internet connection")
        print("   • Verify the self-template-repo URL in init.yaml")
        print("   • Ensure you have git installed and accessible")
        print("   • Check that you have write permissions in this directory")
        print(f"{'='*60}")