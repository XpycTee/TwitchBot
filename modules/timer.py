import Data, Utils, os, yaml, time

def starter():
	spamList = { "timers" : [
		{ 
			"description" : "после 5 линий и после 1 минуты",
			"messages" : ["Первое: после 5 линий и после 1 минуты", "Второе: после 5 линий и после 1 минуты"], 
			"timer" : 1, 
			"lines" : 5
		}]
	}
	folderPath = Utils.Bot.moduleFolder(__name__)
	if not 'messages.yml' in os.listdir(folderPath):
		with open(f'{folderPath}\\messages.yml', 'w') as spamMsgs:
			spamMsgData = yaml.dump(spamList, spamMsgs)

	Data.Mods.globData["timer"] = { "messages": { "count" : 0 }, "timers" : { "0" : { "last_time" : 0, "last_post" : 0 } } }

def responder(message, username):
	Data.Mods.globData["timer"]["messages"]["count"] += 1
	folderPath = Utils.Bot.moduleFolder(__name__)
	with open(f'{folderPath}\\messages.yml') as spamMsgs:
		spamList = yaml.load(spamMsgs, Loader=yaml.FullLoader)
	countMessInFile = len(spamList["timers"][0])
	countMessLocal = len(Data.Mods.globData["timer"]["timers"])
	if countMessInFile > countMessLocal:
		for i in range(countMessLocal, countMessInFile-1):
			Data.Mods.globData["timer"]["timers"][f"{i}"] = { "last_time" : 0, "last_post" : 0 }
	retMess = None
	timer_id = 0
	for timer in spamList["timers"]:
		if timer["lines"] == 0:
			Utils.Bot.logging_inLive("Количество строк и минут сообщениея не могут быть меньше 1")
			return
		count = Data.Mods.globData["timer"]["messages"]["count"]
		if Data.Mods.globData["timer"]["messages"]["count"] % timer["lines"] == 0:
			for message_id in range(0, len(timer["messages"])-1):
				if message_id == Data.Mods.globData["timer"]["timers"][f"{timer_id}"]["last_post"]:
					if message_id <= countMessLocal:
						message_id += 1
					else:
						message_id = 0
				deltaTime = time.time() - Data.Mods.globData["timer"]["timers"][f"{timer_id}"]["last_time"]
				timerTime = timer["timer"] * 60
				if deltaTime > timerTime:
					retMess = timer["messages"][message_id]
					Data.Mods.globData["timer"]["timers"][f"{timer_id}"]["last_time"] = time.time()
					Data.Mods.globData["timer"]["timers"][f"{timer_id}"]["last_post"] = message_id
		timer_id += 1
	return retMess

	