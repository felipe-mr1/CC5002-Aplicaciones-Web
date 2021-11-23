-- insertar evento:
INSERT INTO evento (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion, tipo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
-- ejemplo: 
-- INSERT INTO evento (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion, tipo) VALUES (130606, 'Estadio Comunal', 'Don Manolo', 'info@donmanolo.cl', '+56955555555', '2021-09-28 13:00', '2021-09-28 19:00', 'ricos sandwiches', 'Sándwiches');

-- insertar red social:
INSERT INTO red_social (nombre, identificador, evento_id) VALUES (?, ?, ?);
-- ejemplo:
-- INSERT INTO red_social (nombre, identificador, evento_id) VALUES ('instagram', 'https://www.instagram.com/donmanolo/', 1);

-- insertar foto:
INSERT INTO foto (ruta_archivo, nombre_archivo, evento_id) VALUES (?, ?, ?);
-- ejemplo:
-- INSERT INTO foto (ruta_archivo, nombre_archivo, evento_id ) VALUES ('/Users/jourzua/personal/DCC/51t/python/archivos/', 'foto-lomito-mayo.jpg', 1);

-- seleccionar eventos:
SELECT id, comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion, tipo FROM evento
-- seleccionar ultimos 5 eventos ordenados por fecha de inicio descendente:
SELECT id, comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion, tipo FROM evento ORDER BY dia_hora_inicio DESC LIMIT 5

-- seleccionar redes sociales de un evento
SELECT id, nombre, identificador, evento_id FROM red_social WHERE evento_id=?

-- seleccionar información de la fotos de un evento:
SELECT id, ruta_archivo, nombre_archivo, evento_id FROM foto WHERE evento_id=?

