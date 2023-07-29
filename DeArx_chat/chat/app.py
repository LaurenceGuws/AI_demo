from flask import Flask, render_template, request, jsonify
from models.gpt import Chat
from setup import build_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    message = request.form.get('message')
    print(message)
    # Prepare messages for GPT
    messages = ["Welcome to the chat!", message]
    response = Chat.chat_gpt_interact(messages)
    print(response)
    return jsonify({'response': response})

@app.cli.command()
def setup():
    """Run the setup function."""
    build_db('instance/chat.db')  # call the function

if __name__ == '__main__':
    app.run(debug=True)
