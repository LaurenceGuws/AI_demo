import os
import sqlite3
from scripts import model_detect

def build_db(db_file):
    """
    Sets up the SQLite database and creates the required tables.

    Args:
        db_file: The path to the SQLite database file.
    """
    os.makedirs(os.path.dirname(db_file), exist_ok=True)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create conversation table with an is_active field
    cursor.execute("""
    CREATE TABLE conversation (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        is_active BOOLEAN DEFAULT FALSE
    )
    """)

    cursor.execute("""
    CREATE TABLE messages (
        id INTEGER PRIMARY KEY,
        conversation_id INTEGER,
        user_id INTEGER,
        content TEXT,
        FOREIGN KEY(conversation_id) REFERENCES conversation(id)
    )
    """)

    # Create the models table with an is_active field
    cursor.execute("""
    CREATE TABLE models (
        id INTEGER PRIMARY KEY,
        name TEXT,
        is_active BOOLEAN DEFAULT FALSE
    )
    """)

    cursor.execute("""
    CREATE TABLE custom_instructions (
        id INTEGER PRIMARY KEY,
        example_request TEXT,
        example_response TEXT
    )
    """)

    passed_test, failed_test = model_detect.test_models()

    for model_name in passed_test:
        cursor.execute("""
        INSERT INTO models (name, is_active)
        VALUES (?, FALSE)
        """, (model_name,))

    conn.commit()


     # Insert dummy data
    # for i in range(1, 21):  # 5 conversations
    #     conversation_name = f"dummy_conversation_{i}"
    #     cursor.execute("""
    #     INSERT INTO conversation (name, is_active)
    #     VALUES (?, FALSE)
    #     """, (conversation_name,))
    #     conversation_id = cursor.lastrowid
    #     for j in range(20):  # 10 messages for each conversation
    #         user_id = j % 2  # Alternating user_id
    #         content = f"dummy_message_{j+1}_from_user_{user_id}"
    #         cursor.execute("""
    #         INSERT INTO messages (conversation_id, user_id, content)
    #         VALUES (?, ?, ?)
    #         """, (conversation_id, user_id, content))

    # conn.commit()
