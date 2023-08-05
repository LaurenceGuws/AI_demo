window.onload = function() {
    fetchConversations();
}

function fetchConversations() {
    fetch('http://localhost:30000/conversations')
        .then(response => response.json())
        .then(data => {
            const conversationContainer = document.getElementById('conversations');
            data.conversation_names.forEach(name => {
                const button = document.createElement('button');
                button.textContent = name;
                button.onclick = function() { selectConversation(name); };
                conversationContainer.appendChild(button);
            });
        });
}

function selectConversation(name) {
    fetch('http://localhost:30000/conversations/' + name)
        .then(response => response.json())
        .then(data => {
            const chatArea = document.getElementById('chatArea');
            chatArea.innerHTML = '';

            data.conversation_messages.forEach(message => {
                const messageElement = document.createElement('p');
                messageElement.classList.add(message.role === 'user' ? 'message-bubble-user' : 'message-bubble-assistant');
                messageElement.textContent = message.content;
                chatArea.appendChild(messageElement);
            });
        });
}

function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value;
    userInput.value = '';

    fetch('http://localhost:30000/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: { content: message } })
    })
        .then(response => response.json())
        .then(data => {
            const chatArea = document.getElementById('chatArea');
            chatArea.innerHTML = '';

            data.messages.forEach(message => {
                const messageElement = document.createElement('p');
                messageElement.classList.add(message.role === 'user' ? 'message-bubble-user' : 'message-bubble-assistant');
                messageElement.textContent = message.content;
                chatArea.appendChild(messageElement);
            });
        });
}

document.getElementById('sendButton').addEventListener('click', sendMessage);

document.getElementById('optionsButton').addEventListener('click', function() {
    document.getElementById('optionsPopup').style.display = 'block';
});

document.getElementById('closePopup').addEventListener('click', function() {
    document.getElementById('optionsPopup').style.display = 'none';
});

document.getElementById('restartServer').addEventListener('click', function() {
    fetch('http://localhost:30000/restartServer')
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => console.log('Error:', error));
});

document.getElementById('downloadDB').addEventListener('click', function() {
    fetch('http://localhost:30000/downloadDB')
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            // the filename you want
            a.download = 'database.zip';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            alert('Your download has started.');
        })
        .catch(error => console.log('Error:', error));
});


document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_active_model')
    .then(response => response.json())
    .then(data => {
        document.getElementById('modelDisplay').innerHTML = `Active Model: ${data.name}`;
    });
});

document.getElementById('changeModelButton').addEventListener('click', function() {
    // Close the options popup
    document.getElementById('optionsPopup').style.display = 'none';

    // Fetch all model names
    fetch('http://localhost:30000/get_models')
    .then(response => response.json())
    .then(model_names => {
        // Remove existing model buttons
        const popupContent = document.querySelector('#changeModelPopup .popup-content');
        const oldModelButtons = document.querySelectorAll('.model-button');
        oldModelButtons.forEach(button => popupContent.removeChild(button));

        // Create a new button for each model
        model_names.forEach(name => {
            const button = document.createElement('button');
            button.textContent = name;
            button.classList.add('model-button');
            popupContent.insertBefore(button, document.getElementById('closeChangeModelPopup'));

            // When a model button is clicked, send a request to change the active model
            button.addEventListener('click', function() {
                fetch('http://localhost:30000/change_model', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ model_name: name })
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                });
            });
        });

        // Show the change model popup
        document.getElementById('changeModelPopup').style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('closeChangeModelPopup').addEventListener('click', function() {
    document.getElementById('changeModelPopup').style.display = 'none';
});

document.getElementById('customInstructionsButton').addEventListener('click', function() {
    document.getElementById('optionsPopup').style.display = 'none';
    document.getElementById('customInstructionsPopup').style.display = 'block';
});

document.getElementById('submitInstructions').addEventListener('click', function() {
    var exampleRequest = document.getElementById('exampleRequest').value;
    var exampleResponse = document.getElementById('exampleResponse').value;
    var instructions = {example_request: exampleRequest, example_response: exampleResponse};
    fetch('custom_instructions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(instructions)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.log('Error:', error));
});

document.getElementById('closeCustomInstructions').addEventListener('click', function() {
    document.getElementById('customInstructionsPopup').style.display = 'none';
});
