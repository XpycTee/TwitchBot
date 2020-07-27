import Data

def starter():
    Data.Mods.globData["memeCounter"] = { "emoteСoincident": { "count" : 0, "emote" : None } }
    Data.Chat.loadEmotIcons()

def responder(message, username):

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



