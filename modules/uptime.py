import sys, datetime

import utils

def execute(message, username):
	message = message.lower()
	if (message.strip() == "!uptime" or message.strip() == "!time" or message.strip() == "!время" or (message.find("сколько") != -1 and (message.find("идёт") != -1 or message.find("идет") != -1 or message.find("длится") != -1) and message.find("стрим") != -1)):
		if utils.streamIsLive():
			streamStartTimeAPI = utils.reqStreamData()['stream']['created_at']

			startTime = datetime.datetime.strptime(streamStartTimeAPI,"%Y-%m-%dT%H:%M:%SZ")#datetime.datetime(2020, 5, 19, 15, 50, 0)
			nowTimeNoForm = datetime.datetime.now(datetime.timezone.utc)
			nowTime = datetime.datetime(nowTimeNoForm.year, nowTimeNoForm.month, nowTimeNoForm.day, nowTimeNoForm.hour, nowTimeNoForm.minute, nowTimeNoForm.second)
			deltaTime = nowTime - startTime
			seconds = deltaTime.total_seconds()

			deltaHours = int(seconds // 3600)
			deltaMinutes = int((seconds % 3600) // 60)

			wordHours = declensionNumsRus(deltaHours, "час", "часа", "часов")
			wordMinutes = declensionNumsRus(deltaMinutes, "минута", "минуты", "минут")

			return f"@{username}, {deltaHours} {wordHours} {deltaMinutes} {wordMinutes} <3"
		else:
			return f"@{username}, на данный момент трансляция не идет <3"

def declensionNumsRus(number, singlNomin, singlGeni, pluralGeni):
	""" 
		The function of "the Declension of the noun by the numbers" for Russian language
		- number: the number for which there is a decline
		- singlNomin: singular nominative declinable noun
		- singlGeni: singular genitive declinable noun
		- pluralGeni: plural genitive declinable noun
		Return declined noun
	"""
	if number % 10 == 1:
		result = singlNomin
	if number % 10 >= 2 and number % 10 <= 4:
		result = singlGeni
	if (number % 10 >= 5 and number % 10 <= 9) or number % 10 == 0 or (number >= 11 and number <= 19):
		result = pluralGeni
	return result
