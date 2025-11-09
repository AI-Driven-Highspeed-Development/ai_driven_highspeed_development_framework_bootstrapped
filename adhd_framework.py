import sys

from cores.yaml_reading_core.yaml_reading import YamlReadingCore as yaml_reading
from cores.yaml_reading_core.yaml_file import YamlFile

from managers.config_manager import ConfigManager
from utils.logger_util.logger import Logger
from cores.github_api_core.api import GithubApi
from cores.questionary_core.questionary_core import QuestionaryCore
from cores.project_creator_core.project_creation_wizard import run_project_creation_wizard


class ADHDFramework:
    """Main ADHD Framework CLI class"""

    def __init__(self):
        self.logger = Logger(__class__.__name__)
        self.cm = ConfigManager()
        self.config = self.cm.config.main_config
        self.mod_tmpls: YamlFile = yaml_reading.read_yaml(self.config.path.module_templates)
        self.proj_tmpls: YamlFile = yaml_reading.read_yaml(self.config.path.project_templates)
        self.mod_preload_sets: YamlFile = yaml_reading.read_yaml(self.config.path.module_preload_sets)
        self.prompter = QuestionaryCore()

        try:
            self._gh_path = GithubApi.require_gh()
        except RuntimeError as e:
            self.logger.error(f"GitHub CLI setup not complete: {e}")
            sys.exit(1)

    def run(self):
        self.logger.info("Running ADHD Framework...")
        # Enter project creation flow
        self.create_project_proc(self.proj_tmpls, self.mod_preload_sets)

    def create_project_proc(self, proj_tmpls: YamlFile, mod_preload_sets: YamlFile):
        run_project_creation_wizard(
            proj_tmpls,
            mod_preload_sets,
            prompter=self.prompter,
            logger=self.logger,
        )


if __name__ == "__main__":
    framework = ADHDFramework()
    framework.run()
