import sys, os, types, importlib, datetime, subprocess, time, ssl, socket, re, json, yaml, threading

import urllib.request as urllib
from time import sleep

import twitch_data as twitch
import modules, utils
from modules import *

def sock_connecting():
	tcp_sock = socket.socket()
	ssl_sock = ssl.wrap_socket(tcp_sock)
	ssl_sock.connect((twitch.HOST, twitch.PORT))
	ssl_sock.send("PASS oauth:{}\r\n".format(twitch.PASS).encode("utf-8"))
	ssl_sock.send("NICK {}\r\n".format(twitch.NICK).encode("utf-8"))
	ssl_sock.send("JOIN #{}\r\n".format(twitch.CHAN).encode("utf-8"))
	return ssl_sock

def reload_package(package):
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

def main():
	connected = False
	while connected != True:
		try:
			sock = sock_connecting()
			connected = True
		except:
			utils.logging_all("Нет соеденения")
			sleep(1)

	modulesList = {}
	with open('modules.yml') as modulesFile:
		modulesList = yaml.load(modulesFile, Loader=yaml.FullLoader)
	for file in os.listdir(".\\modules"):
		if file != "__init__.py":
			if file.endswith(".py"):
				for module in list(modulesList['modules']):
					if not f'{module}.py' in os.listdir(".\\modules"):
						del modulesList['modules'][module]
				if not file.replace('.py', '') in modulesList['modules']:
					modulesList['modules'][file.replace('.py', '')] = {'enabled': True}
	with open('modules.yml', 'w') as modulesFile:
		modulesData = yaml.dump(modulesList, modulesFile)

	if utils.settings['logging']['file']:
		if not 'log' in os.listdir():
			os.mkdir('log')

	chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

	fillOPThread = threading.Thread(target=utils.fillOpList)
	fillOPThread.start()

	for module in modulesList['modules']:
		utils.logging_all(str(module))
		if modulesList['modules'][module]['enabled']:
			try:
				execFunc = getattr(globals()[module], "starter")
				execFThread = threading.Thread(target=execFunc)
				execFThread.start()
			except:
				pass

	def execModule(message, username):
		for module in modulesList['modules']:
			if modulesList['modules'][module]['enabled']:
				execFunc = getattr(globals()[module], "responder")
				username = utils.reqAPItwitch(f'https://api.twitch.tv/kraken/users?login={username}')['users'][0]['display_name']
				ret = execFunc(message, username)
				if ret != None:
					utils.mess(sock, ret)
					break

	while True:
		sock.settimeout(360)
		try:
			response = sock.recv(1024).decode("utf-8")
		except Exception as e:
			utils.logging_all(str(e))
			utils.logging_all(str(response))
			break
		sock.settimeout(None)
		if response == "PING :tmi.twitch.tv\r\n":
			sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
		else: 
			try:
				username = re.search(r"\w+", response).group(0)
				message = chat_message.sub("", response)
			except Exception as e:
				utils.logging_all(str(e))
				utils.logging_all(str(response))
				break

			if username != "tmi":
				execMThread = threading.Thread(target=execModule, args=(message,username,))
				execMThread.start()

			utils.logging_all(f"{username.strip()}: {message.strip()}")
	return True

reloading = True
while reloading:
	if __name__ == "__main__":
		with open('config.yml') as configFile:
			utils.settings = yaml.load(configFile, Loader=yaml.FullLoader)['settings']
		reload_package(modules)
		reloading = main()