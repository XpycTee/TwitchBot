import sys, datetime


def main(message, username):
	message = message.lower()
	if (message.strip() == "!uptime" or message.strip() == "!time" or message.strip() == "!время" or (message.find("сколько") != -1 and (message.find("идет") != -1 or message.find("длится") != -1) and message.find("стрим") != -1)):
		startTime = datetime.datetime(2020, 5, 19, 15, 50, 0)
		nowTime = datetime.datetime.now()
		deltaTime = nowTime - startTime
		seconds = deltaTime.total_seconds()

		deltaHours = int(seconds // 3600)
		deltaMinutes = int((seconds % 3600) // 60)

		wordHours = wordsForNumsRus(deltaHours, "час", "часа", "часов")
		wordMinutes = wordsForNumsRus(deltaMinutes, "минута", "минуты", "минут")

		print(f"@{username} {deltaHours} {wordHours} {deltaMinutes} {wordMinutes} <3")

def wordsForNumsRus(number, singleN1, singleN2, plural):
	if number % 10 == 1:
		result = singleN1
	if number % 10 >= 2 and number % 10 <= 4:
		result = singleN2
	if (number % 10 >= 5 and number % 10 <= 9) or number % 10 == 0 or (number >= 11 and number <= 19):
		result = plural
	return result


main(sys.argv[1], sys.argv[2])