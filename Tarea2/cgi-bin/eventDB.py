#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import mysql.connector
import filetype
from utils import inputError
import re
import os
import hashlib
import html

MAX_FILE_SIZE = 1 * 1000000 # 1MB

class Event:
    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db.cursor()

    def saveEvent(self, data):
        
        if len(data[2]) > 100:                     # Verificamos SECTOR
            inputError('SECTOR')

        if len(data[3]) > 200:                     # Verificamos NOMBRE
            inputError('NOMBRE')

        mailRegex = r'\S+@\S+\.\S+'                # Verificamos MAIL
        if not re.match(mailRegex, data[4]):
            print(str(data[4]))
            inputError('MAIL')

        phoneRegex =  r"^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s\.-]?){6,7}$"
        if not re.match(phoneRegex, data[5]):     # Verificamos telefono
            inputError('TELEFONO')

        urlRegex = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        if isinstance(data[7], list):
            for url in data[7]:
                if not re.match(urlRegex, url.value):       # Verificamos URL
                    inputError("URL RED SOCIAL")
        else:
            if not re.match(urlRegex, data[7].value):       # Verificamos URL
                inputError("URL RED SOCIAL")
        

        dateRegex = '^\d{4}-(0[1-9]|1[0-2])-[0-3]\d\s([0-1][0-9]|2[0-3]):[0-5]\d$'
        if not re.match(dateRegex, data[8]) or not re.match(dateRegex, data[9]):  # Verificamos FECHA
            inputError('FORMATO FECHA')

        if len(data[10]) > 500:                   # Verificamos DESCRIPCION
            inputError('despcripcion')
        
        sql = f'''
        SELECT id FROM comuna WHERE nombre = '{data[1]}'
        '''

        self.cursor.execute(sql)
        comuna_id = self.cursor.fetchall()
        comuna_id = str(comuna_id[0][0])

        # INSERTAMOS EVENTO
        sql = '''
        INSERT INTO evento (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion, tipo)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.cursor.execute(sql, (comuna_id, html.escape(data[2]), data[3], data[4], data[5], data[8], data[9], data[10], data[11]))
        self.db.commit()

        sql = "SELECT COUNT(id) FROM evento"
        self.cursor.execute(sql)
        evento_id = self.cursor.fetchall()[0][0]

        # INSERTAMOS FOTOS
        if isinstance(data[7], list):
            for i in range(len(data[7])):
                self.saveSocialMedia(data[6][i].value, data[7][i].value, evento_id)
        else:
            self.saveSocialMedia(data[6].value, data[7].value, evento_id)

        # INSERTAMOS REDES SOCIALES
        if isinstance(data[12], list):
            for photo in data[12]:
                self.savePhoto(photo, evento_id)
        else:
            self.savePhoto(data[12], evento_id)

    # FUNCION PARA GUARDAR REDES SOCIALES
    def saveSocialMedia(self, nombre, data_url, evento_id):
        sql = """
            INSERT INTO red_social (nombre, identificador, evento_id)
            VALUES (%s, %s, %s)
            """
        self.cursor.execute(sql, (nombre, data_url, evento_id))
        self.db.commit()

    # FUNCION PARA GUARDAR FOTOS
    def savePhoto(self, fileobj, evento_id):
        filename = fileobj.filename

        if not filename:
            inputError("Archivo no subido")

        size = os.fstat(fileobj.file.fileno()).st_size
        if size > MAX_FILE_SIZE:
            inputError("Archivo muy pesado")

        # Verificacion de FOTO
        sql = "SELECT COUNT(id) FROM foto"
        self.cursor.execute(sql)
        total = self.cursor.fetchall()[0][0] + 1 
        hash_archivo = str(total) + hashlib.sha256(filename.encode()).hexdigest()[0:30]
        filepath = os.getcwd() + '/media/' + hash_archivo

        filehandler = open(filepath, 'wb')
        filehandler.write(fileobj.file.read())
        filehandler.close()

        tipo = filetype.guess(filepath)
        fileobj.file.seek(0, 0)
        if tipo.mime != 'image/png' and tipo.mime != 'image/jpeg':
            os.remove(filepath)
            inputError("Archivo no es tipo png/jpeg")

        # INSERTAMOS FOTO
        sql = """
            INSERT INTO foto (ruta_archivo, nombre_archivo, evento_id)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(sql, (hash_archivo, filename, evento_id))
        self.db.commit() # id


    # RETORNA LOS ULTIMOS 5 EVENTOS REGISTRADOS
    def getRecentEvents(self):
        self.cursor.execute('SELECT id, dia_hora_inicio, dia_hora_termino, comuna_id, sector, tipo from evento order by id desc limit 5')
        return self.cursor.fetchall()

    # RETORNA LOS ULTIMOS 5 EVENTOS REGISTRADOS CON UN OFFSET PARA LAS PAGINAS
    def getListOfEvents(self, page):
        self.cursor.execute(f'SELECT id, dia_hora_inicio, dia_hora_termino, comuna_id, sector, tipo, descripcion from evento order by id desc limit {page}, 5')
        return self.cursor.fetchall()

    # RETORNA TODOS LOS EVENTOS
    def getAllEvents(self):
        self.cursor.execute(f'SELECT id, dia_hora_inicio, dia_hora_termino, comuna_id, sector, tipo from evento order by id desc')
        return self.cursor.fetchall()

    # RETORNA EL PATH DE LA FOTO GUARDADA
    def getPhoto(self, id):
        self.cursor.execute(f'SELECT ruta_archivo from foto where evento_id = {id}')
        return self.cursor.fetchall()

    # RETORNA EL NOMBRE DE LA COMUNA ASIGNADA AL EVENTO
    def getComuna(self, comuna_id):
        self.cursor.execute(f'SELECT nombre from comuna where id = {comuna_id}')
        return self.cursor.fetchall()

    # RETORNA LA RED SOCIAL ASOCIADA AL EVENTO
    def getSocialNetwork(self, id):
        self.cursor.execute(f'SELECT identificador from red_social where evento_id = {id}')
        return self.cursor.fetchall()

    def getNumberPhotos(self, id):
        self.cursor.execute(f'SELECT COUNT(evento_id) from foto where evento_id = {id}')
        return self.cursor.fetchall()