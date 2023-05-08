import sqlite3
import json

def serialize(conn: sqlite3.Connection, filename: str) -> None:
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users''')
    allrows = cursor.fetchall()
    data = [{'id': row[0], 'name': row[1], 'age': row[2]} for row in allrows]

    # Serialize the Python data structure to JSON format
    with open(filename, 'w') as f:
        json.dump(data, f)

def deserialize(filename: str)->sqlite3.Connection:
    with open(filename, 'r') as f:
        deserialized_data = json.load(f)

    new_conn = sqlite3.connect(':memory:')
    new_c = new_conn.cursor()

    new_c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    new_conn.commit()

    new_c.executemany('''INSERT INTO users VALUES (:id, :name, :age)''', deserialized_data)
    new_conn.commit()
    return new_conn

