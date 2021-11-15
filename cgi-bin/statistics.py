#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import cgi
import cgitb
import json
from database import Database
from validate import *

cgitb.enable()
utf8stdout = open(1, 'w', encoding='utf-8', closefd=False)
db = Database()

print('Content-type: text/html; charset=UTF-8')
print('')

msg = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../styles/statistics.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/flot-charts@0.8.3/jquery.flot.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/flot/0.8.3/jquery.flot.pie.min.js" integrity="sha512-jMP1biHEi+eAK+dGbOLAmabdBzVTUjHpryY1vsILFGYatR5i55+ZuXZXBOdbz/KzvTstnsu6+TJCTZ79/PMjbA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/flot/0.8.3/jquery.flot.time.min.js" integrity="sha512-lcRowrkiQvFli9HkuJ2Yr58iEwAtzhFNJ1Galsko4SJDhcZfUub8UxGlMQIsMvARiTqx2pm7g6COxJozihOixA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/flot/0.8.3/jquery.flot.symbol.min.js" integrity="sha512-sNgc3wPoIJSIDDHECpH63hxa5HtCAbsJUjWWarP3BZvfR03wbqIyFywI0qbu/GoLKQkZuO4ji2uMqfk7xnjAxQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/flot/0.8.3/jquery.flot.categories.min.js" integrity="sha512-x4QGSZkQ57pNuICMFFevIhDer5NVB5eJCRmENlCdJukMs8xWFH8OHfzWQVSkl9VQ4+4upPPTkHSAewR6KNMjGA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    <title>Ventas Comida Casera</title>
</head>
<body>
    <div class="header">
        <a href="./home.py"><h1 class="header-title">Ventas de Comida Casera</h1></a>
        <ul class="nav-bar">
            <li class="nav-item"><a class="nav-link" href="../event_form.html">Informar evento</a></li>
            <li class="nav-item"><a class="nav-link" href=".event_list.py?page=0">Listado de eventos</a></li>
            <li class="nav-item"><a class="nav-link" href="./statistics.py">Estadisticas</a></li>
        </ul>
    </div>
    <div class="content">
        <div class="info-box">
            <div class="text-box">
                <h1>Estadisticas</h1>
                <p>Aquí tienes las estadisticas calculadas en base a los eventos registrados</p>           
            </div>
            <div class="graph-container">
                <h2>Frecuencia eventos por día</h1>
                <div id="graph-1" style="width:600px; height:300px;"></div>
                <h2>Frecuencia eventos por tipo de comida</h1>
                <div id="graph-2" style="width:600px; height:300px;"></div>
                <h2>Frecuencia eventos en la mañana, medio día y tarde por día.</h1>
                <div id="graph-3" style="width:600px; height:300px;"></div>
"""
                
                
msg += """
            </div>
            <div class="btn-container">
                <a class="statistics-btn" id="home-btn" href="./cgi-bin/home.py">Volver a la portada</a>
            </div>

        </div>
    </div>
    <div class="footer"></div>
</body>
<script src="../javascript/graphs.js"></script>

</html>
"""

utf8stdout.write(msg)

