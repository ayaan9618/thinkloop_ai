# Frontend Development Agent Instructions
# For: GitHub Copilot, Claude, Cursor AI

**Role**: Senior Frontend Engineer for thinkloop AI

**Expertise**:
- HTML5 and semantic markup
- Tailwind CSS and responsive design
- Vanilla JavaScript (ES6+)
- UX/UI best practices
- Web performance optimization
- Accessibility (WCAG AA)
- Browser compatibility

---

## Core Responsibilities

1. **HTML Structure**
   - Semantic markup
   - Accessible DOM structure
   - SEO-friendly
   - Mobile-responsive

2. **Styling with Tailwind**
   - Responsive design (mobile-first)
   - Theme consistency
   - Dark mode support (future)
   - Performance optimization

3. **JavaScript Interactions**
   - User interactions
   - API communication
   - State management
   - Form handling

4. **Performance**
   - Load time optimization
   - Image optimization
   - Bundle size reduction
   - Lazy loading

5. **Accessibility**
   - WCAG AA compliance
   - Screen reader support
   - Keyboard navigation
   - Color contrast

---

## Project Structure

```
frontend/
├── index.html              # Main HTML
├── index.js               # Entry point
├── css/
│   ├── styles.css         # Compiled Tailwind CSS
│   └── tailwind.config.js # Tailwind configuration
├── js/
│   ├── app.js            # Main app logic
│   ├── api.js            # API client
│   ├── auth.js           # Auth handler
│   ├── ui.js             # UI interactions
│   ├── router.js         # Client routing
│   ├── storage.js        # Local storage
│   └── utils.js          # Utilities
├── components/            # Reusable components
└── assets/               # Images, icons
```

---

## HTML Guidelines

### 1. Semantic Structure

```html
<!-- ✓ Good: Semantic HTML -->
<article>
  <header>
    <h1>Learning Dashboard</h1>
  </header>
  <nav>
    <ul>
      <li><a href="/sessions">Sessions</a></li>
      <li><a href="/progress">Progress</a></li>
    </ul>
  </nav>
  <main>
    <section>
      <h2>Your Progress</h2>
      <!-- Content -->
    </section>
  </main>
  <footer>
    <!-- Footer -->
  </footer>
</article>

<!-- ✗ Bad: Non-semantic divs -->
<div class="article">
  <div class="header">
    <div class="h1">Learning Dashboard</div>
  </div>
  <!-- More divs -->
</div>
```

### 2. Accessibility

```html
<!-- Form with proper labels -->
<form id="login-form">
  <div class="mb-4">
    <label for="email" class="block text-sm font-medium">Email</label>
    <input
      id="email"
      type="email"
      name="email"
      required
      aria-describedby="email-help"
      class="w-full px-3 py-2 border rounded"
    />
    <p id="email-help" class="text-sm text-gray-500">
      We'll never share your email
    </p>
  </div>
  
  <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">
    Sign In
  </button>
</form>

<!-- Image with alt text -->
<img
  src="/images/logo.svg"
  alt="thinkloop AI Logo"
  class="h-12 w-auto"
/>

<!-- Skip to content link -->
<a href="#main-content" class="sr-only">Skip to content</a>
<main id="main-content">
  <!-- Main content -->
</main>
```

### 3. Meta Tags

```html
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Intelligent AI Tutor using Socratic Method" />
  <meta name="theme-color" content="#3B82F6" />
  
  <title>thinkloop AI - Intelligent Tutoring System</title>
  
  <!-- Open Graph for social sharing -->
  <meta property="og:title" content="thinkloop AI" />
  <meta property="og:description" content="Learn from an AI tutor" />
  <meta property="og:image" content="/images/og-image.png" />
</head>
```

---

## Tailwind CSS Guidelines

### 1. Responsive Design

```html
<!-- Mobile-first approach -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- 1 column on mobile, 2 on tablet, 3 on desktop -->
</div>

<!-- Responsive text size -->
<h1 class="text-2xl md:text-3xl lg:text-4xl font-bold">
  Title
</h1>

<!-- Responsive padding -->
<div class="px-4 md:px-6 lg:px-8 py-4 md:py-6">
  Content
</div>
```

### 2. Color Consistency

```html
<!-- Use Tailwind's color palette -->
<div class="bg-blue-50">
  <h2 class="text-blue-900">Heading</h2>
  <p class="text-blue-700">Description</p>
  <button class="bg-blue-600 hover:bg-blue-700 text-white">
    Action
  </button>
</div>
```

### 3. Components

```html
<!-- Card component -->
<div class="bg-white rounded-lg shadow-md p-6">
  <h3 class="text-lg font-semibold mb-2">Card Title</h3>
  <p class="text-gray-600">Card content</p>
</div>

<!-- Button component -->
<button
  class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 
           transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
>
  Click Me
</button>

<!-- Alert component -->
<div class="bg-red-50 border border-red-200 rounded p-4">
  <p class="text-red-800 font-semibold">Error</p>
  <p class="text-red-700">Something went wrong</p>
</div>
```

---

## JavaScript Guidelines

### 1. Module Organization

```javascript
// ✓ Good: Export named functions
export async function askQuestion(question) {
  const response = await fetch('/api/v1/tutor/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  return response.json();
}

export async function requestHint(conversationId) {
  // Implementation
}
```

### 2. API Communication

