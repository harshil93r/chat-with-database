'''
- Connect to MySQL/PG/Elastic
- Mutilple Conditions
- get all table name
- get all coulumn from table
'''
import sys
import string
import re
from fuzzywuzzy.fuzz import ratio

def get_cred(s_q_text,_q_list=None):
    quoted = re.findall('"[^"]*"',s_q_text)
    
    synonyms = ['username','user']
    final_ = []

    for synonym in synonyms:
        if synonym in _q_list:
            indices = [i for i, x in enumerate(_q_list) if x == synonym]
            for index in indices:
                final_.append( _q_list[index + 1])
                final_.append( _q_list[index + 2])
                
    username  = list(set(quoted) & set(final_))[0]
    
    final_ = []
                
    synonyms = ['password','pass','secret']
        
    for synonym in synonyms:
        if synonym in _q_list:
            indices = [i for i, x in enumerate(_q_list) if x == synonym]
            for index in indices:
                final_.append( _q_list[index + 1])
                final_.append( _q_list[index + 2])
                
    password  = list(set(quoted) & set(final_))[0]
    
    final_ = []
       
    synonyms = ['database','collection','db']
        
    for synonym in synonyms:
        if synonym in _q_list:
            indices = [i for i, x in enumerate(_q_list) if x == synonym]
            for index in indices:
                final_.append( _q_list[index + 1])
                final_.append( _q_list[index + 2])
    
    db  = list(set(quoted) & set(final_))[0]
    
    return {
        'username' : username.replace("'",'').replace('"',''),
        'password' : password.replace("'",'').replace('"',''),
        'db' : db.replace("'",'').replace('"','')
    }

    

def get_location(_q_list):
    final_ = []
    synonyms = ['port','socket']
    location = 'not_found'
    for i in _q_list:
        if ('.' in i) and len(i)>6:
            location = i
    if location != 'not_found':
        address = location
    else:
        return { 'error' : 'Address Not Found'}
        
    for synonym in synonyms:
        if synonym in _q_list:
            indices = [i for i, x in enumerate(_q_list) if x == synonym]
            for index in indices:
                final_.append( _q_list[index + 1])
                
    
    print final_
    port = list(set(final_))[0]
    return {
        'port' : port,
        'address' : address 
    }

def get_database(_q_list):
    databases = [
        ('mysql',1),
        ('elastic search',2),
        ('es',2),
        ('elastic',2),
        ('elasticsearch',2),
        ('postgres',3),
        ('postgressql',3),
        ('pgsql',3)
        ]
    fin = []
    for i in databases:
        for j in _q_list:
            if ratio(i[0],j)>80 :
                fin.append(i[1])
    
    return list(set(fin))
    
def get_query(_q_text):
    exclude = set(string.punctuation)
    exclude.remove("'")
    exclude.remove('"')
    exclude.remove('.')
    exclude.remove('_')
    
    s_q_text = ''.join(ch for ch in _q_text if ch not in exclude)    
    _q_list = (s_q_text.lower()).split(' ')
    print _q_list
    # get chart type
    try :
        database =  (get_database(_q_list))
    except Exception,e:
        return {'error' : e}
    
    try:
        location = (get_location(_q_list))
    except Exception,e:
        return {'error' : e}
    
    try:
        cred = (get_cred(s_q_text,_q_list))
    except Exception,e:
        return {'error' : e}
    
    # print  database,  location 
    
    return {
        'database' : database[0],
        'location' : location,
        'credential' : cred
    }
    

def get_connection(message):


    query = get_query(message)
    print query
    if 'error' in query.keys():
        print 'failed'
        
    if query['database'] == 1 :
        print 'mysql'
    elif query['database'] == 2:
        print 'elasticsearch'
    elif query['database'] == 3 :
        from postgres import pg_connect
        connection = pg_connect(
            host = query['location']['address'],
            port = query['location']['port'],
            username = query['credential']['username'],
            password = query['credential']['password'],
            database = query['credential']['db'])
        
        
    return connection
        
        
    