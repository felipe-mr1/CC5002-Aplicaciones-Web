#!/usr/bin/python3
# -*- coding: utf-8 -*-
def inputError(msg):
    #!/usr/bin/python3
    # -*- coding: utf-8 -*-
    #print('Content-type: text/html\r\n\r\n')
    utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Tichen</title>
            <link rel="stylesheet" href="../style.css">
        </head>
        <body>
        <h1>Error en formulario: {msg}</h1>
        <a class = "button button1" href="home.py">Volver al inicio</a>
        </body>
        </html>
    '''
    print(html, file=utf8stdout)
    exit()