import asyncio
import websockets
import json

import os
from streamcontroller_plugin_tools import BackendBase


class Backend(BackendBase):

    # host = "127.0.0.1"
    # port = "48969"
    # ws_uri = "ws://{host}:{port}".format(host=host, port=port)

    # async def init_streamdeck(self, ws_uri):
    #     message = {
    #         "id":"StreamControllerConnected"
    #         }

    #     async with websockets.connect(ws_uri) as websocket:
    #         await websocket.send({"id":"StreamControllerConnected"})
    #         return

    def __init__(self):
        super().__init__()
        host = "127.0.0.1"
        port = "48969"
        ws_uri = "ws://{host}:{port}".format(host=host, port=port)

        message = {
            "id":"StreamControllerConnected"
            }

        async with websockets.connect(ws_uri) as websocket:
            websocket.send({"id":"StreamControllerConnected"})




backend = Backend()