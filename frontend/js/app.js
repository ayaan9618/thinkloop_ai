// Main application logic

// Load token on page load
document.addEventListener('DOMContentLoaded', () => {
    loadToken();
    init();
});

function init() {
    // Setup event listeners
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    document.getElementById('question-form').addEventListener('submit', handleQuestion);

    // Show login or tutor page
    if (authToken) {
        showTutorPage();
    } else {
        showLoginPage();
    }
}

// ============ AUTH HANDLERS ============

async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const errorEl = document.getElementById('login-error');
    
    try {
        errorEl.classList.add('hidden');
        const response = await auth.login(email, password);
        saveToken(response.access_token);
        
        // Show tutor page
        showTutorPage();
    } catch (error) {
        errorEl.textContent = error.message;
        errorEl.classList.remove('hidden');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const email = document.getElementById('register-email').value;
    const username = document.getElementById('register-username').value;
    const firstName = document.getElementById('register-first').value;
    const lastName = document.getElementById('register-last').value;
    const password = document.getElementById('register-password').value;
    const errorEl = document.getElementById('register-error');
    
    try {
        errorEl.classList.add('hidden');
        await auth.register(email, username, password, firstName, lastName);
        
        // Auto login
        const response = await auth.login(email, password);
        saveToken(response.access_token);
        
        showTutorPage();
    } catch (error) {
        errorEl.textContent = error.message;
        errorEl.classList.remove('hidden');
    }
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        clearToken();
        showLoginPage();
        document.getElementById('login-form').reset();
    }
}

// ============ UI HANDLERS ============

function showLoginPage() {
    document.getElementById('login-page').classList.remove('hidden');
    document.getElementById('register-page').classList.add('hidden');
    document.getElementById('tutor-page').classList.add('hidden');
    document.getElementById('nav-user').classList.add('hidden');
}

function showRegister() {
    document.getElementById('login-page').classList.add('hidden');
    document.getElementById('register-page').classList.remove('hidden');
}

function showLogin() {
    document.getElementById('login-page').classList.remove('hidden');
    document.getElementById('register-page').classList.add('hidden');
}

async function showTutorPage() {
    try {
        const user = await auth.getMe();
        document.getElementById('username').textContent = user.username;
        document.getElementById('nav-user').classList.remove('hidden');
        
        document.getElementById('login-page').classList.add('hidden');
        document.getElementById('register-page').classList.add('hidden');
        document.getElementById('tutor-page').classList.remove('hidden');
    } catch (error) {
        clearToken();
        showLoginPage();
    }
}

// ============ TUTOR HANDLERS ============

let conversationId = null;

async function handleQuestion(e) {
    e.preventDefault();
    
    const question = document.getElementById('question-input').value;
    
    try {
        const response = await tutor.ask(question);
        conversationId = response.conversation_id;
        
        // Clear input
        document.getElementById('question-input').value = '';
        
        // Add messages to chat
        addMessage('user', question);
        addMessage('tutor', response.response);
        
        // Enable/disable hint button
        document.getElementById('hint-btn').disabled = !response.can_request_hint;
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function requestHint() {
    if (!conversationId) return;
    
    try {
        const response = await tutor.hint(conversationId);
        addMessage('tutor', response.hint);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function addMessage(sender, text) {
    const chatArea = document.querySelector('#chat-area .space-y-4');
    const div = document.createElement('div');
    div.className = sender === 'user' ? 'text-right' : 'text-left';
    
    const msgClass = sender === 'user' 
        ? 'bg-blue-500 text-white' 
        : 'bg-gray-200 text-gray-900';
    
    div.innerHTML = `
        <div class="inline-block max-w-xs ${msgClass} px-4 py-2 rounded-lg">
            <p class="text-sm">${escapeHtml(text)}</p>
        </div>
    `;
    
    chatArea.appendChild(div);
    document.getElementById('chat-area').scrollTop = document.getElementById('chat-area').scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
