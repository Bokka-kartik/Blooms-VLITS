# import sqlite3
# import bcrypt

# import sqlite3

# DB_PATH = "new_database.db"

# def create_tables():
#     """Creates necessary tables if they don't exist."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # ✅ Create Users Table
#     cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         username TEXT UNIQUE,
#                         password TEXT,
#                         role TEXT CHECK(role IN ('admin', 'user')))''')

#     # ✅ Create Uploads Table
#     cursor.execute('''CREATE TABLE IF NOT EXISTS uploads (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         admin TEXT,
#                         subject TEXT,
#                         file_name TEXT,
#                         dataset_path TEXT,
#                         uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

#     conn.commit()
#     conn.close()

# def register_user(username, password, role):
#     """Registers a new user with hashed password."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     try:
#         cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
#                        (username, hashed_pw, role))
#         conn.commit()
#         return True
#     except sqlite3.IntegrityError:
#         return False
#     finally:
#         conn.close()

# def authenticate_user(username, password):
#     """Checks login credentials."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
#     user = cursor.fetchone()
#     conn.close()
    
#     if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
#         return user[1]
#     return None

# # def authenticate_user(username, password):
# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
# #     result = cursor.fetchone()
# #     conn.close()
# #     if result and (result[1] == password):
# #         return result[1]
# #     else:
# #         return None
# # ✅ Ensure tables exist before using the database
# create_tables()
import sqlite3
import bcrypt # type: ignore

import sqlite3

DB_PATH = "new_database.db"
def create_tables():
    """Creates necessary tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT CHECK(role IN ('admin', 'user')))''')

    # Create Uploads Table - Add username field for tracking
    cursor.execute('''CREATE TABLE IF NOT EXISTS uploads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        admin TEXT,
                        subject TEXT,
                        file_name TEXT,
                        dataset_path TEXT,
                        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                        
    # Create Generated Papers Table - New table for tracking user-generated papers
    cursor.execute('''CREATE TABLE IF NOT EXISTS generated_papers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        subject TEXT,
                        file_path TEXT,
                        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()

def register_user(username, password, role):
    """Registers a new user with hashed password."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hashed_pw, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    """Checks login credentials."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return user[1]
    return None

create_tables()
