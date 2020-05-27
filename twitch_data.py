import yaml

data = {}
with open('config.yml') as configFile:
		data = yaml.load(configFile, Loader=yaml.FullLoader)

HOST = "irc.twitch.tv"
PORT = 6697

NICK = data["twitch"]["bot-name"]
PASS = data["twitch"]["irc-token"]
CHAN = data["twitch"]["channel"].lower()

RATE = (20/30)

API = data["twitch"]["irc-token"]

oplist = {}
userlist = {}