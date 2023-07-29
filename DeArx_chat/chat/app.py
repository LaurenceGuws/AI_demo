import base64
import configparser
from flask import Flask, render_template, request, jsonify, session
import sqlite3
from models.gpt import Chat
from setup import build_db

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('conf\config.conf')
app.secret_key = base64.b64decode(config['OpenAI']['API_KEY']).decode()

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

@app.cli.command()
def setup():
    """Run the setup function."""
    build_db('instance/chat.db')  # call the function

if __name__ == '__main__':
    app.run(debug=True)
