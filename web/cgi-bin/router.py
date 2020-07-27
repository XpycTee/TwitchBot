#!/usr/bin/env python3
import os
import cgi
import sys
from http import cookies

#sys.path.insert(0, "")
#import Data

cookie = cookies.SimpleCookie(os.environ['HTTP_COOKIE'])
session = cookie.get("session")
logined = True
if session is not None:
    session = session.value
if session is None:
    logined = False
else:
    username = session.split(":")[0]

print("Content-type: text/html\r\n\r\n")
#print(cookies.SimpleCookie(os.environ['HTTP_COOKIE'])," | ",os.environ['HTTP_COOKIE']," | ",cookie," | ",session)
url = os.environ['SESSION_URI'][1:]
if not logined:
    print("<meta http-equiv=\"refresh\" content=\"0;url=/login.html\" /> ")


def loadPage(page):
    if f"{page}.html" in os.listdir('web/pages/'):
        with open(f'web/pages/{page}.html') as contentFile:
            htmlContents = contentFile.read()
            return htmlContents

with open('web/index.html') as html:
    htmlContents = ""
    url_get = url.split("?")
    url_split = url_get[0].split("/")
    #print(f'{url_split} {os.listdir("web/pages/")}')
    page = url_split[0]
    htmlPage = html.read()
    if page == "":
        page = "home"

    page_data = {}
    if page == "bot_settings":
    	page_data = Data.Bot.settings


    pageContent = loadPage(page).format(**page_data)

    if pageContent != None:
        print(htmlPage.format(
            page_name=page.replace("_"," ").capitalize(),
            user_name=username,
            contents=pageContent))
    else:
        print(htmlPage.format(
            page_name="Error 404: Page Not Found",
            user_name=username,
            contents=loadPage("404").format(error_page=page)))