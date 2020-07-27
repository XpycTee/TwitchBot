import http.server as http
import ssl
import socket
import os
from http import cookies
from threading import Thread
from socketserver import ThreadingMixIn

import Data

HandlerClass = http.CGIHTTPRequestHandler
ServerClass  = http.HTTPServer
Protocol     = "HTTP/1.0"

class HttpProcessor(HandlerClass):
    def send_error(self, code, message=None):
        if code == 404:
            self.path = "/cgi-bin/router.py"
        return HandlerClass.do_GET(self)
    def do_GET(self):
        os.environ["SESSION_URI"] = str(self.path)
        page = self.path[1:].split('?')[0]
        if self.path == "/login":
            page = "/login.html"
        if self.path == "/":
            page = "home"
        if f'{page}.html' in os.listdir("web/pages/"):
            self.path = "/cgi-bin/router.py"
        return HandlerClass.do_GET(self)
    def do_POST(self):
        if self.path == "/auth":
            self.path = "/cgi-bin/auth.py"
        return HandlerClass.do_POST(self)
    def __init__(self, *args, **kwargs):
        self.have_fork=False
        super().__init__(*args, directory='web/', **kwargs)

class Server(object):
    """Web server"""
    def startServer(self):
        httpd = ServerClass((self.ip_address,self.port), HttpProcessor)
        if self.sslCrypt:
            httpd.socket = ssl.wrap_socket(httpd.socket, server_side=False, certfile='web/cert/cert.pem', keyfile='web/cert/privkey.pem')
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                httpd.server_close()
                pass

    def __init__(self, ip_address, port, sslCrypt = False):
        super(Server, self).__init__()
        self.ip_address = ip_address
        self.port = port
        self.sslCrypt = sslCrypt
