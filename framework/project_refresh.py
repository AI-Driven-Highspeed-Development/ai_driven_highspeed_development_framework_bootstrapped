import os
import sys
import subprocess
from pathlib import Path
from .modules_control import get_modules_controller

class ModulesRefresher:
    """Handles refreshing all modules by running their refresh.py scripts."""
    
    def __init__(self):
        self.modules_controller = get_modules_controller()
        self.successful_refreshes = 0
        self.failed_refreshes = 0
    
    def refresh_all_modules(self):
        """Find and run all refresh.py files in discovered modules."""
        refresh_modules = self.modules_controller.get_modules_with_refresh()
        
        if not refresh_modules:
            print("No modules with refresh capabilities found.")
            return
        
        print(f"🔄 Starting refresh process for {len(refresh_modules)} modules...\n")
        
        for module_path in refresh_modules:
            self._refresh_module(module_path)
        
        self._print_summary()
    
    def _refresh_module(self, module_path: str):
        """Refresh a specific module by running its refresh.py script."""
        module_info = self.modules_controller.get_module_info_object(module_path)
        module_name = module_info.name if module_info else os.path.basename(module_path)
        refresh_script = os.path.join(module_path, "refresh.py")
        
        print(f"🔄 Refreshing module: {module_name}")
        
        try:
            # Run the refresh script from project root (like init.py does)
            result = subprocess.run(
                [sys.executable, refresh_script],
                capture_output=True,
                text=True,
                check=True
            )
            
            self.successful_refreshes += 1
            print(f"   ✅ {module_name} refreshed successfully")
            
            # Print output if there is any (for debugging)
            if result.stdout.strip():
                print(f"   📝 Output: {result.stdout.strip()}")
            
        except subprocess.CalledProcessError as e:
            self.failed_refreshes += 1
            error_msg = f"Failed to refresh {module_name}: {e.stderr.strip() if e.stderr else str(e)}"
            print(f"   ❌ {error_msg}")
            
        except Exception as e:
            self.failed_refreshes += 1
            error_msg = f"Unexpected error refreshing {module_name}: {str(e)}"
            print(f"   ❌ {error_msg}")
    
    def _print_summary(self):
        """Print a summary of the refresh process."""
        total_modules = self.successful_refreshes + self.failed_refreshes
        
        print("\n" + "="*50)
        print("🔄 REFRESH SUMMARY")
        print("="*50)
        print(f"Total modules processed: {total_modules}")
        print(f"✅ Successful refreshes: {self.successful_refreshes}")
        print(f"❌ Failed refreshes: {self.failed_refreshes}")
        
        if self.failed_refreshes == 0:
            print("🎉 All modules refreshed successfully!")
        else:
            print("⚠️  Some modules failed to refresh. Check output above for details.")

def refresh_specific_module(module_name: str):
    """Refresh a specific module by name."""
    controller = get_modules_controller()
    refresher = ModulesRefresher()
    
    # Find the module
    for path, info in controller.get_all_modules().items():
        if info.name == module_name:
            if info.has_refresh:
                print(f"🔄 Refreshing specific module: {module_name}")
                refresher._refresh_module(path)
                return
            else:
                print(f"❌ Module '{module_name}' does not have refresh capability")
                return
    
    print(f"❌ Module '{module_name}' not found")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Refresh specific module
        module_name = sys.argv[1]
        refresh_specific_module(module_name)
    else:
        # Refresh all modules
        refresher = ModulesRefresher()
        refresher.refresh_all_modules()
