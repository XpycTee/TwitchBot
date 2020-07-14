import sys, datetime, random

import Utils, Data

def responder(message, username):


	def timeResponder(username):
		if Utils.Stream.isLive():
			streamStartTimeAPI = Utils.Stream.requestData()['stream']['created_at']

			startTime = datetime.datetime.strptime(streamStartTimeAPI,"%Y-%m-%dT%H:%M:%SZ")#datetime.datetime(2020, 5, 19, 15, 50, 0)
			nowTimeNoForm = datetime.datetime.now(datetime.timezone.utc)
			nowTime = datetime.datetime(nowTimeNoForm.year, nowTimeNoForm.month, nowTimeNoForm.day, nowTimeNoForm.hour, nowTimeNoForm.minute, nowTimeNoForm.second)
			deltaTime = nowTime - startTime
			seconds = deltaTime.total_seconds()

			deltaHours = int(seconds // 3600)
			deltaMinutes = int((seconds % 3600) // 60)

			wordHours = Utils.declensionNumsRus(deltaHours, "час", "часа", "часов")
			wordMinutes = Utils.declensionNumsRus(deltaMinutes, "минуту", "минуты", "минут")

			if deltaHours > 0:
				hours = f"{deltaHours} {wordHours}"
			else:
				hours = ""
			if deltaMinutes > 0:
				mins = f"{deltaMinutes} {wordMinutes}"
			else:
				mins = "ровно"

			return f"{username}, стрим длится {hours} {mins} <3"
		else:
			return f"{username}, стрим будет через час <3"

	message = message.lower()
	splitedMsg = message.strip().split(" ")
	if (splitedMsg[0] == "!uptime" or splitedMsg[0] == "!time" or splitedMsg[0] == "!время"):
		if len(splitedMsg) == 1:
			return timeResponder(username)
		else:
			toWhom = splitedMsg[1].replace("@", "")
			if toWhom.lower() in Data.Chat.userlist:
				return timeResponder(Data.Chat.userlist[toWhom]['display_name'])
			else:
				return timeResponder(username)

	if (message.find("давно") != -1 or message.find("сколько") != -1) and (message.find("идёт") != -1 or message.find("идет") != -1 or message.find("длится") != -1) and message.find("стрим") != -1:
		return timeResponder(username)