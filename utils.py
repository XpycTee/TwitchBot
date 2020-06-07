import json, requests, time, _thread, datetime, os

import urllib.request as urllib
from time import sleep

import Data

class Chat(object):
	"""Class of Chat on Stream"""
	
	class Users(object):
		"""Users in chat object"""
		def isOp(user):
			"""Checking whether the user is an Op"""
			return user.lower() in Data.Twitch.oplist

	def sendMessage(sock, mess):
		"""Sending message in chat"""
		sock.send("PRIVMSG #{} :{}\r\n".format(Data.Twitch.CHAN, mess).encode("utf-8"))

class Stream(object):
	""" class of Stream on Twitch """

	def isLive():
		"""Get Stream Status"""
		stream = Stream.requestData()
		#Bot.logging_all(stream)
		if stream["stream"] != None:
			return True
		else:
			return False

	def requestData():
		"""Request Stream Data from Twitch Kraken API"""
		url = f'https://api.twitch.tv/kraken/streams/{Data.Stream.channel_ID}'
		return TwitchAPI.request(url)

class Bot(object):
	def gen_moduleFolder(modName):
		if not modName.replace('modules.', '') in os.listdir("modules"):
			modFolderName = modName.replace('modules.', '')
			os.mkdir(f"modules\\{modFolderName}")
			return f"modules\\{modFolderName}"
		else:
			modFolderName = modName.replace('modules.', '')
			return f"modules\\{modFolderName}"
	
	def logging_all(message):
		Bot.logging_inFile(message)
		Bot.logging_inLive(message)
	
	def logging_inLive(message):
		if Data.Bot.settings['logging']['live']:
			timeNow = time.strftime("%H.%M.%S", time.localtime())
			print(f"{timeNow} {message}")
	
	def logging_inFile(message):
		if Data.Bot.settings['logging']['file']:
			today = datetime.datetime.today()
			timeNow = time.strftime("%H.%M.%S", time.localtime())
			with open(f'log\\log_{today.strftime("%Y-%m-%d")}.log', 'a', encoding='utf-8') as log_file:
				log_file.write(f"{timeNow} {message}\n")
	
	def fill_opList():
		while True:
			try:
				url = f'http://tmi.twitch.tv/group/user/{Data.Twitch.CHAN}/chatters'
				req = urllib.Request(url, headers={"accept": "*/*"})
				res = urllib.urlopen(req).read()
				Data.Twitch.oplist.clear()
				data = json.loads(res) 
				for p in data["chatters"]["broadcaster"]:
					Data.Twitch.oplist[p] = "broadcaster"
				for p in data["chatters"]["moderators"]:
					Data.Twitch.oplist[p] = "mod"
				for p in data["chatters"]["global_mods"]:
					Data.Twitch.oplist[p] = "global_mods"
				for p in data["chatters"]["admins"]:
					Data.Twitch.oplist[p] = "admins"
				for p in data["chatters"]["staff"]:
					Data.Twitch.oplist[p] = "staff"
			except:
				"Something went wrong...do nothing"
				#logging_all("Something went wrong...do nothing")
			sleep(5)

class TwitchAPI(object):
	def request(url):
		req = ""
		if Data.Twitch.API == "":
			req = requests.get(url, headers = {"Authorization" : f"OAuth {Data.Twitch.PASS}", "Accept" : "application/vnd.twitchtv.v5+json"})
		else:
			req = requests.get(url, headers = {"Client-ID" : Data.Twitch.API, "Accept" : "application/vnd.twitchtv.v5+json"})
		req.raise_for_status()
		return req.json()



