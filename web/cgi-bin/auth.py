#!/usr/bin/env python3
import os
import cgi
import html
import time
import random
import json
import sqlite3
import hashlib

from http import cookies

cookie = cookies.SimpleCookie(os.environ['HTTP_COOKIE'])
session = cookie.get("session")
if session is not None:
    print("Content-type: text/html\r\n\r\n")
    print("<meta http-equiv=\"refresh\" content=\"0;url=/home\" /> ")
else:
    
    form = cgi.FieldStorage()
    
    login = form.getfirst("login", None)
    passwd = form.getfirst("password", None)
    
    if login == None or passwd == None:
        print(f"Set-cookie: auth=failed:406")
        print("Content-type: text/html\r\n\r\n")
        print("<meta http-equiv=\"refresh\" content=\"0;url=/login.html\" /> ")
    
    
    post_remeber = form.getfirst("remeber", False)
    post_login = html.escape(login)
    post_passwd = html.escape(passwd)
    post_passHash = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    
    
    
    db = sqlite3.connect('web/data/data.db')
    cursor = db.cursor()
    
    cursor.execute(f"SELECT * FROM users WHERE username=?", (login,))
    results = cursor.fetchall()
    
    try:
        results = results[0]
    except IndexError:
        db.close()
        print(f"Set-cookie: auth=failed:404")
        print("Content-type: text/html\r\n\r\n")
        print("<meta http-equiv=\"refresh\" content=\"0;url=/login.html\" /> ")
        
    
    db_id = results[0]
    db_username = results[1]
    db_passwd = results[2]
    db_cookie = results[3]
    
    if len(db_passwd) < 64:
        #Automatic hashing password from database
        db_passwd = hashlib.sha256(db_passwd.encode('utf-8')).hexdigest()
        cursor.execute("UPDATE users SET password=? WHERE username=?", (db_passwd, login))
        db.commit()
    if db_passwd == post_passHash:
        cookie = str(time.time()) + str(random.randrange(10**14))
        cursor.execute("UPDATE users SET cookie=? WHERE username=?", (cookie, login))
        db.commit()
        data = f"{login}:{time.time()//10}:{cookie}"
        if post_remeber:
            expires = f"expires={time.ctime(time.time()+604800)};"#+ 7 day
        else:
            expires = ""
        
        if login and passwd != None:
            db.close()
            print(f"Set-cookie: session={data}; {expires}")
            print(f"Set-cookie: auth=done")
            print("Content-type: text/html\r\n\r\n")
            print("<meta http-equiv=\"refresh\" content=\"0;url=/home\" /> ")
    else:
        db.close()
        print(f"Set-cookie: auth=failed:405")
        print("Content-type: text/html\r\n\r\n")
        print("<meta http-equiv=\"refresh\" content=\"0;url=/login.html\" /> ")