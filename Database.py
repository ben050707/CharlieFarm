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

# Create the highscores table if it doesn't exist (finally normalized)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS highscores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        highscore INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Create the money table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS money (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        money INTEGER DEFAULT 0,
        flashlightlevel INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Commit the changes
conn.commit()

# Caesar cipher
def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    for char in text:
        if char.islower():  # Shift lowercase letters
            shift_amount = shift if mode == 'encrypt' else -shift
            result += chr((ord(char) - ord('a') + shift_amount) % 26 + ord('a'))
        elif char.isdigit():  # Shift numbers
            shift_amount = shift if mode == 'encrypt' else -shift
            result += str((int(char) + shift_amount) % 10)
        else:
            result += char  # Non-lowercase and non-numeric characters remain unchanged
    return result

# Test the caesar_cipher function
def test_caesar_cipher():
    original_password = "testpassword"
    encrypted = caesar_cipher(original_password, 3, 'encrypt')
    decrypted = caesar_cipher(encrypted, 3, 'decrypt')
    print(f"Original: {original_password}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    assert original_password == decrypted, "Decryption failed!"

test_caesar_cipher()

# Function to add a user
def add_user(username, password):
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    if cursor.fetchone() is None:
        # Insert the new user
        cursor.execute('INSERT INTO users (username, password, inuse) VALUES (?, ?, 0)', (username, caesar_cipher(password, 3, 'encrypt')))
        # Get the newly inserted user's ID
        user_id = cursor.lastrowid
        # Insert a corresponding row into the money table
        cursor.execute('INSERT INTO money (user_id, money, flashlightlevel) VALUES (?, 0, 0)', (user_id,))
        # Insert a corresponding row into the highscores table
        cursor.execute('INSERT INTO highscores (user_id, highscore) VALUES (?, 0)', (user_id,))
        conn.commit()
    else:
        # If the user already exists, log them in
        cursor.execute('UPDATE users SET inuse = 1 WHERE username = ? AND password = ?', (username, caesar_cipher(password, 3, 'encrypt')))
        conn.commit()

# Function to log in a user
def login_user(username, password):
    # Fetch the stored encrypted password from the database
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    
    if result is not None:
        stored_encrypted_password = result[0]  # Get the stored encrypted password
        # Decrypt the stored password
        stored_decrypted_password = caesar_cipher(stored_encrypted_password, 3, 'decrypt')
        # Compare the decrypted stored password with the input password
        if stored_decrypted_password == password:
            # Mark the user as logged in
            cursor.execute('UPDATE users SET inuse = 1 WHERE username = ?', (username,))
            conn.commit()
            return True
    return False

# Function to log out a user
def logout_user():
    cursor.execute('UPDATE users SET inuse = 0 WHERE inuse = 1')
    conn.commit()

# Function to update a user's high score
def update_highscore(username, new_highscore):
    # Step 1: Get the user_id for the given username
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_result = cursor.fetchone()
    
    if user_result is None:
        print(f"User '{username}' does not exist.")
        return
    
    user_id = user_result[0]  # Extract the user_id from the result

    # Step 2: Check if the user already has a high score
    cursor.execute('SELECT highscore FROM highscores WHERE user_id = ?', (user_id,))
    current_highscore = cursor.fetchone()

    if current_highscore is None:
        # If the user doesn't have a high score yet, insert a new row
        cursor.execute('INSERT INTO highscores (user_id, highscore) VALUES (?, ?)', (user_id, new_highscore))
    else:
        # If the user has a high score, update it only if the new score is higher
        if new_highscore > current_highscore[0]:
            cursor.execute('UPDATE highscores SET highscore = ? WHERE user_id = ?', (new_highscore, user_id))
    
    # Commit the changes to the database
    conn.commit()
    print(f"High score updated for user '{username}'.")

# Function to get a user's high score
def get_highscore(username):
    # Step 1: Get the user_id for the given username
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user_result = cursor.fetchone()
    
    if user_result is None:
        print(f"User '{username}' does not exist.")
        return 0
    
    user_id = user_result[0]  # Extract the user_id from the result

    # Step 2: Get the high score for the user
    cursor.execute('SELECT highscore FROM highscores WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    return 0  # Default value if no high score is found

# Function to get the leaderboard (top N high scores)
def get_leaderboard(limit=10):
    cursor.execute('''
        SELECT users.username, highscores.highscore, money.money
        FROM highscores
        JOIN users ON highscores.user_id = users.id
        JOIN money ON highscores.user_id = money.user_id
        ORDER BY highscores.highscore DESC, money.money DESC
        LIMIT ?
    ''', (limit,))
    return cursor.fetchall()

# Function to get the current user's money
def get_money():
    cursor.execute('SELECT money FROM money WHERE user_id = (SELECT id FROM users WHERE inuse = 1)')
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    return 0  # Default value if no money is found

# Function to change the current user's money
def change_money(amount):
    cursor.execute('UPDATE money SET money = money + ? WHERE user_id = (SELECT id FROM users WHERE inuse = 1)', (amount,))
    conn.commit()

# Function to get the current user's inventory (flashlight level)
def get_inventory():
    cursor.execute('SELECT flashlightlevel FROM money WHERE user_id = (SELECT id FROM users WHERE inuse = 1)')
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    return 0  # Default value if no inventory is found

# Function to change the current user's flashlight level
def change_flashlightlevel(amount):
    cursor.execute('UPDATE money SET flashlightlevel = flashlightlevel + ? WHERE user_id = (SELECT id FROM users WHERE inuse = 1)', (amount,))
    conn.commit()