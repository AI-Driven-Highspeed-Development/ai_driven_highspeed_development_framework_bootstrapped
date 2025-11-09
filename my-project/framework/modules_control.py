import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from .yaml_util import YamlUtil, YamlFile

@dataclass
class ModuleInfo:
    """Data class to store module information"""
    path: str
    name: str
    has_init: bool = False
    has_refresh: bool = False
    has_config: bool = False
    folder_path: str = ""
    type: str = ""
    version: str = "0.0.1"
    description: str = ""
    requirements: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization to set name from path if not provided"""
        if not self.name:
            self.name = os.path.basename(self.path)
    
    @property
    def features(self) -> List[str]:
        """Get list of available features for this module"""
        features = []
        if self.has_init:
            features.append("✅ Init")
        if self.has_refresh:
            features.append("🔄 Refresh")
        if self.has_config:
            features.append("⚙️ Config")
        return features


class ModulesController:
    """Controller for managing and providing information about project modules."""
    
    def __init__(self):
        self.base_dirs = ["managers", "utils", "plugins", "mcps", "cores"]
        self.modules_info: Dict[str, ModuleInfo] = {}
        self._scan_modules()
    
    def _scan_modules(self):
        """Scan for modules in the base directories."""
        # print("Scanning for modules...")  # Uncomment for debugging
        
        for base_dir in self.base_dirs:
            if os.path.exists(base_dir):
                self._scan_directory(base_dir)
        
        # print(f"Found {len(self.modules_info)} modules")  # Uncomment for debugging
    
    def _scan_directory(self, directory: str):
        """Scan a specific directory for modules."""
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path) and not item.startswith('_') and not item.startswith('__') and not item.startswith('.'):
                module_info = ModulesController.get_module_info_from_path(item_path)
                if module_info:
                    self.modules_info[item_path] = module_info

    
    @staticmethod
    def get_module_info_from_path(module_path: str) -> Optional[ModuleInfo]:
        """Get information about a specific module without scanning the entire project."""
        if not os.path.exists(module_path):
            return None
        # Create basic module info
        module_info = ModuleInfo(
            path=module_path,
            name=os.path.basename(module_path),
            has_init=os.path.exists(os.path.join(module_path, "__init__.py")),
            has_refresh=os.path.exists(os.path.join(module_path, "refresh.py")),
            has_config=os.path.exists(os.path.join(module_path, "init.yaml")),
        )
        
        # Try to read init.yaml for additional information
        init_yaml_path = os.path.join(module_path, "init.yaml")
        if os.path.exists(init_yaml_path):
            yaml_file = YamlUtil.read_yaml(init_yaml_path)
            if yaml_file:
                # Update module info with YAML data
                module_info.folder_path = yaml_file.get("folder_path", "")
                module_info.type = yaml_file.get("type", "")
                module_info.version = yaml_file.get("version", "0.0.1")
                module_info.description = yaml_file.get("description", "")
                
                # Handle requirements (can be list or single string)
                requirements = yaml_file.get("requirements", [])
                module_info.requirements = requirements if isinstance(requirements, list) else [requirements]
        
        return module_info
    
    def get_all_modules(self) -> Dict[str, ModuleInfo]:
        """Get information about all discovered modules as ModuleInfo objects."""
        return self.modules_info
    
    def get_modules_with_refresh(self) -> List[str]:
        """Get paths of all modules that have refresh.py files."""
        return [path for path, module in self.modules_info.items() if module.has_refresh]
    
    def get_module_info_object(self, module_path: str) -> Optional[ModuleInfo]:
        """Get information about a specific module as ModuleInfo object."""
        return self.modules_info.get(module_path)
    
    def list_modules(self):
        """Print a formatted list of all modules."""
        if not self.modules_info:
            print("No modules found.")
            return
        
        print(f"\nFound {len(self.modules_info)} modules:")
        print("-" * 80)
        
        for path, module in self.modules_info.items():
            print(f"📁 {module.name} ({module.path})")
            
            if module.type:
                print(f"   📂 Type: {module.type}")
            if module.version:
                print(f"   🏷️ Version: {module.version}")
            if module.description:
                print(f"   📃 {module.description}")
            if module.folder_path:
                print(f"   🎯 Target Path: {module.folder_path}")
            
            # Show requirements if they exist
            if module.requirements:
                print(f"   🔗 Requirements:")
                for req in module.requirements:
                    print(f"      • {req}")
            
            # Show features
            if module.features:
                print(f"   🔧 Features: {', '.join(module.features)}")
            print()

def get_modules_controller() -> ModulesController:
    """Get the modules controller instance."""
    return ModulesController()

if __name__ == "__main__":
    controller = ModulesController()
    controller.list_modules()
