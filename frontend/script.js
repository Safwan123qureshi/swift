const CLIENT_ID = "c53d339f-4f5d-4064-a827-8fb537536100";

// Determine API endpoint dynamically based on current environment
function getApiEndpoints() {
    const isHttp = window.location.protocol.startsWith("http");
    const isLocal = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || window.location.hostname === "";
    
    if (isHttp && !isLocal) {
        // Production hosting (e.g., Vercel / Cloud)
        return {
            primary: "/api/chat",
            fallback: "/chat"
        };
    }
    
    // Local development (Live Server, file://, localhost)
    
return {
    primary: "https://impound-gumdrop-elm.ngrok-free.dev/api/chat",
    fallback: "https://impound-gumdrop-elm.ngrok-free.dev/api/chat"
};
    };


// Session ID generator & storage
function getSessionId() {
    let sessionId = sessionStorage.getItem("swift_chat_session_id");
    if (!sessionId) {
        sessionId = "session-" + Date.now() + "-" + Math.random().toString(36).substring(2, 9);
        sessionStorage.setItem("swift_chat_session_id", sessionId);
    }
    return sessionId;
}

// Helper to escape HTML characters
function escapeHtml(text) {
    if (typeof text !== "string") return "";
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Chat window open/close toggle
function toggleChat() {
    const chatContainer = document.getElementById("chat-container");
    if (!chatContainer) return;
    
    if (chatContainer.style.display === "none" || chatContainer.classList.contains("chat-hidden")) {
        chatContainer.style.display = "flex";
        chatContainer.classList.remove("chat-hidden");
        const inputField = document.getElementById("userInput");
        if (inputField) inputField.focus();
    } else {
        chatContainer.style.display = "none";
        chatContainer.classList.add("chat-hidden");
    }
}

// Flag to prevent double sending
let isSending = false;

// Main message send function
async function sendMessage() {
    if (isSending) return;

    const inputField = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");
    
    if (!inputField || !chatBox) return;
    
    const questionText = inputField.value.trim();
    if (!questionText) return;

    // 1. Display user query in chat
    chatBox.innerHTML += `
        <div style="margin: 8px 0; text-align: right;">
            <span style="background: #007bff; color: white; padding: 8px 12px; border-radius: 8px; display: inline-block; max-width: 80%;">
                <strong>You:</strong> ${escapeHtml(questionText)}
            </span>
        </div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
    
    // Clear input
    inputField.value = "";
    isSending = true;

    // 2. Display typing/loading placeholder
    const loadingElemId = "loading-msg-" + Date.now();
    chatBox.innerHTML += `
        <div id="${loadingElemId}" style="margin: 8px 0; background: #e9ecef; color: #555; padding: 8px 12px; border-radius: 8px; display: inline-block; max-width: 85%;">
            <i class="fa-solid fa-spinner fa-spin"></i> Swift Sign AI is typing...
        </div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    // 3. Payload supporting both main.py and app.py
    const payload = {
        client_id: CLIENT_ID,
        question: questionText,
        message: questionText,
        brand: "Swift Sign Group",
        session_id: getSessionId()
    };

    const endpoints = getApiEndpoints();
    let response = null;
    let errorDetail = null;

    try {
        // Attempt primary endpoint (127.0.0.1:8000/api/chat)
        try {
            response = await fetch(endpoints.primary, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json" 
                },
                body: JSON.stringify(payload)
            });
        } catch (primErr) {
            console.warn(`[Swift Sign Chatbot] Primary endpoint ${endpoints.primary} failed. Trying fallback...`, primErr);
            if (endpoints.fallback && endpoints.fallback !== endpoints.primary) {
                response = await fetch(endpoints.fallback, {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json" 
                    },
                    body: JSON.stringify(payload)
                });
            } else {
                throw primErr;
            }
        }

        // Remove loading placeholder
        const loader = document.getElementById(loadingElemId);
        if (loader) loader.remove();

        if (!response.ok) {
            let serverError = `Server error (HTTP ${response.status})`;
            try {
                const errData = await response.json();
                serverError = errData.detail || errData.message || serverError;
            } catch (_) {}
            throw new Error(serverError);
        }

        const data = await response.json();
        
        // Extract reply text
        const botReply = data.response || data.answer || data.message || "Thank you for reaching out to Swift Sign Group.";

        // Display bot response
        chatBox.innerHTML += `
            <div style="margin: 8px 0; background: #e9ecef; color: #222; padding: 8px 12px; border-radius: 8px; display: inline-block; max-width: 85%; white-space: pre-wrap; word-break: break-word; line-height: 1.4;">
                <strong>AI:</strong> ${escapeHtml(botReply)}
            </div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {
        console.error("[Swift Sign Chatbot] Connection Error:", error);

        // Remove loading placeholder if still present
        const loader = document.getElementById(loadingElemId);
        if (loader) loader.remove();

        chatBox.innerHTML += `
            <div style="margin: 8px 0; color: #721c24; background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px 12px; border-radius: 8px; font-size: 13px;">
                <strong>Error:</strong> Could not connect to server.<br>
                <span style="font-size: 12px; color: #555;">Please verify the backend server is running at <code>http://127.0.0.1:8000</code>.</span>
            </div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    } finally {
        isSending = false;
        inputField.focus();
    }
}

// Background connection test on load to verify connectivity
async function checkBackendConnectivity() {
    const urls = ["http://127.0.0.1:8000/status", "http://127.0.0.1:8000/api/status"];
    for (const url of urls) {
        try {
            const res = await fetch(url);
            if (res.ok) {
                console.log(`✅ [Swift Sign Chatbot] Backend is active and reachable at ${url}`);
                return;
            }
        } catch (_) {}
    }
    console.warn("⚠️ [Swift Sign Chatbot] Backend server not detected at http://127.0.0.1:8000. Start it by running 'start.bat' or 'python run.py'.");
}

// Attach event listeners
document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("userInput");
    if (inputField) {
        inputField.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                sendMessage();
            }
        });
    }

    // Ping backend to verify status in console
    checkBackendConnectivity();
});