#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import html
import datetime

cgitb.enable()
from eventDB import Event

print('Content-type: text/html; charset=UTF-8')
print('')
#print('Content-type: text/html\r\n\r\n')
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)

edb = Event('localhost', 'root', '', 'tarea2')
#edb = Event('localhost', 'cc500226_u', 'ellentesqu', 'cc500226_db')
recent_events = edb.getRecentEvents()
listOfEvents = edb.getListOfEvents(0)

html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Tichen</title>
    <link rel="stylesheet" href="../style-v.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/flot-charts@0.8.3/jquery.flot.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
    integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
    crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
    integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
    crossorigin=""></script>
</head>
<body>

<div class="title black">¡Bienvenid@ a Tichen!</div>
<div class="subtitle">Panoramas de comida</div>

<div class="b_container">
    <button class="button button1" onclick="notifyEvent()" id="btn1">Informar evento</button>
    <button class="button button2" onclick="showEvents()" id="btn2">Ver listado de eventos</button>
    <button class="button button3" onclick="showData()" id="btn3">Estadísticas</button>
</div>

<div id="map" style="height: 180px;"></div>
<script>
    
    var mymap = L.map('map').setView([-33.45694, -70.64827], 8);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(mymap);

    let xhrM = new XMLHttpRequest();
    xhrM.open('GET', 'eventsMap.py');

    xhrM.onload = function(){
        if(xhrM.status == 200){
            let events = xhrM.responseText;
            let eventsA = JSON.parse(events.replaceAll("'", '"'));
            $.getJSON('../chile.json', function(json){
                for(let k=0; k< eventsA.length; k++){
                    for(let j = 0; j < json.length; j++){
                        if(json[j].name == eventsA[k][1]){
                            let lng = parseFloat(json[j].lng);
                            let lat = parseFloat(json[j].lat);
                            let i = eventsA[k][10];
                            let s = i.toString();
                            L.marker([lat, lng], { title: s}).addTo(mymap)
                                .bindPopup("<table><tr><th>Dia y hora inicio</th><th>Tipo de comida</th><th>Sector</th><th>Foto</th></tr>"+
                                    "<tr class='clickable' onclick='details(" + '"' + eventsA[k] + '"' + ")'><th>"+ eventsA[k][6] + "</th><th>"+ eventsA[k][9] + "</th><th>"+ eventsA[k][2] +
                                    "</th><th><img src = '../media/"+ eventsA[k][0] +"' width='50' height='50' alt='foto comida'></th></tr></table>");
                        }
                    }
                }
            });
        }
    }
    xhrM.send();
</script>

<div id = "details"></div>

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
    <h2>A continuación la cantidad de eventos inscritos:</h2>
    <div id="flot-placeholder" style="width:300px;height:150px" class="center"></div>
    <script type="text/javascript">
        function dataEventsPerDay(){
            let xhr = new XMLHttpRequest();
            xhr.open('GET', 'search.py');
            xhr.timeout = 1000;

            xhr.onload = function(){
                if(xhr.status == 200){
                    let statistics = xhr.responseText;
                    let container = document.getElementById("testeo");
                    var options = {
                        series: {
                            lines: {
                                show: true
                            },
                            points: {
                                radius: 3,
                                fill: true,
                                show: true
                            }
                        },
                        xaxis: {
                            axisLabel: "Fecha",
                            axisLabelUseCanvas: true,
                            axisLabelFontSizePixels: 12,
                            axisLabelFontFamily: 'Verdana, Arial',
                            axisLabelPadding: 10
                        },
                        yaxis: {
                            axisLabel: "Cantidad de eventos",
                            axisLabelUseCanvas: true,
                            axisLabelFontSizePixels: 12,
                            axisLabelFontFamily: 'Verdana, Arial'
                        }
                    };
                    $.plot($("#flot-placeholder"), [ JSON.parse(statistics) ], options);
                }
            }
            xhr.send();
        }
        setInterval(dataEventsPerDay, 5000);
        
    </script>
    <h2>Cantidad de eventos por tipo:</h2>
    <div id="flot-placeholder2" style="width:300px;height:150px" class="center"></div>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script src="http://static.pureexample.com/js/flot/excanvas.min.js"></script>
    <script src="http://static.pureexample.com/js/flot/jquery.flot.min.js"></script>
    <script src="http://static.pureexample.com/js/flot/jquery.flot.pie.min.js"></script>
    <script type="text/javascript">
        function typeOfEvents(){
            let xhr2 = new XMLHttpRequest();
            xhr2.open('GET', 'typeSearch.py');
            xhr2.timeout = 1000;

            xhr2.onload = function(){
                if(xhr2.status == 200){
                    let statistics2 = xhr2.responseText;
                    let something = JSON.parse(statistics2.replaceAll("'", '"'));
                    let options2 = {
                        series: {
                            pie: {
                                show: true,
                                tilt: 0.5
                            }
                        },
                        legend: {
                            show: false
                        }
                    };
                    let aux = [];
                    for (let j= 0; j < something.length; j++){
                        aux.push({ label: something[j][0], data: something[j][1] });
                    }
                    $.plot($("#flot-placeholder2"), aux, options2);
                }
            }
            xhr2.send();
        }
        setInterval(typeOfEvents, 5000);
        
    </script>
    <h2>Cantidad de eventos inscritos el año anterior:</h2>
    <img class="center" src="https://i.imgur.com/6lKqaZl.png" width="620" height="480" alt="grafico de barras"><br>
    <br>
    <a href="home.py">Volver al inicio</a>
</div>
'''

html += '''<div id="listEvent">
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

body1 = f'''   </table>
    <a href="home.py">Volver al inicio</a>
    <button class="button" onclick="">Siguiente pagina</button>
    <button class="button" onclick="">Devolver pagina</button>
    <div id="testeo"></div>
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
    

row2 = ""
for event in recent_events:
    
    file_path = "../media/" + str(edb.getPhoto(event[0])[0][0])
    comuna = str(edb.getComuna(event[3])[0][0])
    row2  += f'''
        <tr>
            <th>{str(event[1])}</th>
            <th>{str(event[2])}</th>
            <th>{comuna}</th>
            <th>{str(event[4])}</th>
            <th>{str(event[5])}</th>
            <th><img src = '{file_path}' width="320" height="240" title="source: imgur.com" alt="comida foto"></th>
        </tr>
    '''

body2=f'''
</table>
<script src="../validation.js"></script>

</body>
</html>
'''

print(html, file=utf8stdout)
print(row1, file=utf8stdout)
print(body1, file=utf8stdout)
print(row2, file=utf8stdout)
print(body2, file=utf8stdout)

