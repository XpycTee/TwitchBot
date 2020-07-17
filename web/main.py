import http.server as http
import ssl, socket, os
from threading import Thread
from socketserver import ThreadingMixIn

class HttpProcessor(http.SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/':
			self.path = 'web/html/index.html'
		return http.SimpleHTTPRequestHandler.do_GET(self)

class ThreadingHTTPServer(ThreadingMixIn, http.HTTPServer):
	daemon_threads = True

def serve_on_port(port, sslCrypt=False):
	serv = ThreadingHTTPServer(("0.0.0.0",port), HttpProcessor)
	if sslCrypt:
		serv.socket = ssl.wrap_socket(serv.socket, server_side=True, certfile='web/cert/cert.pem', keyfile='web/cert/privkey.pem')
	serv.serve_forever()