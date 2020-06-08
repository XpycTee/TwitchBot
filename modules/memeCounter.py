import Data

def responder(message, username):
	def emoteFind(message):
		splitedMsg = message.split(" ")
		for emoteFind in splitedMsg:
			if emoteFind in Data.Chat.emotes:
				return emoteFind

	histMsges = Data.Chat.historyMessages[::-1]

	if len(histMsges) < 2:
		return

	emote = emoteFind(message.strip())
	prevEmote = emoteFind(histMsges[0].strip())

	if prevEmote == None:
		return

	count = 0
	if emote != prevEmote:
		for i in range(0, len(histMsges)):
			if prevEmote in histMsges[i].split(" "):
				count += 1
			else:
				if count >= 3:
					return f"{prevEmote} x{count}"
				else:
					return 
