import Data

def starter():
	Data.Mods.globData["memeCounter"] = { "emoteСoincident": { "count" : 0, "emote" : None } }

def responder(message, username):
	print(Data.Mods.globData["memeCounter"])

	def emoteFind(message):
		splitedMsg = message.split(" ")
		for emoteFind in splitedMsg:
			if emoteFind in Data.Chat.emotes:
				return emoteFind

	emote = emoteFind(message.strip())

	prevEmote = Data.Mods.globData["memeCounter"]["emoteСoincident"]["emote"]

	count = Data.Mods.globData["memeCounter"]["emoteСoincident"]["count"]
	if emote != prevEmote:
		Data.Mods.globData["memeCounter"]["emoteСoincident"]["count"] = 1
		Data.Mods.globData["memeCounter"]["emoteСoincident"]["emote"] = emote
		if prevEmote != None and count >= 3:
			return f"{prevEmote} x{count}"
	else:
		if prevEmote != None:
			Data.Mods.globData["memeCounter"]["emoteСoincident"]["count"] += 1
		return



