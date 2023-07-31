import base64
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import os
import sqlite3
from models.gpt import Chat
from setup import build_db

app = Flask(__name__)
app.secret_key = base64.b64decode(os.getenv('OPENAI_API_KEY')).decode()

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    message = request.form.get('message')

    # Get the conversation from the session, or start a new one
    conversation = session.get('conversation')

    # If there's no active conversation in the session
    if not conversation:
        # Start a new conversation with the name as the user's message
        conversation = {'name': message, 'messages': []}

        # Write the new conversation to the database
        conn = sqlite3.connect('instance/chat.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO conversation (name) VALUES (?)', (message,))
        conversation_id = cursor.lastrowid  # Get the ID of the new conversation
        conn.commit()
        conn.close()

        # Store the conversation ID in the session
        session['conversation_id'] = conversation_id

    # Add the new message to the conversation
    conversation['messages'].append({'role': 'user', 'content': message})

    # Prepare messages for GPT
    messages_for_gpt = [{'role': m['role'], 'content': m['content']} for m in conversation['messages']]
    messages_for_gpt.insert(0, {'role': 'system', 'content': 'Welcome to the chat!'})

    response = Chat.chat_gpt_interact(messages_for_gpt)

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

    return jsonify({'response': response})

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
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify({'messages': messages})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('files', filename))
        return 'File uploaded successfully', 200
    
@app.route('/models', methods=['GET'])
def get_models():
    # Return a list of configured models
    models = ["GPT-3.5", "Bard"]  # replace with your actual models
    return jsonify({'models': models})

@app.route('/change_model', methods=['POST'])
def change_model():
    model = request.form.get('model')
    # change the model here
    return 'Model changed', 200

@app.cli.command()
def setup():
    """Run the setup function."""
    build_db('instance/chat.db')  # call the function

if __name__ == '__main__':
    app.run(debug=True)
