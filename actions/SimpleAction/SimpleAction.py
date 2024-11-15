# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os
import json
from loguru import logger as log
# import websockets

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class SimpleAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)

    def on_key_down(self) -> None:
        vscommand = {"id":"StreamControllerConnected"}
        self.prepare_command(vscommand)

    def on_key_up(self) -> None:
        print("Key up")

    def prepare_command(self, vscommand):
        host = "127.0.0.1"
        port = "48969"
        ws_uri = "ws://{host}:{port}".format(host=host, port=port)
        vscommand = json.dumps(vscommand)

        try:
            return self.plugin_base.backend.queue_command(ws_uri, vscommand)
        except Exception as e:
            log.error(e)
            return False