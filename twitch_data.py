import yaml
data = {}

with open('config.yml') as configFile:
		data = yaml.load(configFile, Loader=yaml.FullLoader)

HOST = "irc.twitch.tv"
PORT = 6667
NICK = data["settings"]["bot-name"]
PASS = data["settings"]["token"]
CHAN = data["settings"]["channel"]
RATE = (20/30)

oplist = {}