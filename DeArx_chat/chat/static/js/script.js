document.getElementById('messageForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var message = document.getElementById('messageInput').value;
    // Send message to backend and get response
    // TODO: Add AJAX request to backend here

    // Clear the input field and refocus for the next message
    document.getElementById('messageInput').value = '';
    document.getElementById('messageInput').focus();
});
