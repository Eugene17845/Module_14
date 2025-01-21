import sqlite3


def initiate_db():
    connection = sqlite3.connect('base_d.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    prise INTEGER NOT NULL
    )''')
    for i in range(1, 5):
        cursor.execute("REPLACE INTO Products (id, title, description, prise) VALUES(?, ?, ?, ?)",
                       (f'{i}',f"Продукт{i}", f"Описание {i}", f"Цена {i*100}"))

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('base_d.db')
    cursor = connection.cursor()

    cursor.execute('SELECT title, description, prise FROM Products')
    users = cursor.fetchall()
    connection.commit()
    connection.close()
    return users

def add_user(username, email, age):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute("SELECT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
                   (f'{username}', f'{email}', f'{age}', 1000))

def is_included(username):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    cursor.execute('SELECT username FROM Users')
    users = cursor.fetchall()
    for i in users:
        if username in i:
            return True
        else:
            return False


initiate_db()

