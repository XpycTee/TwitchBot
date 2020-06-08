import Data

def responder(message, username):
	if Data.Chat.countMessages["AllTime"] % 15 == 0:
		return "Здесь будет рекламное сообщение"