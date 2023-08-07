import base64
import importlib
import zipfile
import pandas as pd
from zipfile import ZIP_FILECOUNT_LIMIT
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sqlite3
from setup import build_db
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'Dev'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/message', methods=['POST'])
def message():
    # Fetch the message from the incoming JSON
    data = request.get_json()
    message = data.get('message')
    message_content = message['content']

    # Connect to the database and fetch the active conversation along with its messages
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()

    # Fetch the active conversation
    cursor.execute('SELECT * FROM conversation WHERE is_active = ?', (True,))
    conversation = cursor.fetchone()

    # If there is an active conversation, fetch its messages
    if conversation:
        conversation_id = conversation[0]  # Assuming 'id' is the first column
        cursor.execute('SELECT content, user_id FROM messages WHERE conversation_id = ?', (conversation_id,))
        messages = cursor.fetchall()

        # Format the messages and add them to the conversation
        formatted_messages = [{'role': 'user' if msg[1] == 1 else 'assistant', 'content': msg[0]} for msg in messages]
        conversation = {'name': conversation[1], 'messages': formatted_messages}
    else:
        # If there is no active conversation, create a new one and write it to the database
        conversation = {'name': message_content[:20], 'messages': []}
        cursor.execute('INSERT INTO conversation (name, is_active) VALUES (?, ?)', (message_content[:20], True))

    # Commit changes and close the database connection
    conn.commit()
    conn.close()

    # Append the new message from the user to the conversation
    conversation['messages'].append({'role': 'user', 'content': message_content})

    # Format the messages for use with the LLM
    messages_for_llm = [{'role': m['role'], 'content': m['content']} for m in conversation['messages']]


    # Fetch the active model from the database
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM models WHERE is_active = ?', (True,))
    active_model_result = cursor.fetchone()
    conn.close()

    # If there is an active model, get its name
    if active_model_result is not None:
        active_model = active_model_result[0]
    else:
        # Handle the case where there is no active model
        # For example, you could set active_model to a default value
        active_model = 'test'

    # Import the model's module and use it to generate a response
    model_module = importlib.import_module(f'models.{active_model}')
    response = model_module.interact(messages_for_llm)

    # Append the bot's response to the conversation
    conversation['messages'].append({'role': 'assistant', 'content': response})

    # Fetch the active conversation's id from the database
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM conversation WHERE is_active = ?', (True,))
    conversation_id = cursor.fetchone()[0]
    conn.close()

    # Connect to the database and write the last 2 messages (user's and assistant's)
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO messages (conversation_id, user_id, content) VALUES (?, ?, ?)', 
                       [(conversation_id, (0 if message['role'] == 'assistant' else 1), message['content']) for message in conversation['messages'][-2:]])
    conn.commit()
    conn.close()

    # Return the updated conversation
    return jsonify({'messages': conversation['messages']}), 200

@app.route('/conversations', methods=['GET'])
def get_conversations():
    # Connect to the database and fetch all conversation names
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM conversation')
    conversation_names = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Return the conversation names
    return jsonify({'conversation_names': conversation_names}), 200

