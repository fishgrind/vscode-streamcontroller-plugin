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
    def queue_command(self, vscommand):
        host = "127.0.0.1"
        port = "48969"
        ws_uri = "ws://{host}:{port}".format(host=host, port=port)
        self.thread.run_until_complete(self.push_command(ws_uri, vscommand))

    async def push_command(self, ws_uri, vscommand):
        async with websockets.connect(ws_uri) as websocket:
            await websocket.send(vscommand)
            websocket.close
            return True

backend = Backend()


class WebSocketServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "48969"
        self.activeClient = set()
        self.allClients = set()

    async def echo(self, websocket):
        self.allClients.add(websocket)
        async for message in websocket:
            try:
                msg = json.loads(message) #read the data

                if msg["id"] == "ChangeActiveSessionMessage":
                    #make sure the right vscode session receives the data
                    self.activeClient.clear()
                    self.activeClient.add(websocket)

                    data = msg
                    data["id"] = "ActiveSessionChangedMessage"
                    websockets.broadcast(self.allClients,json.dumps(data))

                elif msg["id"] == "StreamControllerConnected":
                    print("streamcontroller connected")
                else:
                    data = msg
                    data["data"] = json.dumps(msg["data"])
                    websockets.broadcast(self.activeClient,json.dumps(data))
            except websockets.exceptions.ConnectionClosed:
                pass
            # finally:
                # self.activeClient.remove(websocket)

    async def start(self):
        async with websockets.serve(self.echo, self.host, self.port):
            await asyncio.Future()  # Run forever

if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.start())
