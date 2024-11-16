import websockets
import asyncio
import json
import re

from streamcontroller_plugin_tools import BackendBase



class Backend(BackendBase):

    def __init__(self):
        super().__init__()


        self.thread = asyncio.new_event_loop()
        asyncio.set_event_loop(self.thread)


    #receiving commands
    def queue_command(self, ws_uri, vscommand):
        self.thread.run_until_complete(self.push_command(ws_uri, vscommand))

    async def push_command(self, ws_uri, vscommand):
        async with websockets.connect(ws_uri) as websocket:
            await websocket.send(vscommand)
            return True

backend = Backend()


class WebSocketServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "48969"
        self.clients = set()

    async def echo(self, websocket):
        # self.clients.add(websocket)
        async for message in websocket:
            try:
                msg = json.loads(message) #read the data

                if msg["id"] == "ChangeActiveSessionMessage":
                    #make sure the right vscode session receives the data
                    self.clients.clear()
                    self.clients.add(websocket)
                elif msg["id"] == "StreamControllerConnected":
                    print("streamcontroller connected")
                else:
                    data = msg
                    data["data"] = json.dumps(msg["data"])
                    websockets.broadcast(self.clients,json.dumps(data))
            except websockets.exceptions.ConnectionClosed:
                pass
            # finally:
                # self.clients.remove(websocket)

    async def start(self):
        async with websockets.serve(self.echo, self.host, self.port):
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.start())
