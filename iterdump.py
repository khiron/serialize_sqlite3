import sqlite3

def serialize(conn: sqlite3.Connection, filename: str) -> None:
    # Step 1: Create an in-memory SQLite database and add some data to it
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()

    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    conn.commit()

    sample_data = [(1, 'Alice', 30), (2, 'Bob', 25), (3, 'Charlie', 35)]

    c.executemany('''INSERT INTO users VALUES (?, ?, ?)''', sample_data)
    conn.commit()

    # Step 2: Use iterdump() to generate SQL statements representing the database structure and data
    sql_statements = conn.iterdump()

    # Step 3: Save the generated SQL statements to a file
    with open(filename, 'w') as f:
        for sql in sql_statements:
            f.write(f'{sql}\n')

    # Close the database connection
    conn.close()

def deserialize(filename: str)->sqlite3.Connection:
    # Step 1: Open the file containing the SQL statements and read its contents
    with open(filename, 'r') as f:
        sql_statements = f.read().splitlines()

    # Step 2: Create a new in-memory SQLite database
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()

    # Step 3: Execute the SQL statements to recreate the database structure and data
    for sql in sql_statements:
        c.execute(sql)
    return conn