@app.route('/conversations/<name>', methods=['GET'])
def get_conversation(name):
    # Connect to the database and fetch the messages of the specified conversation
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM messages JOIN conversation ON messages.conversation_id = conversation.id WHERE conversation.name = ?', (name,))
    conversation_messages = [{'role': 'user' if i % 2 == 0 else 'assistant', 'content': row[0]} for i, row in enumerate(cursor.fetchall())]
    conn.close()

    # Return the messages of the specified conversation
    return jsonify({'conversation_messages': conversation_messages}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request contains a file part
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    # Get the file from the request
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Save the file if it exists
    if file:
        # Create the directory if it doesn't exist
        os.makedirs('files', exist_ok=True)

        # Save the file
        filename = secure_filename(file.filename)
        file.save(os.path.join('files', filename))

        # Return a success message
        return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/change_model', methods=['POST'])
def change_model():
    # Fetch the name of the new model from the incoming JSON
    model_name = request.get_json().get('model_name')

    # Connect to the database to set the new active model
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE models SET is_active = ?', (False,))
    cursor.execute('UPDATE models SET is_active = ? WHERE name = ?', (True, model_name))
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({
        'message': 'Changed to model ' + model_name  
    }), 200

@app.route('/get_models', methods=['GET'])
def get_models():
    # Connect to the database and fetch all model names
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM models')
    model_names = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Return the model names
    return jsonify(model_names), 200

@app.route('/custom_instructions', methods=['POST'])
def custom_instructions():
    # Fetch the instructions from the incoming JSON
    instructions = request.get_json()

    # Connect to the database and write the new instructions
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO custom_instructions (example_request, example_response) VALUES (?, ?)', 
                   (instructions['example_request'], instructions['example_response']))
    conn.commit()
    conn.close()

    # Check if there are less than 2 messages in the database for the active conversation, and if so, create enough to reach 2
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM messages WHERE conversation_id = (SELECT id FROM conversation WHERE is_active = ?)', (True,))
    count = cursor.fetchone()[0]
    if count < 2:
        for _ in range(2 - count):
            cursor.execute('INSERT INTO messages (conversation_id, user_id, content) VALUES ((SELECT id FROM conversation WHERE is_active = ?), ?, ?)', (True, 0, ''))
    conn.commit()
    conn.close()

    # Override the first 2 messages of the active conversation with the custom instructions
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE messages SET content = ? WHERE id IN (SELECT id FROM messages WHERE conversation_id = (SELECT id FROM conversation WHERE is_active = ?) ORDER BY id ASC LIMIT 1)', (instructions['example_request'], True))
    cursor.execute('UPDATE messages SET content = ? WHERE id IN (SELECT id FROM messages WHERE conversation_id = (SELECT id FROM conversation WHERE is_active = ?) ORDER BY id ASC LIMIT 1, 1)', (instructions['example_response'], True))
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({'message': 'Custom instructions saved successfully'}), 200

@app.route('/restartServer', methods=['GET'])
def restart_server():
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()

    # Clear the conversation and message tables
    cursor.execute('DELETE FROM conversation')
    cursor.execute('DELETE FROM messages')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({'message': 'Server restarted successfully'}), 200


@app.route('/downloadDB')
def download_db():
    # Define the path to the SQLite file
    db_path = "instance/chat.db"

    # Export the tables of the database to CSV files and zip them
    export_tables_to_csv(db_path)
    
    # Return the zip file
    return send_file('tables.zip', mimetype='application/zip', as_attachment=True, download_name='tables.zip'), 200

def export_tables_to_csv(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch the names of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Create a ZipFile object
    with zipfile.ZipFile('tables.zip', 'w') as zipf:
        # Export each table to a CSV file
        for table in tables:
            table_name = table[0]
            print(f"Processing table: {table_name}")
            df = pd.read_sql_query(f"SELECT * from {table_name}", conn)
            csv_path = f"{table_name}.csv"
            df.to_csv(csv_path, index=False)

            # Add the CSV file to the zip
            zipf.write(csv_path)

    conn.close()

    
    conn.close()

@app.route('/get_active_model', methods=['GET'])
def get_active_model():
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM models WHERE is_active = ?', (True,))
    active_model_result = cursor.fetchone()
    conn.close()

    if active_model_result is None:
        # Set 'Test' as active model if no model is active
        conn = sqlite3.connect('instance/chat.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE models SET is_active = ? WHERE name = ?', (True, 'Test'))
        conn.commit()
        conn.close()

        active_model_name = 'Test'
    else:
        active_model_name = active_model_result[0]

    return jsonify({'name': active_model_name})

@app.cli.command()
def setup():
    """Run the setup function."""
    build_db('instance/chat.db')

if __name__ == '__main__':
    app.run(debug=True)
