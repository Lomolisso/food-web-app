#!/usr/bin/python3
# -*- coding: utf-8 -*-
import mysql.connector
import random
import datetime
import numpy as np
import hashlib
import os

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="",
            user="",
            password="",
            database="cc500255_db",
            port="3306"
        )
        self.cursor = self.db.cursor()
    
    # METODOS PARA GUARDAR INFO EN DB.
    def save_evento(self, data):
        sql = '''
        INSERT INTO evento (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion, tipo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        self.cursor.execute(sql, data)
        self.db.commit()

    def save_red_social(self, data):
        sql = '''
        INSERT INTO red_social (nombre, identificador, evento_id)
        VALUES (%s, %s, %s)
        '''
        self.cursor.execute(sql, data)
        self.db.commit() 

    def save_foto(self, data):
        file_item, evento_id = data
        file_name = os.path.basename(file_item.filename)
        file_name_hash = hashlib.sha256(file_name.encode()).hexdigest()[0:30]
        sql = "SELECT COUNT(id) FROM foto"
        self.cursor.execute(sql)
        total = self.cursor.fetchall()[0][0] + 1
        file_name_hash += f"_{total}"
        open(f"img/{file_name_hash}", "wb").write(file_item.value)
        data = (f"../img/{file_name_hash}", file_name, evento_id)
        sql = '''
        INSERT INTO foto (ruta_archivo, nombre_archivo, evento_id)
        VALUES (%s, %s, %s)
        '''
        self.cursor.execute(sql, data)
        self.db.commit() 
    

    # METODOS PARA CONSULTAR DB. 
    def get_region_id(self, nombre_region):
        sql = f'''
        SELECT id FROM region WHERE nombre = '{nombre_region}'
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]
    
    def get_comuna_id(self, nombre_comuna, region_id):
        sql = f'''
        SELECT id FROM comuna WHERE nombre = '{nombre_comuna}' AND region_id = {region_id}
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]

    def get_comuna_data(self, comuna_id):
        sql = f'''
        SELECT nombre, region_id FROM comuna WHERE id = '{comuna_id}'
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]

    def get_region_name(self, region_id):
        sql = f'''
        SELECT nombre FROM region WHERE id = '{region_id}'
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]

    def get_comuna_name(self, comuna_id):
        sql = f'''
        SELECT nombre FROM comuna WHERE id = '{comuna_id}'
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]



    ##########################################################################################
    def get_event_info(self, evento_id):
        sql = f'''
        SELECT * FROM evento WHERE id = '{evento_id}'
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0]

    def get_event_sn(self, evento_id):
        sql = f'''
        SELECT * FROM red_social WHERE evento_id = '{evento_id}'
        ORDER BY id ASC
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_event_photos(self, evento_id):
        sql = f'''
        SELECT * FROM foto WHERE evento_id = '{evento_id}'
        ORDER BY id ASC
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # NOTAR QUE TODOS LOS EVENTOS TIENEN AL MENOS 1 IMAGEN, POR LO
    # QUE PARA LOS MARCADORES BASTA RECUPERAR LA INFORMACION NECESARIA 
    # DE TODOS LOS EVENTOS.
    def get_event_info_marker(self):
        sql = f'''
        SELECT id, comuna_id, sector, dia_hora_inicio, dia_hora_termino, tipo
        FROM evento
        ORDER BY id ASC
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

        
    ##########################################################################################
    
    def get_last_evento_id(self):
        sql = '''
        SELECT max(id) FROM evento 
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]

    def get_eventos(self):
        sql = '''
        SELECT * FROM evento ORDER BY id DESC
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_home_data(self):
        sql = f'''
        SELECT E.id, E.dia_hora_inicio, E.dia_hora_termino, C.nombre, E.sector, E.tipo, E.descripcion, F1.ruta_archivo
        FROM evento E, comuna C, (
            SELECT * FROM foto GROUP BY evento_id
        ) F1
        WHERE E.id = F1.evento_id AND E.comuna_id = C.id
        ORDER BY E.id DESC
        LIMIT 5
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    
    def get_event_list_data(self, page):
        sql = f'''
        SELECT E.id, E.dia_hora_inicio, E.dia_hora_termino, C.nombre, E.sector, E.tipo, E.descripcion, E.nombre, F1.ruta_archivo, F2.total_fotos
        FROM evento E, comuna C, (
            SELECT * FROM foto GROUP BY evento_id
        ) F1, (
            SELECT evento_id, COUNT(*) AS total_fotos FROM foto GROUP BY evento_id
        ) F2
        WHERE E.id = F1.evento_id AND E.id = F2.evento_id AND E.comuna_id = C.id AND E.id > {5*page} AND E.id <= {5*(page+1)}
        ORDER BY E.id ASC
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_min_comunas(self):
        sql = '''
        SELECT * FROM comuna GROUP BY region_id COUNT
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    

    #################################################
    #               QUERYS GRAFICOS                 #
    #################################################

    # Puntos de la forma: (dia: {dd-mm-yyyy}, frec: int)
    def get_data_graph_1(self):
        format_date = lambda d: f"{d.year}-{d.month}-{d.day}"
        dates = sorted([v[6] for v in self.get_eventos()])
        
        data = list(map(format_date, [v for v in dates]))
        
        x = []
        y = []

        for v in data:
            if v not in x:
                x.append(v)
                y.append(1)
            else:
                y[x.index(v)] += 1

        return [[u, v] for u,v in zip(x, y)]

    def get_data_graph_2(self):
        data = [v[9] for v in self.get_eventos()]
        
        x = []
        y = []

        for v in data:
            if v not in x:
                x.append(v)
                y.append(1)
            else:
                y[x.index(v)] += 1

        return [{"label": u + f": {v}", "data": v} for u,v in zip(x, y)]

    def get_data_graph_3(self):
        month_list = [
            ["En"],
            ["Febr"],
            ["Mzo"],
            ["Abr"],
            ["My"],
            ["Jun"],
            ["Jul"],
            ["Agt"],
            ["Sep"],
            ["Oct"],
            [ "Nov"],
            [ "Dic"]
        ]
        
        
        frec = [
            list(np.zeros(12)),
            list(np.zeros(12)),
            list(np.zeros(12)) 
        ]

        data = [v[6] for v in self.get_eventos()]

        for d in data:
            month_index = d.month - 1
            time_period = None
            
            if d.hour < 11 and d.hour >= 0:
                time_period = 0
            elif d.hour >= 11 and d.hour < 15:
                time_period = 1
            else:
                time_period = 2
            
            frec[time_period][month_index] += 1

        ret_1 = [[month_list[i], frec[0][i]] for i in range(0, 12)]
        ret_2 = [[month_list[i], frec[1][i]] for i in range(0, 12)]
        ret_3 = [[month_list[i], frec[2][i]] for i in range(0, 12)]
        
        return ret_1, ret_2, ret_3