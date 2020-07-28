#!/usr/bin/python3
import sys
import os
import time
import ssl
import socket
import re
import json
import yaml
import threading
import requests
import urllib.request as urllib
from time import sleep

from web import server
import Data
import modules
from modules import *

def initWebFig():
    
    ip = Data.Bot.settings['web']['ip_address']

    port = int(Data.Bot.settings['web']['tcp_port'])
    serv = server.Server(ip,port)
    threading.Thread(target=serv.startServer).start()

    sslEnabled = Data.Bot.settings['web']['ssl']['enabled']
    port = int(Data.Bot.settings['web']['ssl']['tcp_port'])
    serv = server.Server(ip,port,sslEnabled)
    threading.Thread(target=serv.startServer).start()

def sock_connecting():
    """
        Function for connecting to Twitch Chat
        return socket of connection
    """
    tcp_sock = socket.socket()
    ssl_sock = ssl.wrap_socket(tcp_sock)
    ssl_sock.connect((Data.Twitch.HOST, Data.Twitch.PORT))
    ssl_sock.send("PASS oauth:{}\r\n".format(Data.Twitch.PASS).encode("utf-8"))
    ssl_sock.send("NICK {}\r\n".format(Data.Twitch.NICK).encode("utf-8"))
    ssl_sock.send("JOIN #{}\r\n".format(Data.Twitch.CHAN).encode("utf-8"))
    return ssl_sock

def main():
    """
        Main function
    """
    connected = False
    while connected != True:
        try:
            sock = sock_connecting()
            connected = True
        except ConnectionRefusedError:
            Data.Bot.logging_all("Нет соеденения")
            sleep(10)

    if Data.Bot.settings['logging']['file']:
        if not 'log' in os.listdir():
            os.mkdir('log')

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    fillOPThread = threading.Thread(target=Data.Bot.fill_opList)
    fillOPThread.start()

    Data.Stream.channel_ID = Data.TwitchAPI.request(f'https://api.twitch.tv/kraken/users?login={Data.Twitch.CHAN}')['users'][0]['_id']    

    
    modulesList = Data.Bot.getModulesList()
    for module in modulesList['modules']:
        if modulesList['modules'][module]['enabled']:
            status = "enabled"
        else:
            status = "disabled"
        Data.Bot.logging_all(f"Module: {str(module)} status: {status}")

        if modulesList['modules'][module]['enabled']:
            Data.Mods.globData[module] = {}
            try:
                execFunc = getattr(globals()[module], "starter")
                execFThread = threading.Thread(target=execFunc)
                execFThread.start()
            except AttributeError:
                pass
            

    def execModule(message, username):
        for module in modulesList['modules']:
            if modulesList['modules'][module]['enabled']:
                try:
                    execFunc = getattr(globals()[module], "responder")
                except AttributeError:
                    break
                if not username in Data.Chat.userlist:
                    user = Data.TwitchAPI.request(f'https://api.twitch.tv/kraken/users?login={username}')['users'][0]
                    Data.Chat.userlist.update({ username : { "display_name" : user['display_name'], "_id" :  user['_id'] } })
                diplay_username = Data.Chat.userlist[username]['display_name']
                ret = execFunc(message, diplay_username)
                if ret != None:
                    Data.Chat.sendMessage(sock, f"/me {ret}")
                    Data.Bot.logging_all(f"BOT(respond): {ret}")
                    break
    initWebFig()
    while True:
        sock.settimeout(360)
        try:
            response = sock.recv(1024).decode("utf-8")
        except KeyboardInterrupt:
            Data.Bot.logging_all("Script has interrupted")
            return False
        except Exception as e:
            Data.Bot.logging_all(str(e))
            Data.Bot.logging_all(str(response))
            break
        sock.settimeout(None)
        if response == "PING :tmi.twitch.tv\r\n":
            sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else: 
            try:
                username = re.search(r"\w+", response).group(0)
                message = chat_message.sub("", response)
            except Exception as e:
                Data.Bot.logging_all(str(e))
                Data.Bot.logging_all(str(response))
                break

            if username != "tmi" and (username != Data.Twitch.NICK.lower() or username == "xpyctee"):
                execMThread = threading.Thread(target=execModule, args=(message,username,))
                execMThread.start()

                Data.Bot.logging_all(f"{username.strip()}: {message.strip()}")
    return True

reloading = True
while reloading:
    if __name__ == "__main__":
        with open('config.yml') as configFile:
            Data.Bot.settings = yaml.load(configFile, Loader=yaml.FullLoader)['settings']
        Data.Bot.reload_module(modules)
        reloading = main()