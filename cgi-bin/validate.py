#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import re
from database import Database
import functools
import filetype

db = Database()
# Validacion del input del usuario:

def val_evento(region, comuna, sector, nombre, email, num_cel, d_h_inicio, d_h_termino, descripcion, tipo):
    val_list = []
    campos_invalidos = []

    # validacion region y region
    val_region = db.get_region_id(region)
    val_list.append(val_region)
    if not val_region:
        campos_invalidos.append("Region")
        campos_invalidos.append("Comuna")
    
    # validacion comuna
    val_comuna = db.get_comuna_id(comuna, val_region)
    val_list.append(val_comuna)
    if not val_comuna:
        campos_invalidos.append("Comuna")

    # validacion sector
    val_sector = len(sector) <= 100
    val_list.append(val_sector)
    if not val_sector:
        campos_invalidos.append("Sector")

    # validacion nombre
    val_nombre = len(nombre) > 0 and len(nombre) <= 200
    val_list.append(val_nombre)
    if not val_nombre:
        campos_invalidos.append("Nombre")

    # validacion email
    val_email = bool(re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)").match(email))
    val_list.append(val_email)
    if not val_email:
        campos_invalidos.append("Email")
    
    # validacion num_cel
    val_num_cel = bool(re.compile(r"(^\+?\(?([0-9]{3})\)?[- ]?([0-9]{4})[- ]?([0-9]{4})$)").match(num_cel))
    val_list.append(val_num_cel)
    if not val_num_cel:
        campos_invalidos.append("Número de Celular")

    # validacion d_h_inicio y d_h_termino
    reg_d_h = re.compile(r"^([0-9]{4})-([0-9]{1,2})-([0-9]{1,2}) ([0-9]{1,2}):([0-9]{2})$")
    val_d_h_i = bool(reg_d_h.match(d_h_inicio))
    val_d_h_t = bool(reg_d_h.match(d_h_termino))
    val_list.append(val_d_h_i)
    val_list.append(val_d_h_t)
    if not val_d_h_i:
        campos_invalidos.append("Día y hora de inicio")
    if not val_d_h_t:
        campos_invalidos.append("Día y hora de termino")

    # validacion descripcion  (No es necesaria)
    # val_descripcion = True 

    # validacion tipo
    tipos_posibles = ['Al Paso', 'Alemana', 'Árabe', 'Argentina', 'Asiática', 'Australiana', 'Brasileña', 'Café y Snacks', 'Carnes', 'Casera', 'Chilena', 'China', 'Cocina de Autor', 'Comida Rápida', 'Completos', 'Coreana', 'Cubana', 'Española', 'Exótica', 'Francesa', 'Gringa', 'Hamburguesa', 'Helados', 'India', 'Internacional', 'Italiana', 'Latinoamericana', 'Mediterránea', 'Mexicana', 'Nikkei', 'Parrillada', 'Peruana', 'Pescados y mariscos', 'Picoteos', 'Pizzas', 'Pollos y Pavos', 'Saludable', 'Sándwiches', 'Suiza', 'Japonesa', 'Sushi', 'Tapas', 'Thai', 'Vegana', 'Vegetariana']
    val_tipo = tipo in tipos_posibles
    val_list.append(val_tipo)
    if not val_tipo:
        campos_invalidos.append("Tipo")

    return functools.reduce(lambda a, b: a and b, val_list), campos_invalidos

def val_red_social(redes_sociales):
    regex_url = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
    val_status = True
    for (rs, url) in redes_sociales:
        val_status = val_status and bool(regex_url.match(url))
    if not val_status:
        return False, ["URL Redes sociales"]
    return True, []

def val_foto(fotos):
    val_status = len(fotos) > 0 and len(fotos) <= 5
    if not val_status:
        return False, ["Fotos"]
    
    for f in fotos:
        tipo_foto = filetype.guess(f.file).mime
        val_status = val_status and ("image" in tipo_foto)
    if not val_status:
        return False, ["Fotos"]
    
    return True, []
