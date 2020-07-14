import sys
from time import sleep
from random import randint
import Utils, Data

def responder(message, username):
	message = message.lower()
	splitedMsg = message.strip().split(" ")
	if (splitedMsg[0] == "!mod" or splitedMsg[0] == "!мод" or splitedMsg[0] == "!моды"):
		if len(splitedMsg) == 1:
			return f"{username}, Fate of Wanderer <3"
		else:
			toWhom = splitedMsg[1].replace("@", "")
			if toWhom.lower() in Data.Chat.userlist:
				return f"{Data.Chat.userlist[toWhom]['display_name']} Fate of Wanderer <3"
			else:
				return f"{username}, Fate of Wanderer <3"
	"""if message.strip() == "!hi":
		return f"Привет, {username} KonCha <3"
	if message.strip() == "!roll":
		return f"{username} выкинул: {str(randint(1, 6))}"
	if message.strip() == "!банкет":
		return f"{username} накрыл стол для чатика из шашлычка, картошечки, грибочков и пыва panicBasket TakeNRG"
	if message.strip() == "!смех":
		return f"{username} ХоХо-ХаХа"
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
		sleep(2)
		return f"Привет, {username} KonCha <3"""