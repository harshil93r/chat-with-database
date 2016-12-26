from postgres import *


from connect import get_connection # to get connection object
from nlp_test import get_chart_params

from fuzzywuzzy.fuzz import ratio

# x = pg_connect(database='mit',port=5432,host='localhost',username='mit_dev',password='mit_platform')
# 
# x.get_table_values('users_mituser')

stages = [
    (0,'nothing'),
    (1,'connected/ask graph'),
    (2,'graph plotted')
]

stage = 0

while True:
    _msg = raw_input("Hello, What's you commend?\n\n")
    if ratio(_msg,'exit') > 90 or ratio(_msg,'bye') > 90:
        exit
    else:
        if stage == 0:
            connection = get_connection(_msg)
            if connection:
                stage = 1
                print '\nConnected to Database'
                print '\nAll Table available are : \n\n'
                tables = connection.get_all_table()

                for i in tables:
                    print i
                pass
        elif stage == 1 :
            chart_params = get_chart_params(_msg,tables=tables)
            
            if 'error' in chart_params:
                print chart_params
                pass
        