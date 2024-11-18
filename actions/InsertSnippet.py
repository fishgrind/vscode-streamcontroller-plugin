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

class InsertSnippet(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "vscode.svg")
        self.set_media(media_path=icon_path, size=0.40)

    def on_key_down(self) -> None:
        settings = self.get_settings()
        vscommand = {
            "id": "InsertSnippetMessage",
            "data":{
                "name":settings.get("snippet_id_value")
                }
            }
        self.prepare_command(vscommand)

    def get_config_rows(self) -> list:
        self.snippet_id = Adw.EntryRow(title="Code Snippet Name")
        self.load_config_defaults()
        self.snippet_id.connect("notify::text", self.on_snippet_id_changed)
        return [self.snippet_id]

    def load_config_defaults(self):
        settings = self.get_settings()
        self.snippet_id.set_text(settings.get("snippet_id_value", "")) # Does not accept None

    def on_snippet_id_changed(self, entry, *args):
        settings = self.get_settings()
        settings["snippet_id_value"] = entry.get_text()
        self.set_settings(settings)

    def prepare_command(self, vscommand):
        try:
            return self.plugin_base.backend.queue_command(json.dumps(vscommand))
        except Exception as e:
            log.error(e)
            return False