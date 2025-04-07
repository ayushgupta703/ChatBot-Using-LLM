document.getElementById("send-btn").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") sendMessage();
});

function sendMessage() {
    let inputField = document.getElementById("user-input");
    let userMessage = inputField.value.trim();
    if (userMessage === "") return;

    let chatBox = document.getElementById("chat-box");

    // Append user message with icon
    chatBox.innerHTML += `
        <div class="message-container user-container">
            <img class="user-avatar" src="https://cdn-icons-png.flaticon.com/512/4140/4140048.png" alt="User">
            <div class="user-message">${userMessage}</div>
        </div>
    `;

    inputField.value = "";

    // Send message to Flask backend
    fetch("/chat", {
        method: "POST",
        body: JSON.stringify({ message: userMessage }),
        headers: { "Content-Type": "application/json" }
    })
        .then(response => response.json())
        .then(data => {
            // Append bot response with icon
            chatBox.innerHTML += `
            <div class="message-container">
                <img class="bot-avatar" src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" alt="Bot">
                <div class="bot-message">${data.response}</div>
            </div>
        `;
            chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll
        });
}
