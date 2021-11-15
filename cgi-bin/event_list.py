#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import cgi
import cgitb
import math
from database import Database
from validate import *

cgitb.enable()
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)
page = int(cgi.FieldStorage()["page"].value)
db = Database()
total_events = db.get_last_evento_id() if db.get_last_evento_id() is not None else 0
max_page = math.ceil(total_events/5)-1
data = db.get_event_list_data(page)

print('Content-type: text/html; charset=UTF-8')
print('')

utf8stdout.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../styles/event_list.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    <title>Ventas Comida Casera</title>
</head>
<body>
    <div class="header">
        <a href="./home.py"><h1 class="header-title">Ventas de Comida Casera</h1></a>
        <ul class="nav-bar">
            <li class="nav-item"><a class="nav-link" href="../event_form.html">Informar evento</a></li>
            <li class="nav-item"><a class="nav-link" href="./event_list.py?page=0">Listado de eventos</a></li>
            <li class="nav-item"><a class="nav-link" href="./statistics.py">Estadisticas</a></li>
        </ul>
    </div>
    <div class="content">
        <div class="info-box">
            <div class="text-box">
                <h1>Listado de Eventos</h1>
''')
msg = ''''''
if len(data) == 0:
    msg += '''
            <p>Ups! Parece que todavia no hay eventos registados!</p>
            <img style="padding-top: 0;" src="../img/notfound.png" height="450">'''
else:
    msg += '''
                <p>Aquí tienes el listado de eventos de venta de comida, puedes desplazarte mediante las flechas.</p>          
                </div>
                <div class="table-box">
                    <table>
                        <table>
                        <thead>
                            <tr>
                                <th>Fecha - hora inicio</th>
                                <th>Fecha - hora término</th>
                                <th>Comuna</th>
                                <th>Sector</th>
                                <th>Tipo comida</th>
                                <th>Nombre contacto</th>
                                <th>Total fotos</th>
                            </tr>
                        </thead>
                        <tbody>
    '''
    for t in data:
        (evento_id, d_h_i, d_h_t, nombre_com, sector, tipo, descripcion, nombre_contacto, ruta_archivo, total_fotos) = t
        msg += f'''     
                            <tr class="clickable-row" onclick="window.location.href = './event_info.py?evento_id={evento_id}'">
                                <td>{d_h_i}</td>
                                <td>{d_h_t}</td>
                                <td>{nombre_com}</td>
                                <td>{sector}</td>
                                <td>{tipo}: {descripcion}</td>
                                <td>{nombre_contacto}</td>
                                <td>{total_fotos}</td>
                            </tr>
                        '''
    msg += '''    
                        </tbody>
                    </table>
                </div>
                <br>
                <div class="btn-container">
            '''


if (page==0):
	if (max_page>0):
		msg += f'''
	        	    <a class="btn" href="./event_list.py?page={page + 1}">Siguiente</a>
		'''
elif (page>0 and page<max_page):
	msg += f'''
            <a class="btn" href="./event_list.py?page={page - 1}">Anterior</a>
            <a class="btn" href="./event_list.py?page={page + 1}">Siguiente</a>
	'''
else:
	msg += f'''
            <a class="btn" href="./event_list.py?page={page - 1}">Anterior</a>
	'''

utf8stdout.write(msg)
utf8stdout.write('''
            </div>
        </div>
    </div>
    <div class="footer"></div>
</body>
</html>
''')
