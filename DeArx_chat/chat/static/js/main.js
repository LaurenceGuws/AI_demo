window.onload = function() {
    fetchConversations();
    fetchActiveConversation();
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

function fetchActiveConversation() {
    fetch('http://localhost:30000/active_conversation')
        .then(response => response.json())
        .then(data => {
            const chatArea = document.getElementById('chatArea');
            chatArea.innerHTML = ''; // Clear the chat area

            data.conversation_messages.forEach(message => {
                const messageElement = document.createElement('p');
                messageElement.classList.add(message.role === 'user' ? 'message-bubble-user' : 'message-bubble-assistant');
                messageElement.textContent = message.content;
                chatArea.appendChild(messageElement);
            });

            scrollToBottom();  // Ensure the latest messages are in view
        })
        .catch(error => {
            console.error("There was an error fetching the active conversation:", error);
            alert("There was an error fetching the active conversation. Please try again.");
        });
}

function selectConversation(name) {
    // Store the selected conversation's name for later use
    document.getElementById('conversationOptionsPopup').dataset.selectedConversation = name;

    // Display the popup
    document.getElementById('conversationOptionsPopup').style.display = 'block';
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

            scrollToBottom();  // Ensure the latest messages are in view
        });
}


function scrollToBottom() {
    var chatArea = document.getElementById("chatArea");
    chatArea.scrollTop = chatArea.scrollHeight;
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
            location.reload();
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
            document.getElementById('optionsPopup').style.display = 'none';
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
                    location.reload();
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
        document.getElementById('customInstructionsPopup').style.display = 'none';
    })
    .catch(error => console.log('Error:', error));
});

document.getElementById('closeCustomInstructions').addEventListener('click', function() {
    document.getElementById('customInstructionsPopup').style.display = 'none';
});

document.getElementById('startNewConversation').addEventListener('click', function() {
    fetch('http://localhost:30000/new_conversation')
        .then(response => response.json())
        .then(data => {
            if (data.message === 'New conversation started') {
                // Clear the chat area
                const chatArea = document.getElementById('chatArea');
                chatArea.innerHTML = '';

                // Refresh the page to fetch updated conversations
                location.reload();
            } else {
                alert('Error starting a new conversation. Please try again.');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('Error starting a new conversation. Please try again.');
        });
});

document.getElementById('changeConversation').addEventListener('click', function() {
    const name = document.getElementById('conversationOptionsPopup').dataset.selectedConversation;

    // Fetch the selected conversation and update the chat area
    fetch('http://localhost:30000/conversations/' + name)
        .then(response => response.json())
        .then(data => {
            const chatArea = document.getElementById('chatArea');
            chatArea.innerHTML = ''; // Clear the chat area

            data.conversation_messages.forEach(message => {
                const messageElement = document.createElement('p');
                messageElement.classList.add(message.role === 'user' ? 'message-bubble-user' : 'message-bubble-assistant');
                messageElement.textContent = message.content;
                chatArea.appendChild(messageElement);
            });
        })
        .catch(error => {
            console.error("Error fetching the conversation:", error);
            alert("There was an error fetching the selected conversation. Please try again.");
        })
        .finally(() => {
            // Close the popup after the action, regardless of success or error
            document.getElementById('conversationOptionsPopup').style.display = 'none';
        });
});

document.getElementById('deleteConversation').addEventListener('click', function() {
    const name = document.getElementById('conversationOptionsPopup').dataset.selectedConversation;

    // Send a DELETE request to the backend to delete the selected conversation
    fetch('http://localhost:30000/delete_conversation/' + name, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error("Error deleting the conversation:", error);
        alert("There was an error deleting the selected conversation. Please try again.");
    })
    .finally(() => {
        // Close the popup after the action, regardless of success or error
        document.getElementById('conversationOptionsPopup').style.display = 'none';
        location.reload();
    });
});


document.getElementById('closeConversationOptionsPopup').addEventListener('click', function() {
    document.getElementById('conversationOptionsPopup').style.display = 'none';
});
