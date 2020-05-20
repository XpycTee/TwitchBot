import utils
import ssl, socket, json, re
import time, _thread, random, datetime
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
			checkHelloMess = message.lower()
			upTimeMod(s, checkHelloMess, username)
			rndRangMod(s, checkHelloMess, username)
			helloMod(s, checkHelloMess, username)
			commndsMod(s, checkHelloMess, username)
		sleep(1)

def upTimeMod(sock, message, username):
	if (message.strip() == "!uptime" or message.strip() == "!time"):
		startTime = datetime.datetime(2020, 5, 19, 15, 50, 0)
		nowTime = datetime.datetime.now()
		deltaTime = nowTime - startTime
		seconds = deltaTime.total_seconds()
		deltaHours = seconds // 3600
		deltaMinutes = (seconds % 3600) // 60
		deltaSeconds = seconds % 60
		utils.mess(sock, "@"+username+" "+str(int(deltaHours))+" ч. "+str(int(deltaMinutes))+" м. <3 с учетом ребутов")

def rndRangMod(sock, message, username):
	if message.strip() == "!ранг":
		if username == "tovarischcummissar":
			utils.mess(sock, "@"+username+" \"Генералиссимус\"")
		else:
			rangs = [
			'Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой','Рядовой',
			'Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор','Ефрейтор',
			'Сержант','Сержант','Сержант','Сержант','Сержант','Сержант','Сержант','Сержант','Сержант','Сержант','Сержант','Сержант',
			'Ст.Сержант','Ст.Сержант','Ст.Сержант','Ст.Сержант','Ст.Сержант','Ст.Сержант','Ст.Сержант','Ст.Сержант','Ст.Сержант','Ст.Сержант','Ст.Сержант',
			'Лейтенант','Лейтенант','Лейтенант','Лейтенант','Лейтенант','Лейтенант','Лейтенант','Лейтенант','Лейтенант','Лейтенант',
			'Ст.Лейтенант','Ст.Лейтенант','Ст.Лейтенант','Ст.Лейтенант','Ст.Лейтенант','Ст.Лейтенант','Ст.Лейтенант','Ст.Лейтенант','Ст.Лейтенант',
			'Капитан','Капитан','Капитан','Капитан','Капитан','Капитан','Капитан','Капитан',
			'Майор','Майор','Майор','Майор','Майор','Майор','Майор','Майор',
			'Подполковник','Подполковник','Подполковник','Подполковник','Подполковник','Подполковник','Подполковник',
			'Полковник','Полковник','Полковник','Полковник','Полковник','Полковник',
			'Генерал-майор','Генерал-майор','Генерал-майор','Генерал-майор','Генерал-майор',
			'Генерал-лейтенант','Генерал-лейтенант','Генерал-лейтенант','Генерал-лейтенант',
			'Генерал-полковник','Генерал-полковник','Генерал-полковник',
			'Генерал стрима','Генерал стрима',
			'Маршал стрима']
			utils.mess(sock, "@"+username+" получил звание \""+random.choice(rangs)+"\"")

def helloMod(sock, message, username):
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
			message.find("VoHiYo") != -1 or 
			message.find("hello") != -1)):
		if username != "tmi":
			sleep(2)
			utils.hello(sock, username)

def commndsMod(sock, message, username):
	if message.strip() == "!hi":
		utils.hello(sock, username)
	if message.strip() == "!roll":
		utils.mess(sock, f"{username} выкинул: {str(randint(1, 6))}")
	if message.strip() == "!банкет":
		utils.mess(sock, f"{username} накрыл стол для чатика из шашлычка, картошечки, грибочков и пыва panicBasket TakeNRG")
	if message.strip() == "!смех":
		utils.mess(sock, f"{username} ХаХа-ХаХа")
	if message.strip() == "!вогне":
		utils.mess(sock, "grafoyniPls Deutschland, mein Herz in Flammen grafoyniPls")

def waitCLI(sock):
	cliMsg = input()
	utils.mess(sock, f"{cliMsg}")
	waitCLI(sock)

if __name__ == "__main__":
	main()