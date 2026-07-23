const SAMPLE_PROMPTS = [
    "Explain Docker like I am a beginner",
    "What is recursion and when do I use it?",
    "Help me understand Git branches and merges",
    "How do APIs and frontend talk to each other?",
];

const chatState = {
    conversationId: null,
    messages: [],
    typingElement: null,
};

document.addEventListener("DOMContentLoaded", () => {
    loadToken();
    init();
});

function init() {
    document.getElementById("login-form").addEventListener("submit", handleLogin);
    document.getElementById("register-form").addEventListener("submit", handleRegister);
    document.getElementById("question-form").addEventListener("submit", handleQuestion);
    document.getElementById("question-input").addEventListener("keydown", handleComposerKeydown);

    document.querySelectorAll(".quick-prompt").forEach((button) => {
        button.addEventListener("click", () => fillPrompt(button.dataset.prompt || ""));
    });

    renderSidebarPrompts();

    if (authToken) {
        showTutorPage();
    } else {
        showLoginPage();
    }
}

function renderSidebarPrompts() {
    const sidebar = document.getElementById("sidebar-prompts");
    if (!sidebar) return;

    sidebar.innerHTML = SAMPLE_PROMPTS.map(
        (prompt) => `
            <button class="quick-prompt w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-left text-sm text-slate-200 transition hover:bg-white/10"
                data-prompt="${escapeHtml(prompt)}">
                ${escapeHtml(prompt)}
            </button>
        `
    ).join("");

    sidebar.querySelectorAll(".quick-prompt").forEach((button) => {
        button.addEventListener("click", () => fillPrompt(button.dataset.prompt || ""));
    });
}

async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;
    const errorElement = document.getElementById("login-error");

    try {
        errorElement.classList.add("hidden");
        const response = await auth.login(email, password);
        saveToken(response.access_token);
        await showTutorPage();
    } catch (error) {
        errorElement.textContent = error.message;
        errorElement.classList.remove("hidden");
    }
}

async function handleRegister(event) {
    event.preventDefault();

    const email = document.getElementById("register-email").value.trim();
    const username = document.getElementById("register-username").value.trim();
    const firstName = document.getElementById("register-first").value.trim();
    const lastName = document.getElementById("register-last").value.trim();
    const password = document.getElementById("register-password").value;
    const errorElement = document.getElementById("register-error");

    try {
        errorElement.classList.add("hidden");
        await auth.register(email, username, password, firstName, lastName);
        const response = await auth.login(email, password);
        saveToken(response.access_token);
        await showTutorPage();
    } catch (error) {
        errorElement.textContent = error.message;
        errorElement.classList.remove("hidden");
    }
}

function logout() {
    if (!confirm("Log out of thinkloop AI?")) {
        return;
    }

    clearToken();
    resetChat();
    document.getElementById("login-form").reset();
    showLoginPage();
}

function showLoginPage() {
    document.getElementById("auth-shell").classList.remove("hidden");
    document.getElementById("register-shell").classList.add("hidden");
    document.getElementById("tutor-page").classList.add("hidden");
}

function showRegister() {
    document.getElementById("auth-shell").classList.add("hidden");
    document.getElementById("register-shell").classList.remove("hidden");
    document.getElementById("tutor-page").classList.add("hidden");
}

function showLogin() {
    document.getElementById("auth-shell").classList.remove("hidden");
    document.getElementById("register-shell").classList.add("hidden");
    document.getElementById("tutor-page").classList.add("hidden");
}

async function showTutorPage() {
    try {
        const user = await auth.getMe();
        document.getElementById("username").textContent = user.username;
        document.getElementById("nav-user").textContent = `@${user.username}`;

        document.getElementById("auth-shell").classList.add("hidden");
        document.getElementById("register-shell").classList.add("hidden");
        document.getElementById("tutor-page").classList.remove("hidden");

        showWelcomeState();
        setStatus("Ready");
    } catch (error) {
        clearToken();
        showLoginPage();
    }
}

function handleComposerKeydown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        document.getElementById("question-form").requestSubmit();
    }
}

async function handleQuestion(event) {
    event.preventDefault();

    const input = document.getElementById("question-input");
    const question = input.value.trim();
    if (!question) return;

    input.value = "";
    addMessage("user", question);
    setStatus("Thinking...");
    setTyping(true);

    try {
        const response = await tutor.ask(question);
        chatState.conversationId = response.conversation_id;
        addMessage("assistant", response.response, {
            badge: response.can_request_hint ? "Socratic" : "Tutor",
        });
        updateHintButton(response.can_request_hint);
        setStatus("Ready");
    } catch (error) {
        addMessage("system", error.message || "Something went wrong.");
        setStatus("Error");
    } finally {
        setTyping(false);
        revealChat();
    }
}

async function requestHint() {
    if (!chatState.conversationId) {
        setStatus("Ask a question first");
        return;
    }

    setTyping(true);
    setStatus("Generating hint...");

    try {
        const response = await tutor.hint(chatState.conversationId);
        addMessage("assistant", response.hint, { badge: `Hint ${response.hint_level}` });
        updateHintButton(response.can_request_more_hints);
        setStatus("Ready");
    } catch (error) {
        addMessage("system", error.message || "Could not fetch a hint.");
        setStatus("Error");
    } finally {
        setTyping(false);
        revealChat();
    }
}

