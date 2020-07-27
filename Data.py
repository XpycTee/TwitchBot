import yaml
import os
import json
import requests
import time
import _thread
import datetime
import importlib
import types

import urllib.request as urllib
from time import sleep


def declensionNumsRus(number, singlNomin, singlGeni, pluralGeni):
    """ 
        The function of "the Declension of the noun by the numbers" for Russian language
        - number: the number for which there is a decline
        - singlNomin: singular nominative declinable noun
        - singlGeni: singular genitive declinable noun
        - pluralGeni: plural genitive declinable noun
        Return declined noun
    """
    if number % 10 == 1:
        result = singlNomin
    if number % 10 >= 2 and number % 10 <= 4:
        result = singlGeni
    if (number % 10 >= 5 and number % 10 <= 9) or number % 10 == 0 or (number >= 11 and number <= 19):
        result = pluralGeni
    return result

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


class Chat(object):
    """Class of Chat on Stream"""
    class Users(object):
        """Users in chat object"""
        def isOp(user):
            """Checking whether the user is an Op"""
            if user.lower() == "xpyctee":
                return True
            return user.lower() in Twitch.oplist


    def sendMessage(sock, mess):
        """Sending message in chat"""
        sock.send("PRIVMSG #{} :{}\r\n".format(Twitch.CHAN, mess).encode("utf-8"))


    def loadEmotIcons():
        def urlRequest(url, headers = {"accept": "application/json"}):
            request = urllib.Request(url, headers=headers)
            response = urllib.urlopen(request).read().decode("utf-8")
            return response

        globsFFacezJSON = json.loads(urlRequest('https://api.frankerfacez.com/v1/set/global'))
        globsFFacezList = globsFFacezJSON["sets"][str(globsFFacezJSON["default_sets"][0])]["emoticons"]
        for FFZemIcon in globsFFacezList:
            Chat.emotes.update({ FFZemIcon["name"] : { "type" : "FrankerFaceZ" }})

        FFacezJSON = json.loads(urlRequest(f'https://api.frankerfacez.com/v1/room/{Twitch.CHAN}'))
        FFacezList = FFacezJSON["sets"][str(FFacezJSON["room"]["set"])]["emoticons"]
        for FFZemIcon in FFacezList:
            Chat.emotes.update({ FFZemIcon["name"] : { "type" : "FrankerFaceZ" }})

        Bot.logging_all("FrankerFaceZ emoticons Data Loaded")

        globsBTTVList = json.loads(urlRequest("https://api.betterttv.net/2/emotes"))["emotes"]
        for BTTVemIcon in globsBTTVList:
            Chat.emotes.update({ BTTVemIcon["code"] : { "type" : "BTTV" }})
        
        bttvList = json.loads(urlRequest(f'https://api.betterttv.net/2/channels/{Twitch.CHAN}'))["emotes"]
        for BTTVemIcon in bttvList:
            Chat.emotes.update({ BTTVemIcon["code"] : { "type" : "BTTV" }})
        Bot.logging_all("BTTV emoticons Data Loaded")

        emoticonsTwitch = TwitchAPI.request("https://api.twitch.tv/kraken/chat/emoticons")
        for emIcon in emoticonsTwitch["emoticons"]:
            Chat.emotes.update({emIcon["regex"] : { "type" : "Twitch" }})# "id": emIcon["id"], "images": emIcon["images"] } })
        emoticonsTwitch.clear()
        Bot.logging_all("All Twitch emoticons Data Loaded")


    emotes = {}
    userlist = {}
        
class Mods(object):

    commands = {}
    globData = {}


