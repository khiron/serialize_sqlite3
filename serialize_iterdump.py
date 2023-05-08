import sqlite3

def serialize(conn: sqlite3.Connection, filename: str) -> None:
    sql_statements = conn.iterdump()
    with open(filename, 'w') as f:
        for sql in sql_statements:
            f.write(f'{sql}\n')

def deserialize(filename: str)->sqlite3.Connection:
    with open(filename, 'r') as f:
        sql_statements = f.read().splitlines()
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    for sql in sql_statements:
        c.execute(sql)
    return conn
