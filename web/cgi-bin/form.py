#!/usr/bin/env python3
import cgi, html

form = cgi.FieldStorage()
text1 = form.getfirst("TEXT_1", "не задано")
text2 = form.getfirst("TEXT_2", "не задано")
text1 = html.escape(text1)
text2 = html.escape(text2)
#!/usr/bin/env python3
print("Content-type: text/html")
print()
with open('web/index.html') as html:
	htmlContents = """<div class="mdl-color--white mdl-shadow--2dp mdl-cell mdl-cell--12-col mdl-grid">
		<h1>Обработка данных форм!</h1><br>
		<p>TEXT_1: {text_1}</p><br>
		<p>TEXT_2: {text_2}</p><br>
	</div>"""
	
	print(html.read().format(page_name="Form response", current_name="XpycTee", another_name="Biba", contents=htmlContents.format(text_1=text1,text_2=text2)))