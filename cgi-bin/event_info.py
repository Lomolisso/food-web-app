#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import cgi
import cgitb
from database import Database
from validate import *

cgitb.enable()
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)
evento_id = int(cgi.FieldStorage()["evento_id"].value)
db = Database()

# Recuperamos informacion de la base de datos:
(evento_id, comuna_id, sector, nombre, email, celular, d_h_i, d_h_t, desc, tipo) = db.get_event_info(evento_id)
datos_comuna = db.get_comuna_data(comuna_id)
comuna = datos_comuna[0]
region = db.get_region_name(datos_comuna[1])
rrss_evento = db.get_event_sn(evento_id)
fotos_evento = db.get_event_photos(evento_id)

print('Content-type: text/html; charset=UTF-8')
print('')

html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../styles/event_info.css">
    <link rel="stylesheet" href="../styles/image.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    <title>Informar evento</title>
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
        <!-- INFO BOX: CAJA DEL CONTENIDO PRINCIPAL -->
        <div class="info-box">
            <div class="text-box">
                <h1>Informacion Evento</h1>
                <p>A continuacion se indica toda la informacion sobre el evento seleccionado.</p>           
            </div>
            <div id="event-info">
                <h1 class="section-title">Información del lugar</h1>
                <hr class="section-separator">
                <div class="section-info">
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Región<p>
                        </div>
                        <div class="info-right">
                            <p>{region}</p>
                        </div>
                    </div>
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Comuna</p>
                        </div>
                        <div class="info-right">
                            <p>{comuna}</p>
                        </div>
                    </div>
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Sector<p>
                        </div>
                        <div class="info-right">
                            <p>{sector}</p>
                        </div>
                    </div>
                </div>
                <h1 class="section-title">Datos del oferente</h1>
                <hr class="section-separator">
                <div class="section-info">
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Nombre</p>
                        </div>
                        <div class="info-right">
                            <p>{nombre}</p>
                        </div>
                    </div>
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Email</p>
                        </div>
                        <div class="info-right">
                            <p>{email}</p>
                        </div>
                    </div>
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Número de Celular</p>
                        </div>
                        <div class="info-right">
                            <p>{celular}</p>
                        </div>
                    </div>
                </div>
'''
# Mostrar apartado redes sociales si estan registradas.
if len(rrss_evento)>0:
    html += '''
                <h1 class="section-title">Redes sociales del oferente</h1>
                <hr class="section-separator">
                <div class="section-info">
    '''
    for rs in rrss_evento:
        html += f'''
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>{rs[1]}</p>
                        </div>
                        <div class="info-right">
                            <p>{rs[2]}</p>
                        </div>
                    </div>
        '''
    
    html += '''</div>'''


html += f'''
                <h1 class="section-title">Información del evento</h1>
                <hr class="section-separator">
                <div class="section-info">
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Día y hora de inicio</p>
                        </div>
                        <div class="info-right">
                            <p>{d_h_i}</p>
                        </div>
                    </div>
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Día y hora de término</p>
                        </div>
                        <div class="info-right">
                            <p>{d_h_t}</p>
                        </div>
                    </div>
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Descripción</p>
                        </div>
                        <div class="info-right">
                            <p>{desc}</p>
                        </div>
                    </div>
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Tipo</p>
                        </div>
                        <div class="info-right">
                            <p>{tipo}</p>
                        </div>
                    </div>
'''

# Mostrar foto principal:
html += f'''
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Foto principal<p>
                        </div>
                        <div class="info-right">
                            <img class="event-image" src="{fotos_evento[0][1]}" alt="foto_principal" width="320" height="240">
                        </div>
                    </div>
'''
# En caso de existir mas fotos, tambien se muestran:
resto_fotos = fotos_evento[1:]
if len(resto_fotos)>0:
    k = 1
    for f in resto_fotos:
        html += f'''
                    <div class="section-info-line">
                        <div class="info-left">
                            <p>Foto extra {k}<p>
                        </div>
                        <div class="info-right">
                            <img class="event-image" src="../{f[1]}" alt="foto_extra_{k}" width="320" height="240">
                        </div>
                    </div>
        
        '''
html += '''          
                </div>
            </div>
            <div class="btn-container">
                <a class="event-list-btn" id="home-btn" href="./event_list.py?page=0">Volver al listado de eventos</a>
                <a class="event-list-btn" id="return-btn" href="./home.py">Volver a la portada</a>
            </div>
        </div> 
        <!-- IMG VIEW: CONTENIDO DEL POP-UP ASOCIADO A LA VISTA DE UNA IMAGEN -->
        <div class="image-view" id="image-view">
            <div id="image-view-body" class="image-view-body"></div>
            <div class="image-view-footer">
                <button type="button" id="close-btn" class="image-view-btn">Volver a la informacion</button>
            </div>
        </div>
        <div id="image-view-overlay"></div>
    </div>
    <script src="../javascript/image.js"></script>
</body>
</html>
''' 

utf8stdout.write(html)
