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

initiate_db()

