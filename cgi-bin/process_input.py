#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import cgi
import cgitb
from database import Database
from validate import *

# Funciones auxiliares:
def get_social_networks(form):
    sn_keys = filter(lambda k: k.startswith("sn-"), form.keys())
    sn_input = []
    
    for key in sn_keys:
        sn_index, sn = key.split("-")[1:3]
        sn_input.append((int(sn_index), sn, form[key].value))
    
    sn_input.sort(key=lambda tup: tup[0])
    return list(map(lambda tup: (tup[1], tup[2]), sn_input))
 
def get_photos(form):
    photo_keys = filter(lambda k: k.startswith("file-input-"), form.keys())
    photo_input = []

    for key in photo_keys:
        photo_index = key.split("-")[2]
        photo_input.append((photo_index, form[key]))
    
    photo_input.sort(key=lambda tup: tup[0])
    return list(map(lambda tup: tup[1], photo_input))

cgitb.enable()
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)
db = Database()
form = cgi.FieldStorage()
print('Content-type: text/html; charset=UTF-8')
print('')

region  = form["region"].value
comuna = form["comuna"].value
sector = form["sector"].value
nombre = form["nombre"].value
email = form["email"].value
num_cel = form["celular"].value
d_h_inicio = form["dia-hora-inicio"].value
d_h_termino = form["dia-hora-termino"].value
descripcion = form["descripcion-evento"].value
tipo = form["tipo-comida"].value
redes_sociales = get_social_networks(form)
fotos = get_photos(form)

validacion_evento = val_evento(region, comuna, sector, nombre, email, num_cel, d_h_inicio, d_h_termino, descripcion, tipo)
validacion_r_s = val_red_social(redes_sociales)
validacion_fotos = val_foto(fotos)

estado_validacion = validacion_evento[0] and validacion_r_s[0] and validacion_fotos[0] 

html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../styles/event_form.css">
    <link rel="stylesheet" href="../styles/pop_up.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    <title>Informar evento</title>
</head>
<body onload="populateForm(`{region}`, `{comuna}`, `{sector}`, `{nombre}`, `{email}`, `{num_cel}`, `{d_h_inicio}`, `{d_h_termino}`, `{descripcion}`, {len(redes_sociales)}, {len(fotos)}, `{tipo}`, {0 if estado_validacion else 1})">
    <div class="header">
        <a href="./home.py"><h1 class="header-title">Ventas de Comida Casera</h1></a>
        <ul class="nav-bar">
            <li class="nav-item"><a class="nav-link" href="../event_form.html">Informar evento</a></li>
            <li class="nav-item"><a class="nav-link" href="./event_list.py">Listado de eventos</a></li>
            <li class="nav-item"><a class="nav-link" href="../statistics.html">Estadisticas</a></li>
        </ul>
    </div>
    <div class="content">
        <!-- INFO BOX: CAJA DEL CONTENIDO PRINCIPAL -->
        <div class="info-box">
            <div class="text-box">
                <h1>Informa tu Evento</h1>
                <p>Responde este simple formulario para registrar tu evento en el sistema.</p>           
            </div>
            <div id="val-notification">
'''
# Si el input es valido se registra en la base de datos:
if estado_validacion:
    # Guardamos informacion en la tabla evento:
    region_id = db.get_region_id(region)
    comuna_id = db.get_comuna_id(comuna, region_id)
    data_evento = (comuna_id, sector, nombre, email, num_cel, d_h_inicio, d_h_termino, descripcion, tipo)
    db.save_evento(data_evento)

    # Guardamos informacion en la tabla red_social:
    evento_id = db.get_last_evento_id()
    for t in redes_sociales:
        nombre_rs, url_rs = t
        red_social_data = (nombre_rs, url_rs, evento_id)
        db.save_red_social(red_social_data)

    # Guardamos las fotos en la carpeta img/ y luego su informacion en la tabla foto:
    for f in fotos:
        data_foto = (f, evento_id)
        db.save_foto(data_foto)
    
# Si algun campo es invalido:
else:
    campos_invalidos = validacion_evento[1] + validacion_r_s[1] + validacion_fotos[1]
    str_campos_invalidos = ""
    
    k = 0
    n = len(campos_invalidos)
    while(k<n):
        s = campos_invalidos[k]
        if k != n-1:
            str_campos_invalidos += (s+", ") 
        else:
            str_campos_invalidos += (s+".")
        k+=1
    html += f'''Su formulario falló en: {str_campos_invalidos}''' 
                       
html += ''' </div>
            <form id="event-form" enctype="multipart/form-data" method="post" action="./process_input.py">
                <h1 class="section-title">Información del lugar</h1>
                <hr class="section-separator">
                <div class="form-section">
                    <div class="form-input">
                        <div>
                            <label for="region">Región</label>
                        </div>
                        <select name="region" id="region" onclick="loadRegions()" onchange="enableCommunes()" required>
                        </select>
                    </div>
                    <div class="form-input">
                        <div>
                            <label for="comuna">Comuna</label>
                        </div>
                        <select name="comuna" id="comuna" onclick="loadCommunes()" required>
                        </select>
                    </div>
                    <div class="form-input">
                        <div>
                            <label for="sector">Sector</label>
                        </div>
                        <input name="sector" id="sector" type="text" size="100" maxlength="100">
                    </div>
                </div>
                <h1 class="section-title">Datos del oferente</h1>
                <hr class="section-separator">
                <div class="form-section">
                    <div class="form-input">
                        <div>
                            <label for="nombre">Nombre</label>
                        </div>
                        <input name="nombre" id="nombre" type="text" size="100" maxlength="200" required>
                    </div>
                    <div class="form-input">
                        <div>
                            <label for="email">Email</label>
                        </div>
                        <input name="email" id="email" type="text" size="100" placeholder="example@email.com" required>
                    </div>
                    <div class="form-input">
                        <div>
                            <label for="celular">Número de Celular</label>
                        </div>
                        <input name="celular" id="celular" type="text" size="15" placeholder="+569-1234-5678">
                    </div>
                    <div id="social-net-container">
                        <div class="form-input">
                            <div>
                                <label for="red-social">Red social</label>
                            </div>
                            <select name="red-social" id="red-social" onchange="handleSocialNetInput()">
                                <option value="" hidden>Seleccione una red social</option>
                                <option value="Twitter">Twitter</option>
                                <option value="Instagram">Instagram</option>
                                <option value="Facebook">Facebook</option>
                                <option value="Tiktok">Tiktok</option>
                                <option value="Otra">Otra</option>
                            </select>
                        </div>
