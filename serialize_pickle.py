import sqlite3
import pickle

def serialize(conn: sqlite3.Connection, filename: str) -> None:
    cursor = conn.cursor()
    with open(filename, 'wb') as f:
        pickle.dump(cursor.fetchall(), f)

def deserialize(filename: str)->sqlite3.Connection:
    with open('serialized_db.pkl', 'rb') as f:
        deserialized_data = pickle.load(f)

