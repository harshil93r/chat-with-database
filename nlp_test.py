import sys
import string
import re
from fuzzywuzzy.fuzz import ratio

valid_chart_type = ['bar','pie','line']



def get_chart_type(_q_list):
    final_ = []
    synonyms = ['graph','chart','plot','graphs','charts','plots']
    for synonym in synonyms:
        if synonym in _q_list:
            indices = [i for i, x in enumerate(_q_list) if x == synonym]
            if (indices[-1] - 1)>0:
                final_.append( _q_list[indices[-1] - 1])
                
    
    if len( set(valid_chart_type) & set(final_) ) != 0:
        return  set(valid_chart_type) & set(final_)
    else:
        fin = []
        for i in valid_chart_type:
            for j in final_:
                if ratio(i,j)>80 :
                    fin.append(i)
                    
        return fin
    
def get_table(_q_list):
    final_ = []
    synonyms = ['table','index']
    for synonym in synonyms:
        if synonym in _q_list:
            indices = [i for i, x in enumerate(_q_list) if x == synonym]
            if (indices[-1] + 1)>0:
                final_.append( _q_list[indices[-1] + 1])
                
    
    
    if len(final_ ) == 0:
        for _q in _q_list:
            for t in tab:
                if ratio(_q,t)>90:
                    final_.append(t)
                    
        return final_
        
    elif len( set(tab) & set(final_) ) != 0:
        return  set(tab) & set(final_)
    else:
        fin = []
        for i in tab:
            for j in final_:
                if ratio(i,j)>80 :
                    fin.append(i)
                    
        return fin
    
    
def get_query(_q_text):
    exclude = set(string.punctuation)
    exclude.remove("'")
    exclude.remove('"')
    exclude.remove('_')
    s_q_text = ''.join(ch for ch in _q_text if ch not in exclude)    
    _q_list = (s_q_text.lower()).split(' ')
    print _q_list
    # get chart type
    try :
        chart_type =  list(get_chart_type(_q_list))[0]
    except :
        return {'error' : 'Chart_Type'}
    
    quoted = re.findall('"[^"]*"',s_q_text)
    try:
        table = list(get_table(_q_list))[0].replace('"','').replace("'",'')
    except:
        return {'error' : 'Table_Name'}
    
    print chart_type , table
    
    return {
        'chart_type' : chart_type,
        'table_name' : table
    }
    
    
def get_chart_params(_msg,tables):
    global tab
    tab= tables
    return get_query(_q_text = _msg)