import sys

from managers.config_manager import ConfigManager
from utils.logger_util.logger import Logger
from cores.github_api_core.api import GithubApi
from cores.questionary_core.questionary_core import QuestionaryCore
from cores.project_creator_core.project_creation_wizard import run_project_creation_wizard
from cores.module_creator_core.module_creation_wizard import run_module_creation_wizard


class ADHDFramework:
    """Main ADHD Framework CLI class"""

    def __init__(self):
        self.logger = Logger(__class__.__name__)
        self.cm = ConfigManager()
        self.config = self.cm.config.main_config
        self.prompter = QuestionaryCore()

        try:
            self._gh_path = GithubApi.require_gh()
        except RuntimeError as e:
            self.logger.error(f"GitHub CLI setup not complete: {e}")
            sys.exit(1)

    def run(self):
        self.logger.info("Running ADHD Framework...")
        # Enter project creation flow
        self.create_project_proc()

    def create_project_proc(self) -> None:
        run_project_creation_wizard(
            prompter=self.prompter,
            logger=self.logger,
        )

    def create_module_proc(self) -> None:
        """Enter the interactive module creation flow with templates."""
        run_module_creation_wizard(
            prompter=self.prompter,
            logger=self.logger,
        )


if __name__ == "__main__":
    framework = ADHDFramework()
    framework.run()
