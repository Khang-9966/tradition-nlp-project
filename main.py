from Model.parser import Parser
from Input.question import question
from Input.database import DATABASE


parser = Parser()
parsing_result = parser.parsing(question)
with open('Output/output_a.txt', 'w') as writer:
    writer.writelines("+ Dependency: \n")
with open('Output/output_a.txt', 'w') as writer:
    writer.writelines("+ Dependency: \n")
    for parse in parsing_result:
        writer.writelines(parse.__str__() + "\n")
print(parsing_result)
########### LOGICAL FORM ###########
citytable = {
    "huế" : "HUE",
    "hồ_chí_minh" : "HCMC",
    "đà_nẵng" : "DANANG",
}
def get_childleaf_node(parsing_result,word,SOURCE_DEST):
    for realation in parsing_result:
        if realation['head'] == word:
            if word == "từ":
                SOURCE_DEST = 'SOURCE'
            if word == "đến":
                SOURCE_DEST = 'DEST'
            return get_childleaf_node(parsing_result,realation['word'],SOURCE_DEST)
    if word[-2:] == 'hr' :
        if SOURCE_DEST == 'DEST':
            SOURCE_DEST = 'ARRIVE'
        elif SOURCE_DEST == 'SOURCE':
            SOURCE_DEST = 'LEAVES'
    
    if word[0] == 'b' and len(word) == 2:
        SOURCE_DEST = 'NAME'
        
    return word,SOURCE_DEST
def get_all_childleaf_forSUBJ(parsing_result,word):
    child_list = []
    for realation in parsing_result:
        source_dest = None
        if realation['head'] == word and realation['word'] != 'nào' and realation['word'] != 'những':
            if word == "từ":
                source_dest = 'SOURCE'
            if word == "đến":
                source_dest = 'DEST'
            childleaf_node,source_dest = get_childleaf_node(parsing_result,realation['word'],source_dest)
            if source_dest != 'ARRIVE' and  source_dest != 'LEAVES' and source_dest != 'NAME':
                fform = " ( " + source_dest + " x ( NAME " + citytable[childleaf_node]  + " " + childleaf_node + " ) ) "
                child_list.append( ( childleaf_node , source_dest ,  fform) )
            elif source_dest != 'NAME':
                fform = " ( " + source_dest + " x ( NAME t1 " + childleaf_node.upper() + " ) ) "
                child_list.append( ( childleaf_node , source_dest ,  fform) )
            else :
                fform = " ( BUS " + source_dest + " x ( NAME " + childleaf_node + " "  + childleaf_node.upper() + " ) ) "
                #fform = " ( BUS x "  + childleaf_node.upper() + " ) "
                child_list.append( ( childleaf_node , source_dest , fform ) )
    return child_list

def get_all_childleaf_forVERB(parsing_result,word):
    child_list = []
    for realation in parsing_result:
        source_dest = None
        if word == 'đi':
            source_dest = check_SOURCE_or_DEST(parsing_result)
        if realation['head'] == word and realation['relationtype'] != "sub" and realation['relationtype'] != "punct":
            if word == "từ":
                source_dest = 'SOURCE'
            if word == "đến":
                source_dest = 'DEST'
            childleaf_node,source_dest = get_childleaf_node(parsing_result,realation['word'],source_dest)
            if source_dest != 'ARRIVE' and  source_dest != 'LEAVES' and source_dest != 'NAME':
                fform =  " ( " + source_dest + " x ( NAME " + citytable[childleaf_node]  + " " + childleaf_node + " ) ) " 
                child_list.append( ( childleaf_node , source_dest , fform ) )
            elif source_dest != 'NAME':
                fform = " ( " + source_dest + " x ( NAME t1 " + childleaf_node.upper() + " ) ) " 
                child_list.append( ( childleaf_node , source_dest , fform ) )
            else :
                ffrom = " ( " + source_dest + " x ( NAME " + childleaf_node + " "  + childleaf_node.upper() + " ) ) "
                child_list.append( ( childleaf_node , source_dest ,  ffrom  ) )
    return child_list

