import http.server as http
import ssl, socket, os
from threading import Thread
from socketserver import ThreadingMixIn

HandlerClass = http.CGIHTTPRequestHandler
ServerClass  = http.HTTPServer
Protocol	 = "HTTP/1.0"

class HttpProcessor(HandlerClass):
	#def send_error(self, code, message=None):
	#	if code == 404:
	#		self.path = "/cgi-bin/index.py"
	#	return HandlerClass.do_GET(self)
	def do_GET(self):
		os.environ["SESSION_URI"] = str(self.path)
		"""print(os.listdir())
		page = self.path[1:].split('?')[0]
		if f'{page}.html' in os.listdir("web/pages/"):
			self.path = "/cgi-bin/index.py"
		if self.path == "/":
			self.path = "/cgi-bin/index.py\""""
		return HandlerClass.do_GET(self)
	def __init__(self, *args, **kwargs):
		super().__init__(*args, directory='web/', **kwargs)

def serve_on_port(port, sslCrypt=False):
	httpd = ServerClass(("0.0.0.0",port), HttpProcessor)
	if sslCrypt:
		httpd.socket = ssl.wrap_socket(httpd.socket, server_side=False, certfile='web/cert/cert.pem', keyfile='web/cert/privkey.pem')

	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass

	httpd.server_close()
