import twitch_data as twitch 
import urllib.request as urllib
import json, requests
import time, _thread
from time import sleep

def mess(sock, mess):
	sock.send("PRIVMSG #{} :{}\r\n".format(twitch.CHAN, mess).encode("utf-8"))

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

#http://tmi.twitch.tv/group/user/xpyctee/chatters
def fillOpList():
	while True:
		try:
			url = 'http://tmi.twitch.tv/group/user/xpyctee/chatters'
			req = urllib.Request(url, headers={"accept": "*/*"})
			res = urllib.urlopen(req).read()
			twitch.oplist.clear()
			data = json.loads(res) 
			for p in data["chatters"]["broadcaster"]:
				twitch.oplist[p] = "bcaster"
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
		sleep(5)

def isOp(user):
	return user in twitch.oplist

