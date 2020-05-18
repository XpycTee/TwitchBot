import utils
import socket, json, re
import time, _thread, random
import twitch_data as twitch
import urllib.request as urllib
from random import randint
from time import sleep
from modules import *


def main():
	s = socket.socket()
	s.connect((twitch.HOST, twitch.PORT))
	s.send("PASS {}\r\n".format(twitch.PASS).encode("utf-8"))
	s.send("NICK {}\r\n".format(twitch.NICK).encode("utf-8"))
	s.send("JOIN #{}\r\n".format(twitch.CHAN).encode("utf-8"))
	

	chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
	utils.mess(s, "Здрова, Всем! KonCha <3")

	_thread.start_new_thread(utils.fillOpList, ())
	#_thread.start_new_thread(waitCLI, (s,))
	while True:
		response = s.recv(1024).decode("utf-8")
		if response == "PING :tmi.twitch.tv\r\n":
			s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
		else: 
			username = re.search(r"\w+", response).group(0)
			message = chat_message.sub("", response)
			message = message.lower()
			print(username+": "+message)
			#print(response)
			if (message.find(twitch.NICK.lower()) != -1 and 
				(message.find("привет") != -1 or 
					message.find("ку") != -1 or 
					message.find("здорова") != -1 or 
					message.find("приветик") != -1 or 
					message.find("здравствуйте") != -1 or 
					message.find("хай") != -1 or 
					message.find("хелоу") != -1 or 
					message.find("хеллоу") != -1 or 
					message.find("hi") != -1 or 
					message.find("йоу") != -1 or 
					message.find("yo") != -1 or 
					message.find("heyguys") != -1 or 
					message.find("hey") != -1 or 
					message.find("koncha") != -1 or 
					message.find("hello") != -1)):
				if username != "tmi":
					sleep(2)
					utils.hello(s, username)
			if message.strip() == "!hi":
				utils.hello(s, username)
			if message.strip() == "!roll":
				utils.mess(s, f"{username} выкинул: {str(randint(1, 6))}")
			if message.strip() == "!банкет":
				utils.mess(s, f"{username} накрыл стол для чатика из шашлычка, картошечки, грибочков и пыва panicBasket TakeNRG")
			if message.strip() == "!смех":
				utils.mess(s, f"{username} ХаХа-ХаХа")
		sleep(1)

def waitCLI(s):
	cliMsg = input()
	utils.mess(s, f"{cliMsg}")
	waitCLI(s)

if __name__ == "__main__":
	main()