from django.shortcuts import render
from connect import get_connection
import  os
import ast

from nlp_test import get_operation

import cPickle

stages = [
    (0,'nothing'),
    (1,'connected/ask graph'),
    (2,'graph plotted')
]


def dashboard(request):
    operation = None
    table = None
    chart = False
    query = False
    table_content = None
    if request.method == "POST":
        if int(os.environ["stage_nlp"]) == 0:
            connection , address = get_connection( request.POST.get('message'))
            tables = connection.get_all_table_with_columns()
            tab = connection.get_all_table()
            os.environ["tab"] = str(tab)
            os.environ["tables"] = str(tables)
            os.environ["address"] = address
            os.environ["message"] = request.POST.get('message')
            if connection:
                os.environ["connected"] = 'True'
                os.environ["stage_nlp"] = '1'


                
        elif int(os.environ["stage_nlp"]) == 1:
            if request.POST.get('_method') == 'disconnect':
                os.environ['connected'] = 'False'
                os.environ["stage_nlp"] = '0'
            
            elif request.POST.get('chart'):
                chart = True
                operation = get_operation(request.POST.get('message'),ast.literal_eval(os.environ["tab"]))
                print operation
                
            elif request.POST.get('query'):
                query = True
                connection , address = get_connection( os.environ["message"])
                x = connection.get_table_values(query = request.POST.get('message'))
                table_content = x.to_html

            
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]
    chartdata = {'x': xdata, 'y': ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    if os.environ.get('connected',False) == 'True':
        connected = True
        tables = ast.literal_eval(os.environ["tables"])
        address = os.environ["address"]
    else:
        connected = False
        tables = ['none']
        address = 'none'
        

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
        'connected' : connected,
        'tables' : tables,
        'address' : address,
        'stage' : os.environ["stage_nlp"],
        'chart' : chart,
        'table' : table,
        'query' : query,
        'table_content' : table_content,
        'operation' : operation
    }
    return render(request, 'chat.html',data)


