#!/usr/bin/env python3
import os, cgi, html, time, random, json

form = cgi.FieldStorage()

login = form.getfirst("login", None)
passwd = form.getfirst("password", None)
remeber = form.getfirst("remeber", False)
login = html.escape(login)
passwd = html.escape(passwd)

data = f"{login}:{time.time()//10}:{str(time.time()) + str(random.randrange(10**14))}"

if remeber:
	expires = f"expires={time.ctime(time.time()+604800)};"#Wed May 18 03:33:20 2033 + 7 day
else:
	expires = ""

if login and passwd != None:
	print(f"Set-cookie: session={json.dumps(data)}; {expires} httponly")
	print("Content-type: text/html\r\n\r\n")
	print("<meta http-equiv=\"refresh\" content=\"0;url=/home\" /> ")