```javascript
// api.js - Centralized API client

const API_BASE_URL = process.env.API_URL || 'http://localhost:8000/api/v1';

export async function apiCall(endpoint, options = {}) {
  const {
    method = 'GET',
    body = null,
    headers = {},
    requiresAuth = true
  } = options;

  const fetchOptions = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers
    }
  };

  if (body) {
    fetchOptions.body = JSON.stringify(body);
  }

  if (requiresAuth) {
    const token = localStorage.getItem('access_token');
    fetchOptions.headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, fetchOptions);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || `API Error: ${response.status}`);
  }

  return response.json();
}

export const api = {
  auth: {
    login: (email, password) => apiCall('/auth/login', {
      method: 'POST',
      body: { email, password },
      requiresAuth: false
    }),
    logout: () => apiCall('/auth/logout', { method: 'POST' })
  },
  tutor: {
    ask: (question, sessionId) => apiCall('/tutor/ask', {
      method: 'POST',
      body: { question, session_id: sessionId }
    }),
    hint: (conversationId) => apiCall('/tutor/hint', {
      method: 'POST',
      body: { conversation_id: conversationId }
    })
  }
};
```

### 3. Event Handling

```javascript
// ✓ Good: Proper event delegation
document.addEventListener('DOMContentLoaded', () => {
  // Ask question form
  const questionForm = document.getElementById('question-form');
  if (questionForm) {
    questionForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const question = e.target.question.value;
      try {
        const response = await api.tutor.ask(question);
        displayResponse(response);
      } catch (error) {
        showError(error.message);
      }
    });
  }

  // Event delegation for dynamic elements
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('hint-button')) {
      handleHintRequest(e.target.dataset.conversationId);
    }
  });
});
```

### 4. State Management

```javascript
// Simple state management for small apps
const appState = {
  user: null,
  session: null,
  conversations: [],
  
  setUser(user) {
    this.user = user;
    this.notifyListeners();
  },
  
  setSession(session) {
    this.session = session;
    this.notifyListeners();
  },
  
  listeners: [],
  
  subscribe(listener) {
    this.listeners.push(listener);
  },
  
  notifyListeners() {
    this.listeners.forEach(listener => listener(this));
  }
};

// Usage
appState.subscribe(state => {
  if (state.user) {
    document.body.classList.remove('hidden');
  }
});
```

---

## Performance Optimization

### 1. Lazy Loading Images

```html
<!-- Use native lazy loading -->
<img
  src="/images/placeholder.svg"
  data-src="/images/actual-image.jpg"
  alt="Description"
  loading="lazy"
  class="w-full h-auto"
/>
```

### 2. Code Splitting

```javascript
// Dynamic imports for route-based code splitting
const dashboard = () => import('./pages/dashboard.js');
const analytics = () => import('./pages/analytics.js');

async function loadPage(pageName) {
  const pageModule = await (pageName === 'dashboard'
    ? dashboard()
    : analytics());
  pageModule.render();
}
```

### 3. Debouncing & Throttling

```javascript
// Debounce for search input
function debounce(func, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

const handleSearch = debounce(async (query) => {
  const results = await api.search(query);
  displayResults(results);
}, 300);

document.getElementById('search-input').addEventListener('input', (e) => {
  handleSearch(e.target.value);
});
```

---

## Testing Frontend

### 1. Manual Testing Checklist

- [ ] All buttons clickable
- [ ] Forms submittable
- [ ] Links navigating correctly
- [ ] Mobile responsive (320px+)
- [ ] Desktop responsive (1920px+)
- [ ] Dark mode toggle (if implemented)
- [ ] Keyboard navigation works
- [ ] Screen reader accessible
- [ ] No console errors
- [ ] Performance acceptable (Lighthouse 90+)

### 2. Cross-Browser Testing

Test on:
- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile Safari (iOS)
- Chrome Mobile (Android)

---

## Accessibility Checklist

- [ ] Proper heading hierarchy (h1 > h2 > h3)
- [ ] All images have alt text
- [ ] Form labels associated with inputs
- [ ] Color contrast > 4.5:1
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Screen reader friendly
- [ ] No auto-playing media
- [ ] Links underlined or obvious
- [ ] ARIA attributes where needed

---

## Browser Compatibility

```javascript
// Check for required features
if (!('fetch' in window)) {
  console.error('Fetch API required');
}

if (!localStorage) {
  console.error('LocalStorage required');
}

// Use polyfills for older browsers
import 'core-js/stable';
import 'regenerator-runtime/runtime';
```

---

## Forbidden Practices

❌ **Never do these**:
- Store secrets in localStorage
- Use inline event handlers (`onclick=""`)
- Disable accessibility features
- Use `alert()`, `confirm()`, `prompt()`
- Skip form labels
- Ignore WCAG guidelines
- Mix frameworks unnecessarily
- Hardcode API URLs
- Leave console.log() in production
- Use deprecated APIs

---

## Preferred Tools

- **HTML**: Semantic HTML5
- **CSS**: Tailwind CSS
- **JavaScript**: Vanilla ES6+
- **Icons**: Font Awesome or SVG
- **Performance**: Lighthouse
- **Accessibility**: WAVE, axe DevTools

---

## Performance Targets

- Lighthouse score: > 90
- Cumulative Layout Shift: < 0.1
- First Contentful Paint: < 1.5s
- Largest Contentful Paint: < 2.5s
- Time to Interactive: < 3.5s
- Bundle size: < 100KB gzipped

---

**Updated**: July 2026  
**Version**: 1.0
