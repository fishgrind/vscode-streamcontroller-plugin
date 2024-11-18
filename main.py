
# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.DeckManagement.InputIdentifier import Input

# Import actions
from .actions.ChangeLanguage import ChangeLanguage

import os
import sys
import json
from loguru import logger as log


sys.path.append(os.path.dirname(__file__))

class VSCode(PluginBase):
    def __init__(self):
        super().__init__()

        # Launch backend
        self.launch_backend(os.path.join(self.PATH, "backend", "backend.py"), os.path.join(self.PATH, "backend", ".venv"), open_in_terminal=False)


        ## Register actions
        self.changeLanguage_holder = ActionHolder(
            plugin_base = self,
            action_base = ChangeLanguage,
            action_id = "com_fishgrind_vscode::ChangeLanguage",
            action_name = "Change Document Language Mode",
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.changeLanguage_holder)

        # Register plugin
        self.register(
            plugin_name = "VSCode",
            github_repo = "https://github.com/Fishgrind/vscode-streamcontroller-plugin",
            plugin_version = "1.0.0",
            app_version = "1.1.1-alpha"
        )