import sqlite3
import msgpack


def serialize(conn: sqlite3.Connection, filename: str) -> None:
    c = conn.cursor()
    c.execute('''SELECT * FROM users''')
    data = [{'id': row[0], 'name': row[1], 'age': row[2]} for row in c.fetchall()]

    with open(filename, 'wb') as f:
        f.write(msgpack.packb(data))

def deserialize(filename: str)->sqlite3.Connection:
    # Deserialize the MessagePack data back into a Python data structure
    with open(filename, 'rb') as f:
        deserialized_data = msgpack.unpackb(f.read(), raw=False)

    new_conn = sqlite3.connect(':memory:')
    new_c = new_conn.cursor()

    new_c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    new_conn.commit()

    new_c.executemany('''INSERT INTO users VALUES (:id, :name, :age)''', deserialized_data)
    new_conn.commit()
    return new_conn
