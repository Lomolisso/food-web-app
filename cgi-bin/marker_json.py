#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import cgi
import cgitb
import json
from database import Database


cgitb.enable()
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)

db = Database()

print('Content-type: text/html; charset=UTF-8')
print('')

latlng_json = None;
with open("latlng.json", "r") as f:
    latlng_json = json.load(f)

markers_event_info = db.get_event_info_marker()
markers_json = {}
for info in markers_event_info:
    event_id, comuna_id, sector, dia_hora_inicio, dia_hora_termino, tipo = info
    comuna = db.get_comuna_name(comuna_id)
    if comuna not in markers_json.keys():
        lat, lng = None, None
        for v in latlng_json:
            if v["name"] == comuna:
                lat, lng = v["lat"], v["lng"]

        markers_json[comuna] = {}
        
        markers_json[comuna]["info"] = {
            "total_fotos": 0, 
            "lat": lat, 
            "lng": lng
        }
        
        markers_json[comuna]["eventos"] = {}

    fotos = db.get_event_photos(event_id)

    event_dict = {
        "id": event_id,
        "dia_hora_inicio": dia_hora_inicio.strftime(r'%Y-%m-%d %H:%M:%S'),
        "dia_hora_termino": dia_hora_termino.strftime(r'%Y-%m-%d %H:%M:%S'),
        "tipo": tipo,
        "sector": sector,
        "fotos": [v[1] for v in fotos]
    }
    
    markers_json[comuna]["eventos"][event_id] = event_dict
    markers_json[comuna]["info"]["total_fotos"] += len(fotos)

markers_json = json.dumps(markers_json)

utf8stdout.write(markers_json)