// 1. Chat Window Open / Close Toggle Function
function toggleChat() {
    const chatContainer = document.getElementById('chat-container');
    
    // Check karein ke container visible hai ya hidden
    if (chatContainer.style.display === 'none' || chatContainer.style.display === '') {
        chatContainer.style.display = 'flex'; // Chat open kar dega
    } else {
        chatContainer.style.display = 'none'; // Chat band kar dega
    }
}

// 2. Render Backend par message bhejne ka function
const API_URL = "https://swiftsign-backend.onrender.com/api/chat"; // Aapka Render backend link

// Double-send guard: jab tak ek request chal rahi hai, doosri nahi jayegi
let isLoading = false;

async function sendMessage() {
    // Agar already ek request chal rahi hai toh ignore karein
    if (isLoading) return;

    const userInput = document.getElementById('userInput');
    const chatBox = document.getElementById('chatBox');
    const text = userInput.value.trim();

    if (!text) return; // Agar input khali hai toh kuch na karein

    // Loading state ON karein aur send button disable karein
    isLoading = true;
    const sendBtn = document.querySelector('button[onclick="sendMessage()"]');
    if (sendBtn) sendBtn.disabled = true;

    // User ka message chat box mein dikhayein
    chatBox.innerHTML += `
        <div style="margin-bottom: 10px; text-align: right;">
            <span style="background: #007bff; color: white; padding: 8px 12px; border-radius: 8px; display: inline-block; max-width: 80%; text-align: left;">
                ${escapeHtml(text)}
            </span>
        </div>
    `;
    
    userInput.value = ''; // Input box clear kar dein
    chatBox.scrollTop = chatBox.scrollHeight;

    // Loading indicator
    const loadingId = 'loading-' + Date.now();
    chatBox.innerHTML += `
        <div id="${loadingId}" class="bot-msg" style="margin-bottom: 10px; background: #e9ecef; padding: 8px 12px; border-radius: 8px;">
            <strong>AI:</strong> Typing...
        </div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        });

        // HTTP error check (4xx, 5xx responses handle karein)
        if (!response.ok) {
            let errorMsg = `Server error (HTTP ${response.status})`;
            try {
                const errData = await response.json();
                errorMsg = errData.detail || errData.message || errorMsg;
            } catch (_) {}
            throw new Error(errorMsg);
        }

        const data = await response.json();
        
        // Loading message hata dein
        document.getElementById(loadingId).remove();

        // Bot ka response nikalen (Backend ke response key ke mutabiq)
        const botReply = data.reply || data.response || data.message || "Response received!";

        // Bot ka message screen par show karein
        chatBox.innerHTML += `
            <div class="bot-msg" style="margin-bottom: 10px; background: #e9ecef; padding: 8px 12px; border-radius: 8px;">
                <strong>AI:</strong> ${escapeHtml(botReply)}
            </div>
        `;

    } catch (error) {
        console.error("Error:", error);
        const loader = document.getElementById(loadingId);
        if (loader) loader.remove();
        chatBox.innerHTML += `
            <div class="bot-msg" style="margin-bottom: 10px; background: #f8d7da; color: #721c24; padding: 8px 12px; border-radius: 8px;">
                <strong>AI:</strong> ${escapeHtml(error.message) || 'Server se connect nahi ho saka.'} (Render server sleep mode par ho sakta hai, 30 sec baad try karein).
            </div>
        `;
    } finally {
        // Request khatam — loading state OFF karein
        isLoading = false;
        if (sendBtn) sendBtn.disabled = false;
        userInput.focus();
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// Enter key press karne par bhi message send ho jaye
document.addEventListener('DOMContentLoaded', () => {
    const userInputField = document.getElementById('userInput');
    if (userInputField) {
        userInputField.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
});

// Security helper function (HTML injection se bachne ke liye)
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}