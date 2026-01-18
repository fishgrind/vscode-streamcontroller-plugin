import websockets
import asyncio
import json
import threading
from streamcontroller_plugin_tools import BackendBase

class Backend(BackendBase):
    def __init__(self):
        super().__init__()
        self.server = WebSocketServer()
        # Start the server in a separate background thread 
        # so it doesn't block the StreamController main thread
        self.server_thread = threading.Thread(target=self.run_server, daemon=True)
        self.server_thread.start()

    def run_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.server.start())

    def queue_command(self, vscommand):
        # Instead of creating a new connection to itself, 
        # you can now call a method directly on self.server
        asyncio.run_coroutine_threadsafe(
            self.server.broadcast_to_active(vscommand), 
            asyncio.get_event_loop()
        )

class WebSocketServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 48969 # Use integer, not string
        self.activeClient = set()
        self.allClients = set()

    async def echo(self, websocket):
        self.allClients.add(websocket)
        try:
            async for message in websocket:
                msg = json.loads(message)
                if msg.get("id") == "ChangeActiveSessionMessage":
                    self.activeClient.clear()
                    self.activeClient.add(websocket)
                    
                    data = msg
                    data["id"] = "ActiveSessionChangedMessage"
                    websockets.broadcast(self.allClients, json.dumps(data))
                else:
                    # Generic forwarding logic
                    websockets.broadcast(self.activeClient, json.dumps(msg))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.allClients.remove(websocket)
            if websocket in self.activeClient:
                self.activeClient.remove(websocket)

    async def broadcast_to_active(self, command):
        if self.activeClient:
            websockets.broadcast(self.activeClient, command)

    async def start(self):
        # This starts the actual listener
        async with websockets.serve(self.echo, self.host, self.port):
            await asyncio.Future()
