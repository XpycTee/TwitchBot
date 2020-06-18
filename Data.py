import yaml

class Twitch(object):

	data = {}
	with open('config.yml') as configFile:
		data = yaml.load(configFile, Loader=yaml.FullLoader)["twitch"]
	HOST = "irc.twitch.tv"
	PORT = 6697
	NICK = data["bot-name"]
	PASS = data["irc-token"]
	CHAN = data["channel"].lower()
	RATE = (20/30)
	API = data["api-token"]

	oplist = {}

	def __init__(self):
		"""Constructor"""
		pass

class Chat(object):
	emotes = {}
	userlist = {}
	def __init__(self):
		"""Constructor"""
		pass

class Mods(object):
	commands = {}
	globData = {}


class Bot(object):
	settings = {}
	def __init__(self):
		"""Constructor"""
		pass

class Stream(object):
	channel_ID = ""
	def __init__(self):
		"""Constructor"""
		pass
