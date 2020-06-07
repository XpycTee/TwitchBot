import sys, os, yaml, time, json, random

import urllib.request as urllib

import Utils, Data

def starter():
	usersList = {}
	folderPath = Utils.Bot.gen_moduleFolder(__name__)
	if not f'users.yml' in os.listdir(folderPath):
		with open(f'{folderPath}\\users.yml', 'w') as chatUsers:
			chatUsersData = yaml.dump(usersList, chatUsers)
	
	while True:
		try:
			if Utils.Stream.isLive():
				url = f'http://tmi.twitch.tv/group/user/{Data.Twitch.CHAN}/chatters'
				req = urllib.Request(url, headers={"accept": "*/*"})
				res = urllib.urlopen(req).read()
				chattersData = json.loads(res)["chatters"]
				with open(f'{folderPath}\\users.yml') as usersFile:
					usersList = yaml.load(usersFile, Loader=yaml.FullLoader)
				for user in usersList:
					if (user in chattersData["broadcaster"] or 
						user in chattersData["moderators"] or 
						user in chattersData["global_mods"] or 
						user in chattersData["admins"] or 
						user in chattersData["staff"] or 
						user in chattersData["viewers"]):
							usersList[user]["points"] += 100 
							with open(f'{folderPath}\\users.yml', 'w') as chatUsers:
								chatUsersData = yaml.dump(usersList, chatUsers)
		except Exception as e:
			Utils.Bot.logging_all(str(e))
		time.sleep(300)


def responder(message, username):

	def updateUserListFile(usersList):
		with open(f'modules\\points\\users.yml', 'w') as chatUsers:
			chatUsersData = yaml.dump(usersList, chatUsers)

	with open('modules\\points\\users.yml') as usersFile:
		usersList = yaml.load(usersFile, Loader=yaml.FullLoader)

	if not username.lower() in usersList:
		onUpdateDict = {username.lower(): {
			'registation': int(time.time()),
			'points': 0
		}}
		usersList.update(onUpdateDict)
		updateUserListFile(usersList)

	if (message.strip() == "!points"):
		return f"{username}, {usersList[username.lower()]['points']} поинтов"

	if (message.startswith("!give")):
		splitedMsg = message.strip().split(" ")

		toWhom = splitedMsg[1].replace("@", "")

		try:
			howMany = int(splitedMsg[2])
		except ValueError:
			return f"{username}, {splitedMsg[2]} не является числом"

		if Utils.Chat.Users.isOp(username.lower()):
			if toWhom.lower() in usersList:
				usersList[toWhom.lower()]["points"] += howMany
				updateUserListFile(usersList)
				return f"{username}, перевел {howMany} поинтов {toWhom} PogChamp"
			else:
				return f"{username}, такого пользователся в чате нет"

		if toWhom.lower() == username.lower():
			return f"{username}, вы не можете перевести поинты самому себе"

		if usersList[username.lower()]['points'] < howMany:
			return f"{username}, у вас всего {usersList[username.lower()]['points']}"

		if toWhom.lower() in usersList:
			usersList[username.lower()]['points'] -= howMany
			usersList[toWhom.lower()]["points"] += howMany
			updateUserListFile(usersList)
			return f"{username}, перевел {howMany} поинтов {toWhom} PogChamp"
		else:
			return f"{username}, такого пользователся в чате нет"

	if (message.startswith("!roulette")):
		splitedMsg = message.strip().split(" ")
		try:
			if splitedMsg[1] != "all":
				howMany = int(splitedMsg[1])
			else: 
				howMany = usersList[username.lower()]['points']
		except ValueError:
			return f"{username}, {splitedMsg[1]} не является числом"
		except IndexError:
			return f"{username}, не ввел сумму"

		if usersList[username.lower()]['points'] < howMany:
			return f"{username}, у вас всего {usersList[username.lower()]['points']}"
		if random.choice([True, False]):
			usersList[username.lower()]['points'] += howMany
			updateUserListFile(usersList)
			return f"{username} выиграл {howMany} поинтов в рулетке и сейчас имеет {usersList[username.lower()]['points']} поинтов!"
		else:
			usersList[username.lower()]['points'] -= howMany
			updateUserListFile(usersList)
			return f"{username} проиграл {howMany} поинтов в рулетке и сейчас имеет {usersList[username.lower()]['points']} поинтов!"