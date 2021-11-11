#!/usr/bin/python3
# -*- coding: utf-8 -*-
import mysql.connector
import hashlib
import os

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="cc500255_u",
            password="uelacusquI",
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
        open(f"../img/{file_name_hash}", "wb").write(file_item.value)
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
      
