/* ============================================================
   AgenteJP Inventario — Scripts
   ============================================================ */

marked.setOptions({
    breaks: true,
    gfm: true,
    sanitize: false
});

let history = [];
let isTyping = false;
let welcomeHidden = false;
const SESSION_ID = crypto.randomUUID(); // ID único por pestaña/sesión

// ── DOM refs ──────────────────────────────────────────────────
const messagesEl = document.getElementById('messages');
const welcomeEl = document.getElementById('welcome');
const userInputEl = document.getElementById('userInput');
const sendBtnEl = document.getElementById('sendBtn');

// ── Core ──────────────────────────────────────────────────────
function hideWelcome() {
    if (!welcomeHidden && welcomeEl) {
        welcomeEl.style.display = 'none';
        welcomeHidden = true;
    }
}

function addMessage(role, content) {
    hideWelcome();

    const div = document.createElement('div');
    div.className = `message ${role}`;

    const avatarEl = document.createElement('div');
    avatarEl.className = 'msg-avatar';
    avatarEl.textContent = role === 'user' ? 'Tú' : 'MS';

    const bodyEl = document.createElement('div');
    bodyEl.className = 'msg-body';

    const roleEl = document.createElement('div');
    roleEl.className = 'msg-role';
    roleEl.textContent = role === 'user' ? 'Tú' : 'Inventario';

    const textEl = document.createElement('div');
    textEl.className = 'msg-text';

    if (role === 'agent') {
        textEl.innerHTML = marked.parse(content);
    } else {
        textEl.textContent = content;
    }

    bodyEl.appendChild(roleEl);
    bodyEl.appendChild(textEl);
    div.appendChild(avatarEl);
    div.appendChild(bodyEl);
    messagesEl.appendChild(div);
    scrollToBottom();
    return div;
}

function showTyping() {
    hideWelcome();
    const div = document.createElement('div');
    div.className = 'message agent';
    div.id = 'typing-indicator';

    const avatarEl = document.createElement('div');
    avatarEl.className = 'msg-avatar';
    avatarEl.textContent = 'MS';

    const bodyEl = document.createElement('div');
    bodyEl.className = 'msg-body';

    const roleEl = document.createElement('div');
    roleEl.className = 'msg-role';
    roleEl.textContent = 'Inventario';

    const typingEl = document.createElement('div');
    typingEl.className = 'typing';
    typingEl.innerHTML = '<span></span><span></span><span></span>';

    bodyEl.appendChild(roleEl);
    bodyEl.appendChild(typingEl);
    div.appendChild(avatarEl);
    div.appendChild(bodyEl);
    messagesEl.appendChild(div);
    scrollToBottom();
}

function removeTyping() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}

function scrollToBottom() {
    const wrap = document.getElementById('chatWrap');
    if (wrap) wrap.scrollTop = wrap.scrollHeight;
}

// ── Send ──────────────────────────────────────────────────────
async function sendMessage() {
    const msg = userInputEl.value.trim();
    if (!msg || isTyping) return;

    isTyping = true;
    sendBtnEl.disabled = true;
    userInputEl.value = '';
    userInputEl.style.height = 'auto';

    addMessage('user', msg);
    history.push({ role: 'user', content: msg });

    showTyping();

    try {
        const resp = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg, history: history.slice(-10), session_id: SESSION_ID })
        });
        const data = await resp.json();
        removeTyping();

        const reply = data.respuesta || data.error || 'Sin respuesta del servidor.';
        addMessage('agent', reply);
        history.push({ role: 'assistant', content: reply });

    } catch (err) {
        removeTyping();
        addMessage('agent', `⚠️ Error de conexión: ${err.message}`);
    } finally {
        isTyping = false;
        sendBtnEl.disabled = false;
        userInputEl.focus();
    }
}

function quickQuery(text) {
    userInputEl.value = text;
    sendMessage();
}

function resetChat() {
    history = [];
    messagesEl.innerHTML = '';
    if (welcomeEl) {
        welcomeEl.style.display = '';
        welcomeHidden = false;
    }
    userInputEl.value = '';
    userInputEl.style.height = 'auto';
    userInputEl.focus();
}

// ── Input helpers ─────────────────────────────────────────────
function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
}

// ── Init ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    userInputEl.focus();
});