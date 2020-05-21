import sys
from time import sleep
from random import randint

def execute(message, username):
	if message.strip() == "!hi":
		return f"Привет, @{username} KonCha <3"
	if message.strip() == "!roll":
		return f"{username} выкинул: {str(randint(1, 6))}"
	if message.strip() == "!банкет":
		return f"{username} накрыл стол для чатика из шашлычка, картошечки, грибочков и пыва panicBasket TakeNRG"
	if message.strip() == "!смех":
		return f"{username} ХаХа-ХаХа"
	if message.strip() == "!вогне":
		return "grafoyniPls Deutschland, mein Herz in Flammen grafoyniPls"
	checkHelloMess = message.lower()
	if (checkHelloMess.find("xpyctee") != -1 and 
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
			checkHelloMess.find("VoHiYo") != -1 or 
			checkHelloMess.find("hello") != -1)):
		if username != "tmi":
			sleep(2)
			return f"Привет, @{username} KonCha <3"