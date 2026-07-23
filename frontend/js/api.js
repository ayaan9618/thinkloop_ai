// API client module
const API_URL = '/api/v1';

let authToken = null;

// Load token from localStorage on page load
function loadToken() {
    authToken = localStorage.getItem('access_token');
}

// Save token to localStorage
function saveToken(token) {
    authToken = token;
    localStorage.setItem('access_token', token);
}

// Clear token
function clearToken() {
    authToken = null;
    localStorage.removeItem('access_token');
}

// Make API request
async function apiRequest(method, endpoint, body = null) {
    const url = `${API_URL}${endpoint}`;
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (authToken) {
        options.headers['Authorization'] = `Bearer ${authToken}`;
    }

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || error.message || 'API Error');
    }

    return await response.json();
}

// Auth API calls
const auth = {
    login: (email, password) => 
        apiRequest('POST', '/auth/login', { email, password }),
    
    register: (email, username, password, firstName, lastName) => 
        apiRequest('POST', '/auth/register', {
            email,
            username,
            password,
            first_name: firstName,
            last_name: lastName
        }),
    
    getMe: () => 
        apiRequest('GET', '/auth/me'),
    
    logout: () => {
        clearToken();
        return Promise.resolve();
    }
};

// Tutor API calls
const tutor = {
    ask: (question) => 
        apiRequest('POST', '/tutor/ask', { question }),
    
    hint: (conversationId) => 
        apiRequest('POST', `/tutor/hint/${conversationId}`, {}),
    
    reveal: (conversationId) => 
        apiRequest('POST', `/tutor/reveal/${conversationId}`, {})
};
