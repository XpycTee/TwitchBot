#!/usr/bin/env python3
import os, cgi
field = cgi.FieldStorage()
print("Content-type: text/html")
print()
print(field)
with open('web/index.html') as html:
	htmlContents = ""
	with open('web/pages/home.html') as homeFile:
		htmlContents = homeFile.read()
	print(html.read().format(
		page_name="Home",
		user_name="XpycTee",
		user_menu1="Menu 1",
		user_menu2="Menu 2",
		contents=htmlContents))