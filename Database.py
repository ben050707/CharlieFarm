import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        inuse BOOLEAN NOT NULL
    )
''')

# Create the highscores table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS highscores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        highscore INTEGER DEFAULT 0
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS money (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        money INTEGER DEFAULT 0
    )
''')
    
# Commit the changes
conn.commit()

#Caeser cipher
def caesar_cipher(text, shift, mode='encrypt'):

    result = ""

    for char in text:
        if char.islower():  # Shift lowercase letters
            shift_amount = shift if mode == 'encrypt' else -shift
            result += chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a'))
        if char.isdigit():  # Shift numbers
            shift_amount = shift if mode == 'encrypt' else -shift
            result += str((int(char) + shift_amount) % 10)
        else:
            result += char  # Non-lowercase and non-numeric characters remain unchanged

    return result

def add_user(username, password):
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (username, password, inuse) VALUES (?, ?, 0)', (username, caesar_cipher(password, 3, 'encrypt')))
        cursor.execute('INSERT INTO highscores (username, highscore) VALUES (?, 0)', (username,))
        cursor.execute('INSERT INTO money (money) VALUES (0)')
        conn.commit()
    else:
        cursor.execute('UPDATE users SET inuse = 1 WHERE username = ? AND password = ?', (username, caesar_cipher(password, 3, 'encrypt')))
        conn.commit()
    
# Function to log in a user
def login_user(username, password):
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    
    if result is not None:
        stored_password = caesar_cipher(result[0], 3, 'decrypt')  # Decrypt the stored password using Caesar cipher result[0]
        if stored_password == password:  # Compare plain-text passwords
            cursor.execute('UPDATE users SET inuse = 1 WHERE username = ?', (username,))
            conn.commit()
            return True
    return False

# Function to log out a user
def logout_user():
    cursor.execute('UPDATE users SET inuse = 0')
    conn.commit()

# Function to update a user's high score
def update_highscore(username, new_highscore):
    cursor.execute('SELECT highscore FROM highscores WHERE username = ?', (username,))
    current_highscore = cursor.fetchone()
    if current_highscore is None:
        cursor.execute('INSERT INTO highscores (username, highscore) VALUES (?, ?)', (username, new_highscore))
    else:
        if new_highscore > current_highscore[0]:
            cursor.execute('UPDATE highscores SET highscore = ? WHERE username = ?', (new_highscore, username))
    conn.commit()

# Function to get a user's high score
def get_highscore(username):
    cursor.execute('SELECT highscore FROM highscores WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    return 0

# Function to get the leaderboard (top N high scores)
def get_leaderboard(limit=10):
    cursor.execute('SELECT username, highscore FROM highscores ORDER BY highscore DESC LIMIT ?', (limit,))
    return cursor.fetchall()

def get_money():
    cursor.execute('SELECT money FROM money WHERE id = (SELECT id FROM users WHERE inuse = 1)') #subquery
    return cursor.fetchone()

def change_money(amount):
    cursor.execute('UPDATE money SET money = money + ? WHERE id = (SELECT id FROM users WHERE inuse = 1)', (amount,))
    conn.commit()

def moneyhighscore():
    cursor.execute('SELECT users.username, money.money FROM users, money WHERE money.id = users.id ORDER BY money DESC LIMIT 10')
    return cursor.fetchall()

