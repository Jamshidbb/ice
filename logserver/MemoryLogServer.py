import json
import os
import asyncio
import websockets
import os
import threading
import queue

from logserver.LogHttpServer import HttpServer


MIME_TYPES = {
    "html": "text/html",
    "js": "text/javascript",
    "css": "text/css"
}


class MemoryLogServer(threading.Thread):
    def __init__(self, logroot, delay=0.1, port = 4444, wsport=8765, *args, **kwargs):
        self.q = queue.Queue()
        self.port = port
        self.wsport = wsport
        self.delay = delay
        self.root = os.path.dirname(os.path.realpath(__file__))
        self.logroot = logroot
        self.httpserver = HttpServer(os.path.join(os.getcwd(), 'logserver', 'public'), port)
        super().__init__(*args, **kwargs)

    async def data(self, websocket, path):
        print("New WebSocket connection from", websocket.remote_address)
        self.load()
        await websocket.send(json.dumps(self.init()))
        while websocket.open:
            try:
                data = json.dumps(self.q.get(timeout=3))
                await websocket.send(data)
            except queue.Empty:
                pass
            await asyncio.sleep(self.delay)
        self.q.task_done()        
        print("WebSocket connection closed for", websocket.remote_address)
    
    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())

        self.httpserver.start()
        print(f"Running server at http://127.0.0.1:{self.port}/")
        
        start_server = websockets.serve(self.data, '127.0.0.1', self.wsport)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def put(self, value):
        try:
            self.q.put_nowait(value)
            return True
        except queue.Full:
            return False

    def init():
        pass

    def save(self):
        pass

    def load(self):
        pass
