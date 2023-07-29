// When the page loads, fetch the conversations and create buttons
window.addEventListener('load', function() {
    fetch('/conversations')
    .then(response => response.json())
    .then(data => {
        var conversationsPane = document.getElementById('conversationsPane');
        data.conversations.forEach(function(conversation) {
            var button = document.createElement('button');
            button.textContent = conversation;
            button.addEventListener('click', function() {
                fetch('/conversations/' + encodeURIComponent(conversation))
                .then(response => response.json())
                .then(data => {
                    var chatbox = document.getElementById('chatbox');
                    chatbox.textContent = '';  // Clear the chatbox
                    data.messages.forEach(function(message, index) {
                        // Display each message in the chatbox with the appropriate CSS class
                        var messageElement = document.createElement('p');
                        messageElement.textContent = message;
                        messageElement.className = (index % 2 == 0) ? 'user-message' : 'bot-message';
                        chatbox.appendChild(messageElement);
                    });
                })
                .catch(error => console.error('Error:', error));
            });
            conversationsPane.appendChild(button);
        });
    })
    .catch(error => console.error('Error:', error));
});

// Existing code for sending messages
document.getElementById('messageForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var messageInput = document.getElementById('messageInput');
    var message = messageInput.value;
    var chatbox = document.getElementById('chatbox');

    // Display the message in the chatbox
    var userMessage = document.createElement('p');
    userMessage.textContent = message;
    userMessage.className = 'user-message';
    chatbox.appendChild(userMessage);
    chatbox.scrollTop = chatbox.scrollHeight;

    // Send message to server and log response
    fetch('/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'message=' + encodeURIComponent(message)
    })
    .then(response => response.json())
    .then(data => {
        // Display the response in the chatbox
        var botMessage = document.createElement('p');
        botMessage.textContent = data.response;
        botMessage.className = 'bot-message';
        chatbox.appendChild(botMessage);
        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => console.error('Error:', error));

    // Clear the input field and refocus for the next message
    messageInput.value = '';
    messageInput.focus();
});