def check_SOURCE_or_DEST(parsing_result):
    for realation in parsing_result:
        if realation['head'] == 'đi':
            if realation['word'] == 'đến':
                return "DEST"
            if realation['word'] == 'từ':
                return "SOURCE"
    return "SOURCE"

def find_question_object(parsing_result):
    
    for realation in parsing_result:
        if realation['relationtype'] == 'root':
            root = realation['word']
            
    for realation in parsing_result:
        if realation['relationtype'] == 'sub' and realation['head'] == root:
            sub = realation['word']
            sub_query = 'WHx : ( & ( BUS x ) '
            p_form = " ?x ( BUS ?x ) "
            query = 'WHx : ( & ( BUS x ) '
            p_form_query = " ?x ( BUS ?x ) "
            
    for realation in parsing_result:
        if realation['word'] == sub and realation['relationtype'] != 'sub' :
            query = 'WHt : ( & ( TIME ?t ) '
            p_form_query = " ?t ( TIME t ) "
            
    return query,sub,sub_query,root,p_form_query,p_form

query,sub,sub_query,root,p_form_query,p_form = find_question_object(parsing_result)
childleaf_forSUBJ = get_all_childleaf_forSUBJ(parsing_result,sub)
childleaf_forVERB = get_all_childleaf_forVERB(parsing_result,root)

if query == sub_query : 
    LF = query  
    for childleaf in childleaf_forSUBJ:
        LF += childleaf[2]
    for childleaf in childleaf_forVERB:
        LF += childleaf[2]
    LF += " ) "
else:
    LF = query + sub_query  
    for childleaf in childleaf_forSUBJ:
        LF += childleaf[2]
    for childleaf in childleaf_forVERB:
        LF += childleaf[2]
    LF += " )  ) "
    
with open('Output/output_b.txt', 'w') as writer:
    writer.writelines("+ Logical Form: \n")
with open('Output/output_b.txt', 'w') as writer:
    writer.writelines("+ Logical Form: {}\n".format(LF))
print(LF)
############## Procedural Form ###############
pform = ""
source_form = ""
dest_form = ""
QUERY_DEST = {  }
QUERY_SOURCE = {  }
for lf in childleaf_forVERB:
    if lf[1] == 'DEST' :
        dest = lf[0]
        dest_form = " ( ATIME ?x " + citytable[dest] 
        atime = " ?t "
        QUERY_DEST[1] = citytable[dest] 
        for lf in childleaf_forVERB:
            if lf[1] == 'ARRIVE' :
                atime = lf[0].upper()
                QUERY_DEST[2] = atime
        dest_form +=  " " + atime + ") "
        
    if lf[1] == 'SOURCE' :
        source = lf[0]
        source_form = " ( DTIME ?x " + citytable[source] 
        dtime = " ?t "
        QUERY_SOURCE[1] = citytable[source] 
        for lf in childleaf_forVERB:
            if lf[1] == 'LEAVES' :
                dtime = lf[0].upper()
                QUERY_SOURCE[2] = dtime
        source_form +=   " " + dtime + ") "


for lf in childleaf_forSUBJ:
    if lf[1] == 'SOURCE' :
        source = lf[0]
        source_form += " ( DTIME ?x " + citytable[source] 
        dtime = " ?t "
        QUERY_SOURCE[1] = citytable[source] 
        for lf in childleaf_forVERB:
            if lf[1] == 'LEAVES' :
                dtime = lf[0]
                QUERY_SOURCE[2] = dtime
        source_form +=  dtime + " ) "
        
    if lf[1] == 'NAME' :
        source = lf[0]
        QUERY_SOURCE[0] = source.upper()
        source_form += " ( " +source.upper()+ " ?x ) " 

