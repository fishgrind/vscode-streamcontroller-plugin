
# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.DeckManagement.InputIdentifier import Input

# Import actions
from .actions.SimpleAction.SimpleAction import SimpleAction

import os
import sys
import json
from loguru import logger as log


sys.path.append(os.path.dirname(__file__))

class VSCode(PluginBase):
    def __init__(self):
        super().__init__()

        # Launch backend
        self.launch_backend(os.path.join(self.PATH, "backend", "backend.py"), os.path.join(self.PATH, "backend", ".venv"), open_in_terminal=True)


        ## Register actions
        self.simple_action_holder = ActionHolder(
            plugin_base = self,
            action_base = SimpleAction,
            action_id = "dev_fishgrind_VSCode::SimpleAction", # Change this to your own plugin id
            action_name = "Test Action",
        )
        self.add_action_holder(self.simple_action_holder)

        # Register plugin
        self.register(
            plugin_name = "VSCode",
            github_repo = "https://github.com/StreamController/PluginTemplate",
            plugin_version = "1.0.0",
            app_version = "1.1.1-alpha"
        )

    def parse_message(self, message):
        host = "127.0.0.1"
        port = "48969"
        ws_uri = "ws://{host}:{port}".format(host=host, port=port)
        message = json.dumps(message)

        try:
            return self.backend.send_message(ws_uri, message)
        except Exception as e:
            log.error(e)
            return False