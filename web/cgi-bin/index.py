#!/usr/bin/env python3
import os, cgi

print("Content-type: text/html\r\n\r\n")
url = os.environ['SESSION_URI'][1:]
print(os.environ['SESSION_URI'])

def loadPage(page):
	if f"{page}.html" in os.listdir('web/pages/'):
		with open(f'web/pages/{page}.html') as contentFile:
			htmlContents = contentFile.read()
		print(html.read().format(
			page_name="Home",
			user_name="XpycTee",
			user_menu1="Menu 1",
			user_menu2="Menu 2",
			contents=htmlContents))

for param in os.environ.keys():
	print("<b>%20s</b>: %s<br>" % (param, os.environ[param]))
with open('web/index.html') as html:
	htmlContents = ""
	url_get = url.split("?")
	url_split = url_get[0].split("/")
	print(f'{url_split} {os.listdir("web/pages/")}')
	page = url_split[0]
	if page == "":
		loadPage("home")
	loadPage(page)

	