'''

k = 0
for sn, url in redes_sociales:
    html += f'''
                        <div class="form-input">
                            <div>
                                <label for="sn-{k}-{sn}">URL perfil de {sn}</label>
                            </div>
                            <input name="sn-{k}-{sn}" id="sn-{k}-{sn}" class="sn-txt-input" type="text" value="{url}">
                        </div>
    '''
    k += 1


html += '''                       
                    </div>
                </div>
                <h1 class="section-title">Información del evento</h1>
                <hr class="section-separator">
                <div class="form-section">
                    <div class="form-input">
                        <div>
                            <label for="dia-hora-inicio">Día y hora de inicio</label>
                        </div>
                        <input name="dia-hora-inicio" id="dia-hora-inicio" type="text" size="20" required>
                    </div>
                    <div class="form-input">
                        <div>
                            <label for="dia-hora-termino">Día y hora de término</label>
                        </div>
                        <input name="dia-hora-termino" id="dia-hora-termino" type="text" size="20" required>
                    </div>
                    <div class="form-input">
                        <div>
                            <label for="descripcion-evento">Descripción</label>
                        </div>
                        <textarea name="descripcion-evento" id="descripcion-evento" cols="50" rows="10"></textarea>
                    </div>
                    <div class="form-input">
                        <div>
                            <label for="tipo-comida">Tipo</label>
                        </div>
                        <select name="tipo-comida" id="tipo-comida" onclick="loadFoodTypes()" required>
                            <option value="" hidden>Seleccione un tipo de comida</option>
                        </select>
                    </div>
                    <div id="file-input-container">
                        <div class="form-input">
                            <div>
                                <label for="foto-comida">Foto principal</label>
                            </div>
                            <div class="input-file-btns-container">
                                <input type="file" name="file-input-0" id="foto-comida" required>
                                <button type="button" id="add-file-input-btn" onclick="handleInputFile()">Agregar otra foto</button>
                            </div>
                        </div>
'''
if (len(fotos) > 1):
    k = 1
    for f in fotos[1:]:
        html += f'''
                            <div class="form-input">
                                <div>
                                    <label for="file-input-{k}">Foto extra (Nro. {k})</label>
                                </div>
                                <div class="input-file-btns-container">
                                    <input name="file-input-{k}" id="file-input-{k}" type="file" required="" value=>
                                </div>
                            </div>
        '''
        k += 1

html += '''
                    </div>
                    <button type="button" class="send-btn" onclick="validateInputs()">Enviar información de este evento</button>
                </div>
            </form>
        </div>
        <!-- POP-UP: CONTENIDO ASOCIADO AL POP-UP -->
        <div class="pop-up" id="pop-up">
            <div class="pop-up-header">
                <div id="pop-up-title">¿Está seguro que desea agregar este evento?</div>
            </div>
            <div id="pop-up-body" class="pop-up-body">
                <button type="button" class="pop-up-btn" id="confirm-btn">Sí, estoy seguro</button>
                <button type="button" class="pop-up-btn" id="regret-btn">No, no estoy seguro</button>
            </div>
        </div>
'''
if (estado_validacion):
    html += '''
        <div class="pop-up active" id="pop-up">
            <div class="pop-up-header">
                <div id="pop-up-title">Hemos recibido su información, muchas gracias y suerte en su emprendimiento</div>
            </div>
            <div id="pop-up-body" class="pop-up-body">
                <button type="button" class="pop-up-btn" id="confirm-btn" style="display: none;">Sí, estoy seguro</button>
                <button type="button" class="pop-up-btn" id="regret-btn" style="display: none;">No, no estoy seguro</button>
                <a id="home-btn" class="pop-up-btn" href="./home.py">Volver a la pagina de inicio</a>
            </div>
        </div>
        <div id="pop-up-overlay" class="active"></div>
    '''
else:
    html += '''
        <div class="pop-up" id="pop-up">
            <div class="pop-up-header">
                <div id="pop-up-title">¿Está seguro que desea agregar este evento?</div>
            </div>
            <div id="pop-up-body" class="pop-up-body">
                <button type="button" class="pop-up-btn" id="confirm-btn">Sí, estoy seguro</button>
                <button type="button" class="pop-up-btn" id="regret-btn">No, no estoy seguro</button>
            </div>
        </div>
        <div id="pop-up-overlay"></div>
    '''
html += ''' 
    </div>
    <script src="../javascript/repop_form.js"></script>
    <script src="../javascript/pop_up.js"></script>
    <script src="../javascript/validaciones.js"></script>
</body>
</html>
'''
utf8stdout.write(html)
         