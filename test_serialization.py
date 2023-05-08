import random
import sqlite3
import timeit
import serialize_iterdump
import serialize_pickle
import serialize_JSON
from faker import Faker


fake = Faker()
sample_USERS = [
    (i, fake.name(), random.randint(20, 40))
    for i in range(random.randint(4, 100))
]

def create_DB()-> sqlite3.Connection:
    DBconnection = sqlite3.connect(':memory:')
    DBcursor = DBconnection.cursor()
    DBcursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    DBconnection.commit()
    DBcursor.executemany('''INSERT INTO users VALUES (?, ?, ?)''', sample_USERS)
    DBconnection.commit()
    return DBconnection

def check_DB(connection: sqlite3.Connection)-> bool:
    newcursor = connection.cursor()
    newcursor.execute('''SELECT * FROM users''')
    if newcursor.fetchall() == sample_USERS:
        return True

def expand_seconds(s: float)->tuple:
    seconds = int(s)
    milliseconds = int((s - seconds) * 1000)
    microseconds = int((s - seconds - milliseconds/1000) * 1000000)
    return seconds, milliseconds, microseconds
    

def test_iterdump():
    connection = create_DB()  
    filename = 'serialized_db.sql'
    serialize_iterdump.serialize(connection, filename)
    del connection
    
    newconnection = serialize_iterdump.deserialize(filename)
    assert check_DB(newconnection)
    newconnection.close()
    
def test_pickle():
    connection = create_DB()  
    filename = 'serialized_db.pkl'
    serialize_pickle.serialize(connection, filename)
    del connection
    
    newconnection = serialize_pickle.deserialize(filename)
    assert check_DB(newconnection)
    newconnection.close()    

def test_JSON():
    connection = create_DB()  
    filename = 'serialized_db.json'
    serialize_JSON.serialize(connection, filename)
    del connection
    
    newconnection = serialize_JSON.deserialize(filename)
    assert check_DB(newconnection)
    newconnection.close()    
    

if __name__ == '__main__':
    iterdump_time = timeit.timeit(test_iterdump, number=100)
    seconds, milliseconds, microseconds = expand_seconds(iterdump_time/100)
    print(f'iterdump_time: {seconds} seconds, {milliseconds} milliseconds, {microseconds} microseconds')
        
    
    
    