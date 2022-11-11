import copy
import scipy.stats as ss
import psycopg2
from graphviz import Graph
from itertools import groupby
from string import ascii_lowercase as alc

# global variables
db_cur = None
db_conn = None

# postgreSQL connection setup
def connect(params_dict):
    global db_conn
    global db_cur
    print("db_conn is ", db_conn)
    if db_conn!= None:
        disconnect(db_conn, db_cur)
    
    # params_dict = {'host': 'localhost', 'database': 'TPC-H', 'user': 'postgres', 'password': 'Superlim016'}
    try:
        # connect to psql
        print('Connecting to PostgreSQL...')
        db_conn = psycopg2.connect(**params_dict)
		
        # create cursor
        db_cur = db_conn.cursor()

        print("Conn is ", db_conn)
        print("cur is ", db_cur)
        return True
       
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        db_conn = None
        return False

def disconnect(conn, cur):
    cur.close()
    if conn is not None:
        conn.close()
        print('PostgreSQL connection closed.')


# def version(cur):
#     # display PostgreSQL server version
#     db_version = cur.fetchone()
#     print(db_version)

def getQueryPlan(sqlInput):
    global db_cur

    # print("sqlInput: ", sqlInput)
    query_statements = processQuery(sqlInput)
    output = []
    for query in query_statements:
        # execute statement
        try:
            db_cur.execute(query)
        except Exception as e:
            print(e)
            return e
        # get output from query
        try:
            output.append(db_cur.fetchall())
        # psycopg2.ProgrammingError occurs when there
        # is no output from PostgreSQL, 
        # eg. in the CREATE TABLES case, need to verify with
        # SELECT table_names as next query
        except psycopg2.ProgrammingError:
            output.append("query executed, no results to fetch")

    # print("output: ", output)
    # print()
    return output
    # strOutput = preprocessing.stringOutput(output)
    # # print()
    # # print("strOutput: ", strOutput)
    # return strOutput

# process query to have 2 queries with explain analyze
def processQuery(input):
    x = "explain analyze " + input
    y = """
    set enable_hashagg = OFF;
    set enable_hashjoin = OFF;
    set enable_indexscan = OFF;
    set enable_mergejoin = OFF;
    set enable_nestloop = OFF;
    set enable_seqscan = OFF;
    """ + x
    x = " ".join(x.strip().split())
    y = " ".join(y.strip().split())

    result = [x, y]
    return result

# reformats output from list list tuple to list string
def stringOutput(plans): 
    res = [] 
    for plan in plans: 
        temp = "" 
        for item in plan: 
            item = item[0]
            print(item)
            temp += item 
        res.append(temp) 
    return res


# graphviz function
def draw(choice, q1_dict, q2_dict):
    q1_edges = []
    q2_edges = []

    # Instantiate a new Graph object
    q1_dot = Graph('QEP', format='png')
    for i in range(len(q1_dict)):
        old_key = next(iter(q1_dict[i]))
        new_key = alc[i]

        print(alc[i], old_key)
        q1_dot.node(str(alc[i]), str(old_key))

        # update dict with the letters
        q1_dict[i][new_key] = q1_dict[i][old_key]
        del q1_dict[i][old_key]

    print(q1_dict)
    
    for i in range(1, len(q1_dict)):
        # visited.append(next(iter(q1_dict[i-1])))
        pair_str = None
        if q1_dict[i-1][next(iter(q1_dict[i-1]))] < q1_dict[i][next(iter(q1_dict[i]))]:
            
            # print(q1_ops_by_level[i-1][next(iter(q1_ops_by_level[i]))])
            pair_str = next(iter(q1_dict[i-1])) + next((iter(q1_dict[i])))
            print(pair_str)
        else:
            curr_val = q1_dict[i][next(iter(q1_dict[i]))]

            for j in range(i-1,-1,-1):
                if curr_val > q1_dict[j][next(iter(q1_dict[j]))]:
                    pair_str = next(iter(q1_dict[j])) + next(iter(q1_dict[i]))
                    print(pair_str)
                    break
        q1_edges.append(pair_str)

    # Instantiate a new Graph object
    q2_dot = Graph('AQP', format='png')
    for i in range(len(q2_dict)):
        old_key = next(iter(q2_dict[i]))
        new_key = alc[i]

        print(alc[i], old_key)
        q2_dot.node(str(alc[i]), str(old_key))

        # update dict with the letters
        q2_dict[i][new_key] = q2_dict[i][old_key]
        del q2_dict[i][old_key]

    print(q2_dict)
    edges = []
    for i in range(1, len(q2_dict)):
        # visited.append(next(iter(q1_dict[i-1])))
        pair_str = None
        if q2_dict[i-1][next(iter(q2_dict[i-1]))] < q2_dict[i][next(iter(q2_dict[i]))]:
            
            # print(q1_ops_by_level[i-1][next(iter(q1_ops_by_level[i]))])
            pair_str = next(iter(q2_dict[i-1])) + next((iter(q2_dict[i])))
            print(pair_str)
        else:
            curr_val = q2_dict[i][next(iter(q2_dict[i]))]

            for j in range(i-1,-1,-1):
                if curr_val > q2_dict[j][next(iter(q2_dict[j]))]:
                    pair_str = next(iter(q2_dict[j])) + next(iter(q2_dict[i]))
                    print(pair_str)
                    break
        q2_edges.append(pair_str)

    if choice == 0:
        q1_dot.edges(q1_edges)
        # q1_dot.view('query1testqep')
        q1_dot.render('query1testqep', view=False)
    elif choice == 1:
        q2_dot.edges(q2_edges)
        # q2_dot.view('query1testaqp')
        q2_dot.render('query1testaqp', view=False)
    else:
        raise(ValueError("Choice of graph is invalid."))
                