PF =  "( FRINT-ALL "
if p_form_query  == p_form :
    PF += p_form_query + " "
    if source_form != "" :
        PF += " " + source_form + " "
    if dest_form != "" :
        PF += " " + dest_form + " "
else:
    PF += p_form_query +  " ( FRINT-ALL "
    PF += p_form + " "
    if source_form != "" :
        PF += " " + source_form + " "
    if dest_form != "" :
        PF += " " + dest_form + " "  
    PF += " ) "
PF += " ) "

with open('Output/output_c.txt', 'w') as writer:
    writer.writelines("+ Procedural Form: \n")
with open('Output/output_c.txt', 'w') as writer:
    writer.writelines("+ Procedural Form: {}\n".format(PF))
print(PF)
######## QUERY ###########

def merge_list(list_):
    if len(list_) > 0:
        return_list = list_[0]
        for child_list in list_[1:]:
            return_list = list( set(child_list) & set(return_list) )
        return return_list
    else:
        return []

QUERY_SOURCE_list = []
if len(QUERY_SOURCE) >= 1:
    for index_query in QUERY_SOURCE:
        temp = []
        value_query = QUERY_SOURCE[index_query]
        for data in DATABASE["DTIME"]:
            data_bus = data.split()
            if value_query == data_bus[index_query] :
                temp.append(data_bus[0])
        QUERY_SOURCE_list.append(temp)   
QUERY_SOURCE_list = merge_list(QUERY_SOURCE_list)  

QUERY_DEST_list = []
if len(QUERY_DEST) >= 1:
    for index_query in QUERY_DEST:
        temp = []
        value_query = QUERY_DEST[index_query]
        for data in DATABASE["ATIME"]:
            data_bus = data.split()
            if value_query == data_bus[index_query]:
                temp.append(data_bus[0])
        QUERY_DEST_list.append(temp)
QUERY_DEST_list = merge_list(QUERY_DEST_list)               

if len(QUERY_SOURCE) != 0 and len(QUERY_DEST) != 0 :
    RESULT = list( set(QUERY_SOURCE_list) & set(QUERY_DEST_list)  )
    
elif len(QUERY_SOURCE) != 0:
    RESULT = QUERY_SOURCE_list
    
elif len(QUERY_DEST) != 0:
    RESULT = QUERY_DEST_list
    
if query == 'WHt : ( & ( TIME ?t ) ':
    if len(QUERY_SOURCE) != 0 and len(QUERY_DEST) != 0:     
        if len(QUERY_SOURCE) == 1 and 0 in QUERY_SOURCE:
            TIME = []
            for bus in RESULT:
                for data in DATABASE["ATIME"]:
                    data_bus = data.split()
                    if data_bus[0] == bus:
                        TIME.append(data_bus[2])
            RESULT = TIME
        else:
            for index_query in QUERY_DEST:
                TIME = []
                for bus in RESULT:
                    for data in DATABASE["RUN-TIME"]:
                        data_bus = data.split()
                        if data_bus[0] == bus:
                            TIME.append(data_bus[3])
                RESULT = TIME
        
    elif len(QUERY_DEST) != 0:
    # ATIME
        TIME = []
        for bus in RESULT:
            for data in DATABASE["ATIME"]:
                data_bus = data.split()
                if data_bus[0] == bus:
                    TIME.append(data_bus[2])
        RESULT = TIME
    
    elif len(QUERY_SOURCE) != 0:
    # DTIME
        TIME = []
        for bus in RESULT:
            for data in DATABASE["DTIME"]:
                data_bus = data.split()
                if data_bus[0] == bus:
                    TIME.append(data_bus[2])
        RESULT = TIME
    
with open('Output/output_d.txt', 'w') as writer:
    writer.writelines("+ Answer: \n")
for result in RESULT:
    with open('Output/output_d.txt', 'w') as writer:
        writer.writelines("+ Answer: \n ")
        for result in RESULT:
            writer.writelines(result + " \n ") 
print(RESULT)