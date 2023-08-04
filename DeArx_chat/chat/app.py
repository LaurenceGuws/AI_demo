import base64
import importlib
import logging
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sqlite3
from setup import build_db
import json

app = Flask(__name__)
CORS(app)
app.secret_key = base64.b64decode(os.getenv('OPENAI_API_KEY')).decode()

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    data = request.get_json()
    message = data.get('message')

    # Get the conversation from the session, or start a new one
    conversation = session.get('conversation')
    print(message)
    # If there's no active conversation in the session
    if not conversation:
        # Start a new conversation with the name as the user's message
        conversation = {'name': message, 'messages': []}
        message_content = message['content'] 
        # Write the new conversation to the database
        conn = sqlite3.connect('instance/chat.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO conversation (name) VALUES (?)', (message_content,))
        conversation_id = cursor.lastrowid  # Get the ID of the new conversation
        conn.commit()
        conn.close()

        # Store the conversation ID in the session
        session['conversation_id'] = conversation_id

    # Add the new message to the conversation
    conversation['messages'].append({'role': 'user', 'content': message_content})

    # Prepare messages for GPT
    messages_for_gpt = [{'role': m['role'], 'content': m['content']} for m in conversation['messages']]
    messages_for_gpt.insert(0, {'role': 'system', 'content': 'Welcome to the chat!'})

    # Dynamically import the model module based on the active_model session variable
    active_model = session.get('active_model') or 'gpt'
    model_module = importlib.import_module(f'models.{active_model}')

    # Use the dynamically imported module to interact
    response = model_module.interact(messages_for_gpt)

    # Add the bot's response to the conversation
    conversation['messages'].append({'role': 'assistant', 'content': response})

    # Save the updated conversation in the session
    session['conversation'] = conversation

    # Write the messages to the database
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO messages (conversation_id, user_id, content) VALUES (?, ?, ?)', 
                       [(session['conversation_id'], (0 if message['role'] == 'assistant' else 1), message['content']) for message in conversation['messages']])
    conn.commit()
    conn.close()
    logging.debug("Server response: %s", jsonify({'messages': conversation['messages']}))
    return jsonify({'messages': conversation['messages']})

@app.route('/conversations', methods=['GET'])
def get_conversations():
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM conversation')
    conversations = [row[0] for row in cursor.fetchall()]
    print(f'Fetched {len(conversations)} conversations')  # Print the number of fetched conversations
    conn.close()
    return jsonify({'conversations': conversations})

@app.route('/conversations/<name>', methods=['GET'])
def get_conversation(name):
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM messages JOIN conversation ON messages.conversation_id = conversation.id WHERE conversation.name = ?', (name,))
    messages = [{'role': 'user' if i % 2 == 0 else 'assistant', 'content': row[0]} for i, row in enumerate(cursor.fetchall())]
    conn.close()
    return jsonify({'messages': messages})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('files', filename))
        return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/change_model', methods=['POST'])
def change_model():
    model_name = request.get_json().get('model_name')
    session['active_model'] = model_name

    return jsonify({
        'message': 'Changed to model ' + model_name  
    }), 200


@app.route('/get_models', methods=['GET'])
def get_models():
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM models')
    models = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(models)

@app.route('/custom_instructions', methods=['POST'])
def custom_instructions():
    instructions = request.get_json()

    # Write the new instructions to the database
    conn = sqlite3.connect('instance/chat.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO custom_instructions (example_request, example_response) VALUES (?, ?)', 
                   (instructions['example_request'], instructions['example_response']))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Custom instructions saved successfully'}), 200


@app.cli.command()
def setup():
    """Run the setup function."""
    build_db('instance/chat.db')  # call the function

if __name__ == '__main__':
    app.run(debug=True)
