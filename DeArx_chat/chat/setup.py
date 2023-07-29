import os
import sqlite3

def build_db(db_file):
    """
    Sets up the SQLite database and creates the required tables.

    Args:
        db_file: The path to the SQLite database file.
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create conversation table
    cursor.execute("""
    CREATE TABLE conversation (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)

    # Create messages table
    cursor.execute("""
    CREATE TABLE messages (
        id INTEGER PRIMARY KEY,
        conversation_id INTEGER,
        user_id INTEGER,
        content TEXT,
        FOREIGN KEY(conversation_id) REFERENCES conversation(id)
    )
    """)
    # Create the user preferences table.
    cursor.execute('CREATE TABLE user_preferences (id INTEGER PRIMARY KEY, prompt TEXT, answer TEXT, created_at TIMESTAMP)')

    # Create the models table.
    cursor.execute('CREATE TABLE models (id INTEGER PRIMARY KEY, name TEXT, description TEXT, created_at TIMESTAMP)')

    conn.commit()

