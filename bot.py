import utils
import ssl, socket, json, re
import time, _thread
import sys, os
import subprocess
import twitch_data as twitch
import urllib.request as urllib
from time import sleep
from modules import *

def main():
	tcp_sock = socket.socket()
	ssl_sock = ssl.wrap_socket(tcp_sock)
	ssl_sock.connect((twitch.HOST, twitch.PORT))
	ssl_sock.send("PASS oauth:{}\r\n".format(twitch.PASS).encode("utf-8"))
	ssl_sock.send("NICK {}\r\n".format(twitch.NICK).encode("utf-8"))
	ssl_sock.send("JOIN #{}\r\n".format(twitch.CHAN).encode("utf-8"))
	

	chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
	utils.mess(ssl_sock, "Здрова, Всем! KonCha <3")

	_thread.start_new_thread(utils.fillOpList, ())
	#_thread.start_new_thread(waitCLI, (ssl_sock,))
	while True:
		response = ssl_sock.recv(1024).decode("utf-8")
		if response == "PING :tmi.twitch.tv\r\n":
			ssl_sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
		else: 
			username = re.search(r"\w+", response).group(0)
			message = chat_message.sub("", response)
			print(username.strip()+": "+message.strip())

			all_mods = []
			for file in os.listdir(".\\modules"):
				if file.endswith(".py"):
					all_mods.insert(len(all_mods), file)
			for mod in all_mods:
				ret = None

				proc = subprocess.Popen([sys.executable, '-u', f'modules/{mod}', message, username, str(utils.isOp(username))], stdout=subprocess.PIPE, universal_newlines=True)
				for line in proc.stdout:
					ret = line
				if ret != None:
					utils.mess(ssl_sock, ret)
					ret = None
		sleep(1)

def waitCLI(sock):
	cliMsg = input(">")
	utils.mess(sock, f"{cliMsg}")
	waitCLI(sock)

if __name__ == "__main__":
	main()