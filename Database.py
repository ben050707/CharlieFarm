import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        inuse BOOLEAN NOT NULL
    )
''')

def add_user(username, password):
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (username, password, inuse) VALUES (?, ?, 0)', (username, password))
        conn.commit()
    else:
        cursor.execute('UPDATE users SET inuse = 1 WHERE username = ? AND password = ?', (username, password))
        conn.commit()

def logout_user():
    cursor.execute('UPDATE users SET inuse = 0')
    conn.commit()