def txt2list(input_path="./query_output.txt"):
    lines = []
    output_q1 = []
    output_q2 = []
    ret = []
    with open(input_path, 'r') as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        if lines[i] == "For Query Number 2\n":
            combine = lines[i]
            break
        output_q1.append(lines[i])
        i+=1
    
    while i < len(lines):
        output_q2.append(lines[i])
        i+=1
    
    print("lines")
    print(output_q2)

    return [output_q1, output_q2]


def get_ops_in_order(psql_out):
    break_conditions = ["  (", " on", " us"]
    q1_ops = []
    q2_ops = []

    # queries = [list(group) for k, group in groupby(psql_out.copy(), lambda x: x == "For Query Number 2\n") if not k]
    # q1 = queries[0]
    # q2 = queries[1]
    psql_temp = copy.deepcopy(psql_out)
    q1 = psql_temp[0]
    q2 = psql_temp[1]

    for i in range(len(q1)):
        q1[i] = "('"+q1[i][0]+"')"
    
    for i in range(len(q2)):
        q2[i] = "('"+q2[i][0]+"')"

    for line in q1:
        if "cost" in line:
            for i in range(0, len(line)):
                if (line[i]+line[i+1]+line[i+2]) in break_conditions:
                    q1_ops.append(line[0:i+1])
                    break
            print(q1_ops)
    for line in q2:
        if "cost" in line:
            for i in range(0, len(line)):
                if (line[i]+line[i+1]+line[i+2]) in break_conditions:
                    q2_ops.append(line[0:i+1])
                    break
            print(q2_ops)

    assert not (q1 == [] or q1 == [])

    return q1_ops, q2_ops
    
def find_levels(q1_ops, q2_ops):
    q1_levels_dict_list = []
    q1_spaces_count = []
    q2_levels_dict_list = []
    q2_spaces_count = []

    for op in q1_ops:
        try:
            hyphen_idx = op.index("-")
            op_name_idx = op.index(">")+3
        except ValueError:
            hyphen_idx = 1
            op_name_idx = 2
        q1_spaces_count.append(hyphen_idx)
        q1_levels_dict_list.append({op[op_name_idx:-1] : hyphen_idx})
    ranks = list(ss.rankdata(q1_spaces_count, method='dense'))

    # for elem in q1_levels_dict_list:
    #     elem[next(iter(elem))] = 0

    for i in range(len(q1_levels_dict_list)):
        q1_levels_dict_list[i][next(iter(q1_levels_dict_list[i]))] = ranks[i]
    print(q1_levels_dict_list)

    for op in q2_ops:
        try:
            hyphen_idx = op.index("-")
            op_name_idx = op.index(">")+3
        except ValueError:
            hyphen_idx = 1
            op_name_idx = 2
        q2_spaces_count.append(hyphen_idx)
        q2_levels_dict_list.append({op[op_name_idx:-1] : hyphen_idx})
    ranks = list(ss.rankdata(q2_spaces_count, method='dense'))

    for i in range(len(q2_levels_dict_list)):
        q2_levels_dict_list[i][next(iter(q2_levels_dict_list[i]))] = ranks[i]
    print(q2_levels_dict_list)

    return q1_levels_dict_list, q2_levels_dict_list


def create_graph(choice, psql_out):
    q1_ops, q2_ops = get_ops_in_order(psql_out)
    print("q1_ops: ", q1_ops)
    print("q2_ops: ", q2_ops)
    q1_ops_by_level, q2_ops_by_level = find_levels(q1_ops, q2_ops)
    draw(choice, q1_ops_by_level, q2_ops_by_level)
