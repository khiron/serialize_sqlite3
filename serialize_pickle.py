import sqlite3
import pickle

def serialize(conn: sqlite3.Connection, filename: str) -> None:
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM users''')
    with open(filename, 'wb') as f:
        pickle.dump(cursor.fetchall(), f)

def deserialize(filename: str)->sqlite3.Connection:
    with open('serialized_db.pkl', 'rb') as f:
        deserialized_data = pickle.load(f)

    new_conn = sqlite3.connect(':memory:')
    new_c = new_conn.cursor()

    new_c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    new_conn.commit()

    new_c.executemany('''INSERT INTO users VALUES (:id, :name, :age)''', deserialized_data)
    new_conn.commit()
    return new_conn
    
    

