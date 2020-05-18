import utils
import ssl, socket, json, re
import time, _thread, random
import twitch_data as twitch
import urllib.request as urllib
from random import randint
from time import sleep
from modules import *

def irc_send():
	pass

def main():
	tcp_sock = socket.socket()
	ssl_sock = ssl.wrap_socket(tcp_sock)
	ssl_sock.connect((twitch.HOST, twitch.PORT))
	ssl_sock.send("PASS {}\r\n".format(twitch.PASS).encode("utf-8"))
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
			#print(response)
			checkHelloMess = message.lower()
			if (checkHelloMess.find(twitch.NICK.lower()) != -1 and
				(checkHelloMess.find("привет") != -1 or 
					checkHelloMess.find("ку") != -1 or 
					checkHelloMess.find("здорова") != -1 or 
					checkHelloMess.find("приветик") != -1 or 
					checkHelloMess.find("здравствуйте") != -1 or 
					checkHelloMess.find("хай") != -1 or 
					checkHelloMess.find("хелоу") != -1 or 
					checkHelloMess.find("хеллоу") != -1 or 
					checkHelloMess.find("hi") != -1 or 
					checkHelloMess.find("йоу") != -1 or 
					checkHelloMess.find("yo") != -1 or 
					checkHelloMess.find("heyguys") != -1 or 
					checkHelloMess.find("hey") != -1 or 
					checkHelloMess.find("koncha") != -1 or 
					checkHelloMess.find("hello") != -1)):
				if username != "tmi":
					sleep(3)
					utils.hello(ssl_sock, username)
			if message.strip() == "!hi":
				utils.hello(ssl_sock, username)
			if message.strip() == "!roll":
				utils.mess(ssl_sock, f"{username} выкинул: {str(randint(1, 6))}")
			if message.strip() == "!банкет":
				utils.mess(ssl_sock, f"{username} накрыл стол для чатика из шашлычка, картошечки, грибочков и пыва panicBasket TakeNRG")
			if message.strip() == "!смех":
				utils.mess(ssl_sock, f"{username} ХаХа-ХаХа")
		sleep(1)

def waitCLI(sock):
	cliMsg = input()
	utils.mess(sock, f"{cliMsg}")
	waitCLI(sock)

if __name__ == "__main__":
	main()