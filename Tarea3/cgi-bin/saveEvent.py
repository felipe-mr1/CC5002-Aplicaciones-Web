#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import html

cgitb.enable()
from eventDB import Event


print('Content-type: text/html; charset=UTF-8')
print('')
#print('Content-type: text/html\r\n\r\n')
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)

form = cgi.FieldStorage()
edb = Event('localhost', 'root', '', 'tarea2')
#edb = Event('localhost', 'cc500226_u', 'ellentesqu', 'cc500226_db')

# Agragar los valores opcionales
data = (
    form.getfirst('region'), form.getfirst('comuna'), form.getfirst('sector'), form.getfirst('nombre'),
    form.getfirst('email'), form.getfirst('celular'), form['red-social'], form['red-social-url'],
    form.getfirst('dia-hora-inicio'), form.getfirst('dia-hora-termino'), form.getfirst('descripcion-evento'),
    form.getfirst('tipo-comida'), form['foto-comida']
)

edb.saveEvent(data)
recent_events = edb.getRecentEvents()

listOfEvents = edb.getListOfEvents(0)
nextEvents = edb.getListOfEvents(2)
allEvents = edb.getAllEvents()

html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=home.py"/>
    <title>Tichen</title>
    <link rel="stylesheet" href="../style-v.css">
    <script type="text/javascript">
            window.location.href = "home.py"
    </script>
</head>
<body>

<h1>Si no fue redirigido a la pagina principal haga click en este boton</h1>
<button type="button" onclick="home.py">Click</button>

'''

body2=f'''
<script src="../validation.js"></script>

</body>
</html>
'''

print(html, file=utf8stdout)
print(body2,file=utf8stdout)


