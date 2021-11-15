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

data_graph_1 = db.get_data_graph_1()
data_graph_2 = db.get_data_graph_2()
data_graph_31, data_graph_32, data_graph_33 = db.get_data_graph_3()


graph_json = {
    "graph-1": data_graph_1,
    "graph-2": data_graph_2,
    "graph-3": {
        "graph-3-1": data_graph_31,
        "graph-3-2": data_graph_32,
        "graph-3-3": data_graph_33
    }
}

graph_json = json.dumps(graph_json)

utf8stdout.write(graph_json)