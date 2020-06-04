import json, requests, time, _thread, datetime, os

import urllib.request as urllib
from time import sleep

import twitch_data as twitch

settings = {}

def mess(sock, mess):
	sock.send("PRIVMSG #{} :{}\r\n".format(twitch.CHAN, mess).encode("utf-8"))

def genModuleFolder(modName):
	if not modName.replace('modules.', '') in os.listdir("modules"):
		modFolderName = modName.replace('modules.', '')
		os.mkdir(f"modules\\{modFolderName}")
		return f"modules\\{modFolderName}"
	else:
		modFolderName = modName.replace('modules.', '')
		return f"modules\\{modFolderName}"

def reqAPItwitch(url):
	req = ""
	if twitch.API != "":
		req = requests.get(url, headers = {"Authorization" : f"OAuth {twitch.PASS}", "Accept" : "application/vnd.twitchtv.v5+json"})
	else:
		req = requests.get(url, headers = {"Client-ID" : twitch.API, "Accept" : "application/vnd.twitchtv.v5+json"})
	req.raise_for_status()
	return req.json()

def reqStreamData():
	userID = reqAPItwitch(f'https://api.twitch.tv/kraken/users?login={twitch.CHAN}')['users'][0]['_id']
	url = f'https://api.twitch.tv/kraken/streams/{userID}'
	return reqAPItwitch(url)

def streamIsLive():
	stream = reqStreamData()["stream"]
	if stream != None:
		return True
	else:
		return False
def logging_all(message):
	logging_inFile(message)
	logging_inLive(message)

def logging_inLive(message):
	if settings['logging']['live']:
		timeNow = time.strftime("%H.%M.%S", time.localtime())
		print(f"{timeNow} {message}")

def logging_inFile(message):
	if settings['logging']['file']:
		today = datetime.datetime.today()
		timeNow = time.strftime("%H.%M.%S", time.localtime())
		with open(f'log\\log_{today.strftime("%Y-%m-%d")}.log', 'a', encoding='utf-8') as log_file:
			log_file.write(f"{timeNow} {message}\n")

def fillOpList():
	while True:
		try:
			url = f'http://tmi.twitch.tv/group/user/{twitch.CHAN}/chatters'
			req = urllib.Request(url, headers={"accept": "*/*"})
			res = urllib.urlopen(req).read()
			twitch.oplist.clear()
			data = json.loads(res) 
			for p in data["chatters"]["broadcaster"]:
				twitch.oplist[p] = "broadcaster"
			for p in data["chatters"]["moderators"]:
				twitch.oplist[p] = "mod"
			for p in data["chatters"]["global_mods"]:
				twitch.oplist[p] = "global_mods"
			for p in data["chatters"]["admins"]:
				twitch.oplist[p] = "admins"
			for p in data["chatters"]["staff"]:
				twitch.oplist[p] = "staff"
		except:
			"Something went wrong...do nothing"
			#logging_all("Something went wrong...do nothing")
		sleep(5)

def isOp(user):
	return user.lower() in twitch.oplist

