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
    <title>Tichen</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>

<div class="title black">¡Bienvenid@ a Tichen!</div>
<div class="subtitle">Panoramas de comida</div>

<div class="b_container">
    <button class="button button1" onclick="notifyEvent()" id="btn1">Informar evento</button>
    <button class="button button2" onclick="showEvents()" id="btn2">Ver listado de eventos</button>
    <button class="button button3" onclick="showData()" id="btn3">Estadísticas</button>
</div>

<div id="sheetEvent">
    <form method="post" action="saveEvent.py" onsubmit="return validateForm()" enctype="multipart/form-data">
        <p>Los campos obligatorios están demarcados con *</p>
        <p class="subtitle">¿Dónde?</p>
        <div class="entrada">
            <div class="leyenda">Región *</div>
            <label for="region"></label><select name="region" id="region" onchange="getComuna()" required="required">
                <option value="" selected="selected">Seleccione Region</option>
            </select>
        </div>
        <div class="entrada">
            <div class="leyenda">Comuna *</div>
            <label for="comuna"></label><select name="comuna" id="comuna" required="required">
                <option value="" selected="selected">Seleccione comuna</option>
            </select>
        </div>
        <div class="entrada formfield">
            <div class="leyenda">Sector</div>
            <label for="sector"></label><input type="text" size="100" name="sector" id="sector" maxlength="100">
        </div>
        <p class="subtitle">¿Quién?</p>
        <div class="entrada">
            <div class="leyenda">Nombre *</div>
            <input type="text" id="nombre" name="nombre" size="100" required="required" maxlength="200">
        </div>
        <div class="entrada">
            <div class="leyenda">e-mail *</div>
            <input type="text" id="email" name="email" size="100" required="required">
        </div>
        <div class="entrada">
            <div class="leyenda">Número de celular</div>
            <input type="text" id="celular" name="celular" size="15">
        </div>
        <div class="entrada formfield">
            <div class="leyenda">Redes Sociales</div>
            <select id="red-social" name="red-social">
                <option value="" selected="selected">Seleccione su red-social (máx 5)</option>
                <option value="Twitter" >Twitter</option>
                <option value="Instagram" >Instagram</option>
                <option value="Facebook" >Facebook</option>
                <option value="Tik-tok" >Tik-tok</option>
                <option value="Otra" >Otra</option>
            </select>
            <input type="text" name="red-social-url" id="red-social-url">
            <div id="redesSociales"></div>
            <button class="button" type="button" onclick="socialNetworks()">Agregar Red Social</button>
        </div>
        <p class="subtitle">¿Cuándo y qué se ofrece?</p>
        <div class="entrada">
            <div class="leyenda">Día hora de inicio *</div>
            <input type="text" size="20" placeholder="aaaa-mm-dd hora:minuto" id="dia-hora-inicio" name="dia-hora-inicio"
                   onchange="refillDate()" required="required">
        </div>
        <div class="entrada">
            <div class="leyenda">Día hora de termino *</div>
            <input type="text" size="20" placeholder="aaaa-mm-dd hora:minuto" id="dia-hora-termino" name="dia-hora-termino" required="required">
        </div>
        <div class="entrada formfield">
            <div class="leyenda">Descripción</div>
            <textarea cols="50" rows="10" placeholder="Detalles del evento" id="descripcion-evento" name="descripcion-evento"></textarea>
        </div>
        <div class="entrada">
            <div class="leyenda">Tipo de comida *</div>
            <select id="tipo-comida" name="tipo-comida" required="required">
                <option value="" selected="selected">Seleccione una opcion</option>
            </select>
        </div>
        <div class="entrada">
            <div class="leyenda">Fotografía *</div>

            <input type="file" accept="image/png, image/jpg" required="required" id="foto-comida" name="foto-comida">
            <button onclick="AddPhoto()" type="button">Agregar Foto</button>
            <div id="photos"></div>

        </div>
        <div class="entrada">
            <button class="button" onclick="confirmation()" type="button">Enviar información de este evento</button>
            <div class="b_container" id="confirmation"></div>
        </div>
    </form>
</div>

<div id="dataInfo">
    <h1>En esta sección se presenta algunas estadísticas de este sitio.</h1>
        <h2>A continuación la cantidad de eventos inscritos el mes pasado:</h2>
    <img class="center" src="https://imgur.com/2czgevV.png" width="620" height="480" alt="grafico de linea">
        <h2>Cantidad de eventos por tipo en el mes de Agosto:</h2>
    <img class="center" src="https://i.imgur.com/fnKdXXn.png" width="620" height="480" alt="grafico de torta">
        <h2>Cantidad de eventos inscritos el año anterior:</h2>
    <img class="center" src="https://i.imgur.com/6lKqaZl.png" width="620" height="480" alt="grafico de barras"><br>
    <a href="Tichen.html">Volver al inicio</a>
</div>

<div id="listEvent">
    <div id="zoomedPhoto"></div>
    <div id="eventInfo"></div>
    <table class="my_table">
        <tr>
            <th>Fecha - Hora inicio</th>
            <th>Fecha - Hora termino</th>
            <th>Comuna</th>
            <th>Sector</th>
            <th>Tipo de comida</th>
            <th>Nombre de contacto</th>
            <th>Total fotos</th>
        </tr>
'''

row1 = ""
for event in listOfEvents:
    red_social = str(edb.getSocialNetwork(event[0])[0][0])
    comuna = str(edb.getComuna(event[3])[0][0])
    file_path = "../media/" + str(edb.getPhoto(event[0])[0][0])
    numberOfPhotos = int(edb.getNumberPhotos(event[0])[0][0])
    row1+= f'''
    <tr onclick="EventoInfo({str(event[6]), file_path})" class="clickable">
        <th>{str(event[1])}</th>
        <th>{str(event[2])}</th>
        <th>{comuna}</th>
        <th>{str(event[4])}</th>
        <th>{str(event[5])}</th>
        <th>{red_social}</th>
        <th>{numberOfPhotos}</th>
    </tr>
    '''


body1=f'''</table>
    <a href="home.py">Volver al inicio</a>
    <button class="button" onclick="">Siguiente pagina</button>
    <button class="button" onclick="">Devolver pagina</button>
</div>
<table class="my_table">
    <tr>
        <th>Fecha - Hora inicio</th>
        <th>Fecha - Hora termino</th>
        <th>Comuna</th>
        <th>Sector</th>
        <th>Tipo</th>
        <th>Foto</th>
    </tr>
'''
row = ""
for event in recent_events:
    
    file_path = "../media/" + str(edb.getPhoto(event[0])[0][0])
    comuna = str(edb.getComuna(event[3])[0][0])
    row  += f'''
        <tr>
            <th>{str(event[1])}</th>
            <th>{str(event[2])}</th>
            <th>{comuna}</th>
            <th>{str(event[4])}</th>
            <th>{str(event[5])}</th>
            <th><image src = '{file_path}' width="320" height="240" title="source: imgur.com" alt="comida china"></th>
        </tr>
    '''

body2=f'''
<script src="../valid-ation.js"></script>

</body>
</html>
'''

print(html, file=utf8stdout)
print(row1, file=utf8stdout)
print(body1, file=utf8stdout)
print(row, file=utf8stdout)
print(body2,file=utf8stdout)


