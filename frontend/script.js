/* ==========================================================
   Swift Sign Group — Chat Widget Logic
   ========================================================== */

// ---- Backend endpoint configuration -------------------------
// Auto-detect the correct API URL so the widget works locally and in production.
function resolveApiUrl() {
    // Allow an explicit override via a global on the page.
    if (window.SWIFTSIGN_API_URL) return window.SWIFTSIGN_API_URL;

    const host = window.location.hostname;
    const protocol = window.location.protocol;

    // Local development (file://, localhost) -> local backend.
    if (protocol === 'file:' || host === 'localhost' || host === '127.0.0.1' || host === '') {
        return 'http://127.0.0.1:8000/api/chat';
    }
    // Production (e.g. Vercel) -> same-origin serverless function.
    return '/api/chat';
}
const API_URL = resolveApiUrl();

// ---- State --------------------------------------------------
let isLoading = false;

// ---- Chat window open / close -------------------------------
function toggleChat(forceOpen) {
    const chatContainer = document.getElementById('chat-container');
    const fab = document.getElementById('chatFab');
    if (!chatContainer) return;

    const shouldOpen = typeof forceOpen === 'boolean'
        ? forceOpen
        : chatContainer.classList.contains('chat-hidden');

    chatContainer.classList.toggle('chat-hidden', !shouldOpen);
    if (fab) fab.classList.toggle('is-open', shouldOpen);

    if (shouldOpen) {
        const input = document.getElementById('userInput');
        if (input) setTimeout(() => input.focus(), 120);
        scrollToBottom();
    }
}

// ---- Helpers ------------------------------------------------
function scrollToBottom() {
    const chatBox = document.getElementById('chatBox');
    if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
}

function escapeHtml(text) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return String(text).replace(/[&<>"']/g, (m) => map[m]);
}

// Lightweight formatting: escape first, then render newlines as
// paragraphs and **bold** as <strong>. Safe because we escape HTML first.
function formatMessage(text) {
    const safe = escapeHtml(text);
    const paragraphs = safe.split(/\n+/).filter(Boolean).map((line) => {
        const bolded = line.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        return `<p>${bolded}</p>`;
    });
    return paragraphs.join('') || '<p>…</p>';
}

// Append a message bubble to the conversation.
function addMessage(role, text, isError) {
    const chatBox = document.getElementById('chatBox');
    if (!chatBox) return;

    const wrap = document.createElement('div');
    wrap.className = 'msg ' + (role === 'user' ? 'user-msg' : 'bot-msg') + (isError ? ' msg-error' : '');

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    avatar.innerHTML = role === 'user'
        ? '<i class="fa-solid fa-user"></i>'
        : '<i class="fa-solid fa-robot"></i>';

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    if (role === 'user') {
        bubble.innerHTML = `<p>${escapeHtml(text)}</p>`;
    } else {
        bubble.innerHTML = formatMessage(text);
    }

    wrap.appendChild(avatar);
    wrap.appendChild(bubble);
    chatBox.appendChild(wrap);
    scrollToBottom();
}

// Show an animated "typing…" indicator. Returns its element.
function showTyping() {
    const chatBox = document.getElementById('chatBox');
    if (!chatBox) return null;
    const wrap = document.createElement('div');
    wrap.className = 'msg bot-msg';
    wrap.id = 'typingIndicator';
    wrap.innerHTML = `
        <div class="msg-avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="msg-bubble typing"><span></span><span></span><span></span></div>
    `;
    chatBox.appendChild(wrap);
    scrollToBottom();
    return wrap;
}

function hideTyping() {
    const t = document.getElementById('typingIndicator');
    if (t) t.remove();
}

// ---- Send a message -----------------------------------------
async function sendMessage(event) {
    if (event && event.preventDefault) event.preventDefault();
    if (isLoading) return false;

    const input = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const text = (input ? input.value : '').trim();
    if (!text) return false;

    // Hide quick-reply chips after the first message for a cleaner look.
    const quick = document.getElementById('chatQuick');
    if (quick) quick.style.display = 'none';

    isLoading = true;
    if (sendBtn) sendBtn.disabled = true;

    addMessage('user', text);
    if (input) input.value = '';
    showTyping();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        if (!response.ok) {
            let errorMsg = `Server error (HTTP ${response.status})`;
            try {
                const errData = await response.json();
                errorMsg = errData.detail || errData.message || errorMsg;
            } catch (_) {}
            throw new Error(errorMsg);
        }

        const data = await response.json();
        hideTyping();
        const botReply = data.reply || data.response || data.answer || data.message || "Sorry, I didn't catch that. Could you rephrase?";
        addMessage('bot', botReply);

    } catch (error) {
        console.error('Chat error:', error);
        hideTyping();
        addMessage('bot', '⚠️ ' + (error.message || 'Could not reach the server. Please try again in a moment.'), true);
    } finally {
        isLoading = false;
        if (sendBtn) sendBtn.disabled = false;
        if (input) input.focus();
        scrollToBottom();
    }
    return false;
}

// ---- Quick suggestion chip ----------------------------------
function quickAsk(text) {
    const input = document.getElementById('userInput');
    if (input) input.value = text;
    sendMessage();
}

// ---- Division card -> ask about a topic ---------------------
function askAbout(topic) {
    toggleChat(true);
    const input = document.getElementById('userInput');
    if (input) input.value = `Tell me about ${topic}`;
    // Small delay so the open animation finishes before sending.
    setTimeout(() => sendMessage(), 250);
}

// ---- Clear conversation -------------------------------------
function clearChat() {
    const chatBox = document.getElementById('chatBox');
    if (chatBox) chatBox.innerHTML = '';
    addMessage('bot', '👋 Hi again! How can I help you with Swift Sign Group today?');
    const quick = document.getElementById('chatQuick');
    if (quick) quick.style.display = '';
}

// ---- Init ---------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    // Footer year
    const year = document.getElementById('year');
    if (year) year.textContent = new Date().getFullYear();

    // Enter-to-send (form submit also handles this; kept for safety)
    const input = document.getElementById('userInput');
    if (input) {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage(e);
            }
        });
    }

    // Clear button
    const clearBtn = document.getElementById('chatClear');
    if (clearBtn) clearBtn.addEventListener('click', clearChat);

    // Mobile nav toggle
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
    }

    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) themeToggle.addEventListener('click', toggleTheme);

    // Close chat on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const chat = document.getElementById('chat-container');
            if (chat && !chat.classList.contains('chat-hidden')) toggleChat(false);
        }
    });
});

// ---- Theme (light / dark) -----------------------------------
function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('swiftsign-theme', next); } catch (e) { /* ignore */ }
}

