import utils
import ssl, socket, json, re, yaml
import time, _thread
import sys, os, types, importlib
import subprocess
import twitch_data as twitch
import urllib.request as urllib
from time import sleep
import modules
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
                        # print("reloading:", fn_child, "from", module)
                        module_visit.add(fn_child)
                        reload_recursive_ex(module_child)



    return reload_recursive_ex(package)

def main():
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




	connected = False
	while connected != True:
		try:
			ssl_sock = sock_connecting()
			connected = True
		except:
			print("Нет соеденения")
			sleep(1)


	chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
	#utils.mess(ssl_sock, "Здрова, Всем! KonCha <3")

	_thread.start_new_thread(utils.fillOpList, ())
	#_thread.start_new_thread(waitCLI, (ssl_sock,))
	while True:
		response = ssl_sock.recv(1024).decode("utf-8")
		if response == "PING :tmi.twitch.tv\r\n":
			ssl_sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
		else: 
			username = re.search(r"\w+", response).group(0)
			message = chat_message.sub("", response)
			print(username.strip()+": "+message.strip())
			if (message.strip() == "!reload" and utils.isOp(username)):
				utils.mess(ssl_sock, "Перезагрузка бота")
				break

			for module in modulesList['modules']:
				if modulesList['modules'][module]['enabled']:
					execFunc = getattr(globals()[module], "execute")
					ret = execFunc(message, username)
					if ret != None:
						utils.mess(ssl_sock, ret)
						break
		sleep(0.1)
	return True

def waitCLI(sock):
	cliMsg = input(">")
	utils.mess(sock, f"{cliMsg}")
	waitCLI(sock)

reloading = True
while reloading:
	if __name__ == "__main__":
		reload_package(modules)
		reloading = main()