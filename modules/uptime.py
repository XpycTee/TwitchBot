import sys, datetime


def main(message, username):
	message = message.lower()
	if (message.strip() == "!uptime" or message.strip() == "!time" or message.strip() == "!время" or (message.find("сколько") != -1 and (message.find("идет") != -1 or message.find("длится") != -1) and message.find("стрим") != -1)):
		startTime = datetime.datetime.now()#datetime.datetime(2020, 5, 19, 15, 50, 0)
		nowTime = datetime.datetime.now()
		deltaTime = nowTime - startTime
		seconds = deltaTime.total_seconds()
		deltaHours = seconds // 3600
		deltaMinutes = (seconds % 3600) // 60
		deltaSeconds = seconds % 60
		print(f"@{username} {str(int(deltaHours))} ч. {str(int(deltaMinutes))} м. <3")

main(sys.argv[1], sys.argv[2])