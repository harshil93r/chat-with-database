import psycopg2
import psycopg2.extras

import pandas as pd



class pg_connect():
    
    def __init__(self,host,port,username,password,database):
        self.conn = psycopg2.connect(database=database, user=username,
                                password=password, host=host,
                                port=port)
        self.cursor = self.conn.cursor()

    def get_all_table(self):
        
        self.cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        self.tables = []
        for table in self.cursor.fetchall():
            self.tables.append(table[0])
            
        return self.tables
    
    def get_all_table_with_columns(self):
        self.cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        self.tables = []
        for table in self.cursor.fetchall():
            self.tables.append({'name' : table[0],
                                'columns' : ' ,'.join(self.get_table_coulumns(table[0]))})
            
        return self.tables

    def get_table_coulumns(self,table_name):
        self.cursor.execute("Select * FROM %s" % (table_name))
        colnames = [desc[0] for desc in self.cursor.description]
        return colnames
    
    
    def get_table_values(self,table_name=None,query=None):
        
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if query:
            cur.execute(query)
        else:
            cur.execute("Select * FROM %s" % (table_name))
        ans =cur.fetchall()
        df = pd.DataFrame([i.copy() for i in ans])
        ans1 = []
        for row in ans:
            ans1.append(dict(row))
        
        print df #actually it's return
        return df
        
        
        
        


    
        
