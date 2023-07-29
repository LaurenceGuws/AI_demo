
document.getElementById('messageForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var messageInput = document.getElementById('messageInput');
    var message = messageInput.value;
    var chatbox = document.getElementById('chatbox');

    // Display the message in the chatbox
    var userMessage = document.createElement('p');
    userMessage.textContent = message;
    userMessage.className = 'user-message';  // Add class to user message
    chatbox.appendChild(userMessage);
    chatbox.scrollTop = chatbox.scrollHeight; // Auto scroll to bottom

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
        botMessage.className = 'bot-message';  // Add class to bot message
        chatbox.appendChild(botMessage);
        chatbox.scrollTop = chatbox.scrollHeight; // Auto scroll to bottom
    })
    .catch(error => console.error('Error:', error));

    // Clear the input field and refocus for the next message
    messageInput.value = '';
    messageInput.focus();
});
