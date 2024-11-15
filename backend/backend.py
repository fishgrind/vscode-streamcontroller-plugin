import websockets

from streamcontroller_plugin_tools import BackendBase


class Backend(BackendBase):


    async def send_message(ws_uri, message):
        async with websockets.connect(ws_uri) as websocket:
            await websocket.send(message)
            return True

    def __init__(self):
        super().__init__()





backend = Backend()