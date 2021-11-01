from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading
import posixpath
from urllib import parse
import os


class RootedHTTPRequestHandler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        path = posixpath.normpath(parse.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.base_path
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

class RootedHTTPServer(ThreadingHTTPServer):

    def __init__(self, base_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.RequestHandlerClass.base_path = base_path

class HttpServer(threading.Thread):
    def __init__(self, logdir, port = 4444, https =False, *args, **kwargs) -> None:
        self.port = port
        self.server = RootedHTTPServer(logdir, ('0.0.0.0', port), RootedHTTPRequestHandler)
        if https:
            import ssl
            self.server.socket = ssl.wrap_socket(
                self.server.socket,
                keyfile='./key.pem',
                certfile='./cert.pem',
                server_side=True
            )
        super().__init__(*args, **kwargs)

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()

    def run(self):
        self.server.serve_forever()