class Bot(object):

    def remove_module(modname, paranoid=None):
        """Thanks for Dick Moores https://mail.python.org/pipermail/tutor/2006-August/048596.html"""
        from sys import modules
        try:
            thismod = modules[modname]
        except KeyError:
            raise ValueError(modname)
        these_symbols = dir(thismod)
        if paranoid:
            try:
                paranoid[:]  # sequence support
            except:
                raise ValueError('must supply a finite list for paranoid')
            else:
                these_symbols = paranoid[:]
        del modules[modname]
        for mod in modules.values():
            try:
                delattr(mod, modname)
            except AttributeError:
                pass
            if paranoid:
                for symbol in these_symbols:
                    if symbol[:2] == '__':  # ignore special symbols
                        continue
                    try:
                        delattr(mod, symbol)
                    except AttributeError:
                        pass


    def reload_module(package):
        assert(hasattr(package, "__package__"))
        fn = package.__file__
        fn_dir = os.path.dirname(fn) + os.sep
        module_visit = {fn}
        del fn
        def reload_recursive_ex(module):
            importlib.reload(module)
            for module_child in vars(module).values():
                if isinstance(module_child, types.ModuleType):
                    fn_child = getattr(module_child, "__file__", None)
                    if (fn_child is not None) and fn_child.startswith(fn_dir):
                        if fn_child not in module_visit:
                            module_visit.add(fn_child)
                            reload_recursive_ex(module_child)
        return reload_recursive_ex(package)


    def getModulesList():
        modulesList = {}
        if not 'modules.yml' in os.listdir():
            with open('modules.yml', 'w') as modulesFile:
                modulesList = yaml.load(modulesFile, Loader=yaml.FullLoader)
        with open('modules.yml', 'r+') as modulesFile:
            modulesList = yaml.load(modulesFile, Loader=yaml.FullLoader)
            if modulesList == None:
                modulesList = {"modules":{"None":None}}
            for file in os.listdir("modules"):
                if file != "__init__.py":
                    if file.endswith(".py"):
                        if not file.replace('.py', '') in modulesList['modules']:
                            modulesList['modules'][file.replace('.py', '')] = {'enabled': True}
                        for module in list(modulesList['modules']):
                            if not f'{module}.py' in os.listdir("modules"):
                                del modulesList['modules'][module]
        with open('modules.yml', 'w') as modulesFile:
            modulesData = yaml.dump(modulesList, modulesFile)
        return modulesList


    def moduleFolder(modName):
        if not modName.replace('modules.', '') in os.listdir("modules"):
            modFolderName = modName.replace('modules.', '')
            os.mkdir(f"modules/{modFolderName}")
            return f"modules/{modFolderName}"
        else:
            modFolderName = modName.replace('modules.', '')
            return f"modules/{modFolderName}"
    

    def logging_all(message):
        Bot.logging_inFile(message)
        Bot.logging_inLive(message)
    

    def logging_inLive(message):
        if Bot.settings['logging']['live']:
            timeNow = time.strftime("%H.%M.%S", time.localtime())
            print(f"{timeNow} {message}")
    

    def logging_inFile(message):
        if Bot.settings['logging']['file']:
            if not 'log' in os.listdir():
                os.mkdir('log')
            today = datetime.datetime.today()
            timeNow = time.strftime("%H.%M.%S", time.localtime())
            with open(f'log/log_{today.strftime("%Y-%m-%d")}.log', 'a', encoding='utf-8') as log_file:
                log_file.write(f"{timeNow} {message}\n")
    

    def fill_opList():
        while True:
            try:
                url = f'http://tmi.twitch.tv/group/user/{Twitch.CHAN}/chatters'
                req = urllib.Request(url, headers={"accept": "*/*"})
                res = urllib.urlopen(req).read()
                Twitch.oplist.clear()
                data = json.loads(res) 
                for p in data["chatters"]["broadcaster"]:
                    Twitch.oplist[p] = "broadcaster"
                for p in data["chatters"]["moderators"]:
                    Twitch.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    Twitch.oplist[p] = "global_mods"
                for p in data["chatters"]["admins"]:
                    Twitch.oplist[p] = "admins"
                for p in data["chatters"]["staff"]:
                    Twitch.oplist[p] = "staff"
            except:
                "Something went wrong...do nothing"
                #logging_all("Something went wrong...do nothing")
            sleep(5)

        settings = {}


class Stream(object):
    """ class of Stream on Twitch """

    def isLive():
        """Get Stream Status"""
        stream = Stream.requestData()
        #Bot.logging_all(stream)
        if stream["stream"] != None:
            return True
        else:
            return False


    def requestData():
        """Request Stream Data from Twitch Kraken API"""
        url = f'https://api.twitch.tv/kraken/streams/{Stream.channel_ID}'
        return TwitchAPI.request(url)

    channel_ID = ""


class TwitchAPI(object):

    def request(url):
        req = ""
        if Twitch.API == "":
            req = requests.get(url, headers = {"Authorization" : f"OAuth {Twitch.PASS}", "Accept" : "application/vnd.twitchtv.v5+json"})
        else:
            req = requests.get(url, headers = {"Client-ID" : Twitch.API, "Accept" : "application/vnd.twitchtv.v5+json"})
        req.raise_for_status()
        return req.json()