function newChat() {
    resetChat();
    document.getElementById("question-input").value = "";
    document.getElementById("question-input").focus();
}

function resetChat() {
    chatState.conversationId = null;
    chatState.messages = [];
    updateHintButton(false);

    const messages = document.getElementById("chat-messages");
    if (messages) {
        messages.innerHTML = "";
    }

    showWelcomeState();
}

function fillPrompt(prompt) {
    const input = document.getElementById("question-input");
    input.value = prompt;
    input.focus();
}

function showWelcomeState() {
    document.getElementById("chat-empty").classList.remove("hidden");
    document.getElementById("chat-area").classList.add("hidden");
}

function revealChat() {
    document.getElementById("chat-empty").classList.add("hidden");
    document.getElementById("chat-area").classList.remove("hidden");
}

function updateHintButton(enabled) {
    const button = document.getElementById("hint-btn");
    button.disabled = !enabled;
}

function setStatus(text) {
    document.getElementById("status-pill").textContent = text;
}

function setTyping(isTyping) {
    if (isTyping) {
        if (chatState.typingElement) return;

        revealChat();
        const messages = document.getElementById("chat-messages");
        chatState.typingElement = document.createElement("div");
        chatState.typingElement.className = "flex w-full justify-start";
        chatState.typingElement.innerHTML = `
            <div class="flex w-full max-w-[46rem] items-start gap-3">
                <div class="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-slate-700 text-[11px] font-semibold text-slate-100">
                    AI
                </div>
                <div class="min-w-0 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300">
                    <div class="flex items-center gap-2">
                    <span class="h-2.5 w-2.5 animate-pulse rounded-full bg-sky-400"></span>
                    <span class="h-2.5 w-2.5 animate-pulse rounded-full bg-sky-300" style="animation-delay: 120ms"></span>
                    <span class="h-2.5 w-2.5 animate-pulse rounded-full bg-sky-200" style="animation-delay: 240ms"></span>
                    </div>
                </div>
            </div>
        `;
        messages.appendChild(chatState.typingElement);
        scrollChatToBottom();
        return;
    }

    if (chatState.typingElement) {
        chatState.typingElement.remove();
        chatState.typingElement = null;
    }
}

function addMessage(role, text, options = {}) {
    const messages = document.getElementById("chat-messages");
    if (!messages) return;

    const wrapper = document.createElement("div");
    const isUser = role === "user";
    const isSystem = role === "system";

    wrapper.className = `flex w-full ${isUser ? "justify-end" : "justify-start"}`;

    const bubbleClasses = isUser
        ? "bg-gradient-to-br from-cyan-500 via-sky-500 to-indigo-500 text-white shadow-lg shadow-cyan-500/15"
        : isSystem
            ? "border border-amber-500/20 bg-amber-500/10 text-amber-100"
            : "border border-white/10 bg-white/5 text-slate-100";

    if (isUser) {
        wrapper.innerHTML = `
            <div class="max-w-[22rem] rounded-3xl px-4 py-3 ${bubbleClasses}">
                <div class="message-content whitespace-pre-wrap text-[15px] leading-6 text-white">
                    ${formatMessage(text)}
                </div>
            </div>
        `;
    } else {
        const avatar = `<div class="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${isSystem ? "bg-amber-500/15 text-amber-200" : "bg-slate-700 text-slate-100"} text-[11px] font-semibold">${isSystem ? "!" : "AI"}</div>`;
        wrapper.innerHTML = `
            <div class="flex w-full max-w-[46rem] items-start gap-3">
                ${avatar}
                <div class="min-w-0 flex-1 pt-1">
                    <div class="mb-1 text-[11px] uppercase tracking-[0.22em] text-slate-500">
                        ${options.badge || (isSystem ? "Notice" : "Socratic")}
                    </div>
                    <div class="message-content whitespace-pre-wrap text-[15px] leading-7 ${isSystem ? "text-amber-100" : "text-slate-100"}">
                        ${formatMessage(text)}
                    </div>
                </div>
            </div>
        `;
    }

    messages.appendChild(wrapper);
    chatState.messages.push({ role, text, options });
    scrollChatToBottom();
}

function formatMessage(text) {
    const escaped = escapeHtml(text);
    const withLinks = escaped.replace(
        /(https?:\/\/[^\s<]+)/g,
        '<a href="$1" target="_blank" rel="noreferrer" class="text-sky-300 underline decoration-sky-400/40 underline-offset-4">$1</a>'
    );

    return withLinks
        .replace(/\n\n/g, "</p><p>")
        .replace(/\n/g, "<br>")
        .replace(/^/, "<p>")
        .replace(/$/, "</p>");
}

function scrollChatToBottom() {
    const chatArea = document.getElementById("chat-area");
    if (chatArea) {
        chatArea.scrollTop = chatArea.scrollHeight;
    }
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
