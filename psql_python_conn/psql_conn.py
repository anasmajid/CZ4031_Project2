import psycopg2
from configparser import ConfigParser


def config(filename='D:\witeo\Documents\Computer Science\CZ 4031 Database System Principles\Lab\Lab 2\CZ4031_Project2\psql_python_conn\database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # section - postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    conn = None
    try:
        # read config file (database.ini)
        print("Reading config file")
        params = config()

        # connect to psql
        print('Connecting to PostgreSQL...')
        conn = psycopg2.connect(**params)
		
        # create cursor
        cur = conn.cursor()

        return conn, cur
       
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def disconnect(conn, cur):
    cur.close()
    if conn is not None:
        conn.close()
        print('PostgreSQL connection closed.')


def version(cur):
    # display PostgreSQL server version
    db_version = cur.fetchone()
    print(db_version)


def run_query(cur, query_statements):
    print('\nQuery Start')

    output = []
    for query in query_statements:
        # execute statement
        cur.execute(query)
        # get output from query
        try:
            output.append(cur.fetchall())
        # psycopg2.ProgrammingError occurs when there
        # is no output from PostgreSQL, 
        # eg. in the CREATE TABLES case, need to verify with
        # SELECT table_names as next query
        except psycopg2.ProgrammingError:
            output.append("query executed, no results to fetch")

    # # output to txt file        
    # with open("query_output.txt", "w") as f:

    #     for num, query in enumerate(output):
    #         print("For Query Number", num+1, file=f)
    #         for step in query:
    #             print(step, file=f)
    #         print(file=f)
    #     print('Query End\n', file=f)

    for num, query in enumerate(output):
        print("For Query Number", num+1)
        for step in query:
            print(step)
        print()
    print('Query End\n')
    return output


if __name__ == '__main__':
    # connect function - calls connect() and config()
    db_conn, db_cur = connect()

    # '''Sample Queries'''

    # set query statement
    # version_query = ['SELECT version()']
    # run query statement
    # run_query(db_cur, version_query)

    # # set query statement
    # create_tables_query = [
    #     """
    #     CREATE TABLE vendors (
    #         vendor_id SERIAL PRIMARY KEY,
    #         vendor_name VARCHAR(255) NOT NULL
    #     )
    #     """,
    #     """ CREATE TABLE parts (
    #             part_id SERIAL PRIMARY KEY,
    #             part_name VARCHAR(255) NOT NULL
    #             )
    #     """,
    #     """
    #     CREATE TABLE part_drawings (
    #             part_id INTEGER PRIMARY KEY,
    #             file_extension VARCHAR(5) NOT NULL,
    #             drawing_data BYTEA NOT NULL,
    #             FOREIGN KEY (part_id)
    #             REFERENCES parts (part_id)
    #             ON UPDATE CASCADE ON DELETE CASCADE
    #     )
    #     """,
    #     """
    #     CREATE TABLE vendor_parts (
    #             vendor_id INTEGER NOT NULL,
    #             part_id INTEGER NOT NULL,
    #             PRIMARY KEY (vendor_id , part_id),
    #             FOREIGN KEY (vendor_id)
    #                 REFERENCES vendors (vendor_id)
    #                 ON UPDATE CASCADE ON DELETE CASCADE,
    #             FOREIGN KEY (part_id)
    #                 REFERENCES parts (part_id)
    #                 ON UPDATE CASCADE ON DELETE CASCADE
    #     )
    #     """]
    # # run query statement
    # run_query(db_cur, create_tables_query)

    # # set query statement
    # list_tables_query = ["""SELECT table_name 
    #                         FROM information_schema.tables
    #                         WHERE table_schema = 'public'"""]

    query_sample = [
        """
        explain analyze select 
            l_orderkey, sum( l_extendedprice *( 1-l_discount )) as revenue,
            o_orderdate,
            o_shippriority 
            from
                customer,
                orders,
                lineitem 
            where
                c_mktsegment = 'HOUSEHOLD' 
                and c_custkey = o_custkey 
                and l_orderkey = o_orderkey 
                and o_orderdate < date '1995-03-21' and l_shipdate > date '1955-03-21' 
            group by
                l_orderkey,
                o_orderdate,
                o_shippriority 
            order by
                revenue DESC,
                o_orderdate
                limit 10;
        """,
        """
        set enable_hashagg = OFF;
        set enable_hashjoin = OFF;
        set enable_indexscan = OFF;
        set enable_mergejoin = OFF;
        set enable_nestloop = OFF;
        set enable_seqscan = OFF;

        explain analyze select 
            l_orderkey, sum( l_extendedprice *( 1-l_discount )) as revenue,
            o_orderdate,
            o_shippriority 
            from
                customer,
                orders,
                lineitem 
            where
                c_mktsegment = 'HOUSEHOLD' 
                and c_custkey = o_custkey 
                and l_orderkey = o_orderkey 
                and o_orderdate < date '1995-03-21' and l_shipdate > date '1955-03-21' 
            group by
                l_orderkey,
                o_orderdate,
                o_shippriority 
            order by
                revenue DESC,
                o_orderdate
                limit 10;
        """
        ]
    # # run query statement
    run_query(db_cur, query_sample)

    # '''Sample Queries End'''

    

    disconnect(db_conn, db_cur)