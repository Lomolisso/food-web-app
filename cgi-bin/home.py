#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import cgi
import cgitb
from database import Database
from validate import *

cgitb.enable()
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)
db = Database()
data = db.get_home_data()

print('Content-type: text/html; charset=UTF-8')
print('')

utf8stdout.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../styles/index.css">
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
            <li class="nav-item"><a class="nav-link" href="../statistics.html">Estadisticas</a></li>
        </ul>
    </div>
    <div class="content">
        <div class="info-box">
            <div class="text-box">
                <h1>Bienvenido!</h1>
''')
msg = ''''''
if len(data) == 0:
    msg += '''
            <p>Ups! Parece que todavia no hay eventos registados!</p>
            <img style="padding-top: 0;" src="../img/notfound.png" height="450">'''
else:
    msg += '''
                <p>Aquí tienes los últimos 5 eventos de venta de comida registrados</p>           
                </div>
                <div class="table-box">
                    <table>
                        <thead>
                            <tr>
                                <th>Fecha - hora inicio</th>
                                <th>Fecha - hora término</th>
                                <th>Comuna</th>
                                <th>Sector</th>
                                <th>Tipo</th>
                                <th>Foto</th>
                            </tr>
                        </thead>
                        <tbody>
    '''
    for t in data:
        (evento_id, d_h_i, d_h_t, nombre_com, sector, tipo, descripcion, ruta_archivo) = t
        msg += f'''     
                            <tr>
                                <td>{d_h_i}</td>
                                <td>{d_h_t}</td>
                                <td>{nombre_com}</td>
                                <td>{sector}</td>
                                <td>{tipo}: {descripcion}</td>
                                <td><img class="table-image" src="{ruta_archivo}" alt="{tipo}: {descripcion}"></td>
                            </tr>
                        '''
    msg += '''    
                        </tbody>
                    </table>
                </div>
            '''

utf8stdout.write(msg)
utf8stdout.write('''
        </div>
    </div>
    <div class="footer"></div>
</body>
</html>
''')
