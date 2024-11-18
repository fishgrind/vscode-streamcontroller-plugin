# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os
import json

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class OpenFolder(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "vscode.svg")
        self.set_media(media_path=icon_path, size=0.40)

    def on_key_down(self) -> None:
        settings = self.get_settings()
        vscommand = {
            "id": "OpenFolderMessage",
            "data":{
                "path":settings.get("open_folder_path_value").replace('/', '//'),
                "newWindow": True
                }
            }
        self.prepare_command(vscommand)

    def get_config_rows(self) -> list:
        self.open_folder_path = Adw.EntryRow(title="Folder Path")
        self.load_config_defaults()
        self.open_folder_path.connect("notify::text", self.on_open_folder_path_changed)
        return [self.open_folder_path]

    def load_config_defaults(self):
        settings = self.get_settings()
        self.open_folder_path.set_text(settings.get("open_folder_path_value", "")) # Does not accept None

    def on_open_folder_path_changed(self, entry, *args):
        settings = self.get_settings()
        settings["open_folder_path_value"] = entry.get_text()
        self.set_settings(settings)

    def prepare_command(self, vscommand):
        try:
            return self.plugin_base.backend.queue_command(json.dumps(vscommand))
        except Exception as e:
            log.error(e)
            return False