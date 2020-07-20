import Utils, Data, yaml, os
def starter():
	folderPath = Utils.Bot.moduleFolder(__name__)
	if not 'commands.yml' in os.listdir(folderPath):
		nulDict = {}
		with open(f'{folderPath}/commands.yml', 'w') as commands:
			commandsData = yaml.dump(nulDict, commands)
	with open(f'{folderPath}/commands.yml') as commands:
		commandsData = yaml.load(commands, Loader=yaml.FullLoader)
	Data.Mods.globData["chatCommander"] = commandsData

def responder(message, username):
	def addCommand(command, respond):
		Data.Mods.globData["chatCommander"].update({command : respond})
		folderPath = Utils.Bot.moduleFolder(__name__)
		if command == Data.Mods.globData["chatCommander"]:
			return f"{username}, команда !{command} уже существует"
		with open(f'{folderPath}/commands.yml', 'w') as commands:
			commandsData = yaml.dump(Data.Mods.globData["chatCommander"], commands)
		return f"{username}, команда !{command} добавлена"

	def removeCommand(command):
		try:
			Data.Mods.globData["chatCommander"].pop(command)
		except KeyError:
			return f"{username}, команды !{command} нет"
		folderPath = Utils.Bot.moduleFolder(__name__)
		with open(f'{folderPath}/commands.yml', 'w') as commands:
			commandsData = yaml.dump(Data.Mods.globData["chatCommander"], commands)
		return f"{username}, команда !{command} удалена"
		
	def updateCommand(command, respond):
		Data.Mods.globData["chatCommander"].update({command : respond})
		folderPath = Utils.Bot.moduleFolder(__name__)
		with open(f'{folderPath}/commands.yml', 'w') as commands:
			commandsData = yaml.dump(Data.Mods.globData["chatCommander"], commands)
		return f"{username}, команда !{command} обновлена"

	splitedMsg = message.strip().split(" ")
	if Utils.Chat.Users.isOp(username):
		if (splitedMsg[0].lower() == "!rmcommand" or splitedMsg[0].lower() == "!addcommand"):
			try:
				command = splitedMsg[1].lower()
			except IndexError:
				return f"{username}, команда не введена"
			if (splitedMsg[0] == "!rmcommand"):
				return removeCommand(command)	
			try:
				respond = splitedMsg[2]
			except IndexError:
				return f"{username}, сообщение не введено"
			if len(splitedMsg) > 3:
				for wordIndex in range(3,len(splitedMsg)):
					respond = f"{respond} {splitedMsg[wordIndex]}"
			if (splitedMsg[0].lower() == "!addcommand"):
				return addCommand(splitedMsg[1].lower(),respond);
			if (splitedMsg[0].lower() == "!upcommand"):
				return addCommand(splitedMsg[1].lower(),respond);
	if splitedMsg[0][0] != "!":
		return None
	commandForRespond = splitedMsg[0].replace("!","")
	if commandForRespond in Data.Mods.globData["chatCommander"]:
		if len(splitedMsg) == 1:
			ret = Data.Mods.globData["chatCommander"][commandForRespond]
			message = ret.replace('{username}', username)
			return message
		else:
			toWhom = splitedMsg[1].replace("@", "")
			if toWhom.lower() in Data.Chat.userlist:
				ret = Data.Mods.globData["chatCommander"][commandForRespond]
				message = ret.replace('{username}', Data.Chat.userlist[toWhom]['display_name'])
				return message
			else:
				ret = Data.Mods.globData["chatCommander"][commandForRespond]
				message = ret.replace('{username}', username)
				return message
		

		
