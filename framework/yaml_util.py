"""
YAML Utility Module for ADHD Framework

Provides YamlFile class for loaded YAML data operations and YamlUtil class
for file I/O and utility functions.
"""

import yaml
import os
import re
import urllib.request
from urllib.parse import urlparse
from pathlib import Path
from typing import Dict, Any, Optional, Union, List


class YamlFile:
    """Represents a loaded YAML file with convenient data access methods."""
    
    def __init__(self, data: Dict[str, Any] = None, file_path: Union[str, Path] = None):
        self.data = data or {}
        self.file_path = file_path
    
    def exists_key(self, key_path: str) -> bool:
        """Check if a key exists using dot notation."""
        try:
            keys = key_path.split('.')
            value = self.data
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return False
            return True
        except (AttributeError, TypeError):
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        try:
            keys = key_path.split('.')
            value = self.data
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            return value
        except (AttributeError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        try:
            keys = key_path.split('.')
            current = self.data
            
            # Navigate to the parent of the target key
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                elif not isinstance(current[key], dict):
                    current[key] = {}
                current = current[key]
            
            # Set the final value
            current[keys[-1]] = value
        except (AttributeError, TypeError, IndexError):
            pass
    
    def has_required_keys(self, required_keys: List[str]) -> bool:
        return all(self.exists_key(key) for key in required_keys)
    
    def has_value(self, key_path: str) -> bool:
        """Check if a value exists at the given key path (not None)."""
        return self.get(key_path) is not None

    def save(self, file_path: Union[str, Path] = None) -> bool:
        target_path = file_path or self.file_path
        if not target_path:
            return False
        
        try:
            file_path = Path(file_path)
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.safe_dump(self.data, file, default_flow_style=False,
                               allow_unicode=True, sort_keys=False)
            return True
        except (yaml.YAMLError, IOError, UnicodeEncodeError):
            return False

    def to_dict(self) -> Dict[str, Any]:
        return self.data.copy()
    
    def get_value(self, key_path: str, default: Any = None) -> Any:
        """Alias for get() method for consistency with YamlUtil."""
        return self.get(key_path, default)
    
    def validate_structure(self, required_keys: List[str]) -> bool:
        """Validate that the YAML data contains all required keys with non-None values."""
        if not isinstance(self.data, dict):
            return False
            
        return all(self.has_value(key_path) for key_path in required_keys)
    
    def merge(self, override_data: Dict[str, Any]) -> 'YamlFile':
        """Merge this YAML data with override data."""
        try:
            result = self.data.copy()
            for key, value in override_data.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._merge_dict_recursive(result[key], value)
                else:
                    result[key] = value
            return YamlFile(result, self.file_path)
        except (AttributeError, TypeError):
            return YamlFile(self.data.copy(), self.file_path)
    
    def _merge_dict_recursive(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge two dictionaries."""
        try:
            result = base.copy()
            for key, value in override.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = self._merge_dict_recursive(result[key], value)
                else:
                    result[key] = value
            return result
        except (AttributeError, TypeError):
            return base


class YamlUtil:
    """Utility class for YAML file I/O and common operations."""
    
    @staticmethod
    def read_yaml(file_path: Union[str, Path]) -> Optional['YamlFile']:
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
                
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file) or {}
                return YamlFile(data, file_path)
        except (yaml.YAMLError, IOError, UnicodeDecodeError):
            raise FileNotFoundError(f"Configuration file '{file_path}' not found or invalid")
    
    @staticmethod
    def read_yaml_from_url(url: str) -> Optional['YamlFile']:
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read().decode('utf-8')
                data = yaml.safe_load(content) or {}
                return YamlFile(data, url)
        except (urllib.error.URLError, yaml.YAMLError, UnicodeDecodeError):
            return None
    
    @staticmethod
    def is_url(item: str) -> bool:
        try:
            result = urlparse(item)
            return all([result.scheme, result.netloc])
        except (ValueError, AttributeError):
            return False
    
    @staticmethod
    def get_repo_full_name(url: str) -> Optional[str]:
        """Extract owner/repo from GitHub URL."""
        try:
            # Handle both HTTPS and SSH GitHub URLs
            patterns = [
                r'github\.com[:/]([^/]+/[^/]+?)(?:\.git)?/?$',
                r'github\.com/([^/]+/[^/]+?)(?:/.*)?$'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    repo_full_name = match.group(1)
                    # Remove .git suffix if present
                    if repo_full_name.endswith('.git'):
                        repo_full_name = repo_full_name[:-4]
                    return repo_full_name
            return None
        except (AttributeError, TypeError):
            return None
    
    @staticmethod
    def get_repo_name(url: str) -> Optional[str]:
        """Extract just the repo name (without owner) from GitHub URL."""
        full_name = YamlUtil.get_repo_full_name(url)
        if full_name and '/' in full_name:
            return full_name.split('/')[-1]
        return None
        
    @staticmethod
    def construct_github_raw_url(repo_url: str, path: str, branch: str = "main") -> str:
        """Convert GitHub repo URL to raw.githubusercontent.com URL for file access."""
        repo_full_name = YamlUtil.get_repo_full_name(repo_url)
        if repo_full_name:
            # Remove leading slash from path if present
            clean_path = path.lstrip('/')
            return f"https://raw.githubusercontent.com/{repo_full_name}/{branch}/{clean_path}"
        return ""

    @staticmethod
    def load_init_yaml(file_path: str = "init.yaml", defaults_schema: Dict[str, Any] = None) -> Optional['YamlFile']:
        """Load and validate an init.yaml file with default values."""
        yaml_file = YamlUtil.read_yaml(file_path)
        if yaml_file is None:
            return None

        for key, default_value in (defaults_schema or {}).items():
            if not yaml_file.exists_key(key):
                yaml_file.set(key, default_value)
        
        return yaml_file

    @staticmethod
    def save_init_yaml(data: Dict[str, Any], file_path: str = "init.yaml", required_keys: List[str] = None) -> bool:
        """Save data to an init.yaml file with validation."""
        # Create YamlFile object and validate
        yaml_file = YamlFile(data)

        if not yaml_file.has_required_keys(required_keys):
            missing_keys = [key for key in required_keys if not yaml_file.exists_key(key)]
            print(f"Warning: Missing required keys in YAML data: {missing_keys}")
        
        return YamlUtil.save_yaml(data, file_path)
