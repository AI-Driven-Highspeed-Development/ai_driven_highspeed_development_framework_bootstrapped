from typing import List
import os
import sys

# Ensure repository root is on sys.path so `cores/...` imports work when running as a script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cores.yaml_reading_core.yaml_reading import YamlReadingCore as yaml_reading
from cores.yaml_reading_core.yaml_file import YamlFile

from managers.config_manager import ConfigManager
from utils.logger_util.logger import Logger
from cores.project_creator_core.project_creator import ProjectCreator, ProjectParams
from cores.project_creator_core.preload_sets import parse_preload_sets, PreloadSet
from cores.project_creator_core.templates import list_project_templates, TemplateInfo

class ADHDFramework:
    """Main ADHD Framework CLI class"""

    def __init__(self):
        self.logger = Logger(__class__.__name__)
        self.cm = ConfigManager()
        self.config = self.cm.config.main_config
        self.mod_tmpls: YamlFile = yaml_reading.read_yaml(self.config.path.module_templates)
        self.proj_tmpls: YamlFile = yaml_reading.read_yaml(self.config.path.project_templates)
        self.mod_preload_sets: YamlFile = yaml_reading.read_yaml(self.config.path.module_preload_sets)


    def run(self):
        print("Running ADHD Framework...")
        # Enter project creation flow
        self.create_project_proc(self.proj_tmpls, self.mod_preload_sets)

    def _prompt(self, prompt_text: str, default: str | None = None) -> str:
        suffix = f" [{default}]" if default else ""
        val = input(f"{prompt_text}{suffix}: ").strip()
        return val or (default or "")

    def _prompt_select(self, title: str, options: list[str], default_idx: int = 0) -> int:
        print(f"\n{title}")
        for i, opt in enumerate(options):
            print(f"  {i}) {opt}")
        while True:
            raw = input(f"Select [0-{len(options)-1}] (default {default_idx}): ").strip()
            if raw == "":
                return default_idx
            if raw.isdigit():
                idx = int(raw)
                if 0 <= idx < len(options):
                    return idx
            print("Invalid selection. Try again.")

    def create_project_proc(self, proj_tmpls: YamlFile, mod_preload_sets: YamlFile):
        # 1) Ask for project basics
        project_name = self._prompt("Project name", default="my-project")
        module_type = self._prompt("Module type (core/manager/plugin/util/mcp)", default="core")
        dest_path = self._prompt("Destination path", default=f"./{project_name}")

        # 2) Select project template
        templates: list[TemplateInfo] = list_project_templates(proj_tmpls)
        if not templates:
            print("No project templates found in configuration.")
            return
        tmpl_opts = [f"{t.name} — {t.description or t.url}" for t in templates]
        tmpl_idx = self._prompt_select("Select a project template", tmpl_opts, default_idx=0)
        template_url = templates[tmpl_idx].url

        # 3) Select preload set (with 'None' option)
        always_urls, sets = parse_preload_sets(mod_preload_sets)
        set_opts = ["None"] + [f"{s.name} — {s.description}" for s in sets]
        set_idx = self._prompt_select("Select a module preload set", set_opts, default_idx=0)
        selected_urls: list[str] = []
        if set_idx > 0:
            selected_urls = sets[set_idx - 1].urls

        module_urls = list(dict.fromkeys(always_urls + selected_urls))  # de-duplicate, preserve order

        # 4) Create the project
        params = ProjectParams(
            repo_path=dest_path,
            module_urls=module_urls,
            project_name=project_name,
            module_type=module_type,
        )
        creator = ProjectCreator(params)
        try:
            dest = creator.create(template_url)
        except Exception as e:
            print(f"❌ Failed to create project: {e}")
            return

        print(f"✅ Project created at: {dest}")
    
        
        
if __name__ == "__main__":
    framework = ADHDFramework()
    framework.run()
    