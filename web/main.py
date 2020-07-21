import http.server as http
import ssl, socket, os
from threading import Thread
from socketserver import ThreadingMixIn

HandlerClass = http.CGIHTTPRequestHandler
ServerClass  = http.HTTPServer
Protocol	 = "HTTP/1.0"

class HttpProcessor(HandlerClass):
	def do_GET(self):
		if self.path == "/":
			self.path = "/cgi-bin/index.py"
		return HandlerClass.do_GET(self)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, directory='web/', **kwargs)

class ThreadingHTTPServer(ThreadingMixIn, ServerClass):
	daemon_threads = True

def serve_on_port(port, sslCrypt=False):
	httpd = ThreadingHTTPServer(("0.0.0.0",port), HttpProcessor)
	if sslCrypt:
		httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='web/cert/cert.pem', keyfile='web/cert/privkey.pem')
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	httpd.server_close()
