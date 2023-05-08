import sqlite3
import csv

def serialize(conn: sqlite3.Connection, filename: str) -> None:
    c = conn.cursor()
    c.execute('''SELECT * FROM users''')
    data = [row for row in c.fetchall()]

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'age']) 
        writer.writerows(data) 

def deserialize(filename: str)->sqlite3.Connection:
    with open('serialized_db.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        deserialized_data = [tuple(row) for row in reader]

    new_conn = sqlite3.connect(':memory:')
    new_c = new_conn.cursor()

    new_c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    new_conn.commit()

    new_c.executemany('''INSERT INTO users VALUES (:id, :name, :age)''', deserialized_data)
    new_conn.commit()
    return new_conn

