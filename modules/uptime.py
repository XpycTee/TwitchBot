import sys, datetime

import Utils

def responder(message, username):
	message = message.lower()
	if (message.strip() == "!uptime" or message.strip() == "!time" or message.strip() == "!время" or (message.find("сколько") != -1 and (message.find("идёт") != -1 or message.find("идет") != -1 or message.find("длится") != -1) and message.find("стрим") != -1)):
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
