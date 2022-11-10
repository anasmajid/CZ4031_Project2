import psycopg2
from configparser import ConfigParser

import preprocessing

# # global variables
db_cur = None
db_conn = None


# def config(filename='D:\witeo\Documents\Computer Science\CZ 4031 Database System Principles\Lab\Lab 2\CZ4031_Project2\psql_python_conn\database.ini', section='postgresql'):
#     parser = ConfigParser()
#     parser.read(filename)

#     # section - postgresql
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception('Section {0} not found in the {1} file'.format(section, filename))

#     return db


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


def version(cur):
    # display PostgreSQL server version
    db_version = cur.fetchone()
    print(db_version)

def getQueryPlan(sqlInput):
    global db_cur

    # print("sqlInput: ", sqlInput)
    query_statements = preprocessing.processQuery(sqlInput)
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

