import datetime
import sqlite3
import timeit
import iterdump


def create_DB()-> sqlite3.Connection:
    DBconnection = sqlite3.connect(':memory:')
    DBcursor = DBconnection.cursor()
    DBcursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    DBconnection.commit()
    sample_data = [(1, 'Alice', 30), (2, 'Bob', 25), (3, 'Charlie', 35)]
    DBcursor.executemany('''INSERT INTO users VALUES (?, ?, ?)''', sample_data)
    DBconnection.commit()
    return DBconnection

def check_DB(connection: sqlite3.Connection)-> bool:
    newcursor = connection.cursor()
    newcursor.execute('''SELECT * FROM users''')
    if newcursor.fetchall() == [(1, 'Alice', 30), (2, 'Bob', 25), (3, 'Charlie', 35)]:
        return True

def expand_seconds(s: float)->tuple:
    seconds = int(s)
    milliseconds = int((s - seconds) * 1000)
    microseconds = int((s - seconds - milliseconds/1000) * 1000000)
    return seconds, milliseconds, microseconds
    

def test_iterdump():
    connection = create_DB()  
    filename = 'iterdump.sql'
    iterdump.serialize(connection, filename)
    del connection
    
    newconnection = iterdump.deserialize(filename)
    assert check_DB(newconnection)
    newconnection.close()
    

if __name__ == '__main__':
    iterdump_time = timeit.timeit(test_iterdump, number=100)
    seconds, milliseconds, microseconds = expand_seconds(iterdump_time/100)
    print(f'iterdump_time: {seconds} seconds, {milliseconds} milliseconds, {microseconds} microseconds')
        
    
    
    