import utils
import ssl, socket, json, re
import time, _thread
import sys, os
import subprocess
import twitch_data as twitch
import urllib.request as urllib
from time import sleep
from modules import *

def sock_connecting():
	tcp_sock = socket.socket()
	ssl_sock = ssl.wrap_socket(tcp_sock)
	ssl_sock.connect((twitch.HOST, twitch.PORT))
	ssl_sock.send("PASS oauth:{}\r\n".format(twitch.PASS).encode("utf-8"))
	ssl_sock.send("NICK {}\r\n".format(twitch.NICK).encode("utf-8"))
	ssl_sock.send("JOIN #{}\r\n".format(twitch.CHAN).encode("utf-8"))
	return ssl_sock

def main():
	connected = False
	while connected != True:
		try:
			ssl_sock = sock_connecting()
			connected = True
		except:
			print("Нет соеденения")
			sleep(1)
	
	

	chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
	#utils.mess(ssl_sock, "Здрова, Всем! KonCha <3")

	_thread.start_new_thread(utils.fillOpList, ())
	#_thread.start_new_thread(waitCLI, (ssl_sock,))
	
	while True:
		try:
			response = ssl_sock.recv(1024).decode("utf-8")
			if response == "PING :tmi.twitch.tv\r\n":
				ssl_sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
			else: 
				username = re.search(r"\w+", response).group(0)
				message = chat_message.sub("", response)
				print(username.strip()+": "+message.strip())
				for file in os.listdir(".\\modules"):
					if file != "__init__.py":
						if file.endswith(".py"):
							execFunc = getattr(globals()[file.replace('.py', '')], "execute")
							#print(file.replace('.py', ''))
							ret = execFunc(message, username)
							if ret != None:
								utils.mess(ssl_sock, ret)
								break
		except:
			break


		sleep(0.1)
	return True

def waitCLI(sock):
	cliMsg = input(">")
	utils.mess(sock, f"{cliMsg}")
	waitCLI(sock)

reloading = True
while reloading:
	if __name__ == "__main__":
		relaod = main()