import sqlite3
from User_pb2 import Database, User

def serialize(conn: sqlite3.Connection, filename: str) -> None:
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    data = [User(id=row[0], name=row[1], age=row[2]) for row in c.fetchall()]

    db = Database()
    db.users.extend(data)

    with open(filename, 'wb') as f:
        f.write(db.SerializeToString())

def deserialize(filename: str) -> sqlite3.Connection:
    db = Database()

    with open(filename, 'rb') as f:
        db.ParseFromString(f.read())

    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

    data = [{'id': user.id, 'name': user.name, 'age': user.age} for user in db.users]
    c.executemany("INSERT INTO users VALUES (:id, :name, :age)", data)
    conn.commit()

    return conn


