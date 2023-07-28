import sqlite3

def setup(db_file):
  """
  Sets up the SQLite database and creates the required tables.

  Args:
    db_file: The path to the SQLite database file.
  """

  conn = sqlite3.connect(db_file)
  cursor = conn.cursor()

  # Create the conversations table.
  cursor.execute('CREATE TABLE conversations (id INTEGER PRIMARY KEY, prompt TEXT, response TEXT, model TEXT, created_at TIMESTAMP)')

  # Create the user preferences table.
  cursor.execute('CREATE TABLE user_preferences (id INTEGER PRIMARY KEY, prompt TEXT, answer TEXT, created_at TIMESTAMP)')

  # Create the models table.
  cursor.execute('CREATE TABLE models (id INTEGER PRIMARY KEY, name TEXT, description TEXT, created_at TIMESTAMP)')

  conn.commit()

