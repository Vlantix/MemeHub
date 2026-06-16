// ================================================
// LOGIN
// Handles login form submission and view switching
// between login, register, and forgot password
// ================================================

import { post, setAccessToken, setUser } from '../../api/client.js';
import { redirectIfLoggedIn } from '../../utils/auth_guard.js';

// ── DOM ───────────────────────────────────────
const viewLogin = document.getElementById('view-login');
const viewRegister = document.getElementById('view-register');
const viewForgot = document.getElementById('view-forgot');

const usernameOrEmailInput = document.getElementById('login-credential');
const passwordInput = document.getElementById('login-password');
const loginBtn = document.getElementById('btn-login');
const loginError = document.getElementById('login-error');

// ── View switching ────────────────────────────
export function showView(viewId) {
    document.querySelectorAll('.auth-view').forEach(v => v.style.display = 'none');
    document.getElementById(viewId).style.display = 'block';
}

// ── Init ──────────────────────────────────────
redirectIfLoggedIn();

// Read ?mode=login or ?mode=register from URL
const params = new URLSearchParams(window.location.search);
const mode = params.get('mode');
if (mode === 'register') {
    showView('view-register');
} else {
    showView('view-login');
}

// ── Navigation links ──────────────────────────
document.getElementById('goto-login').addEventListener('click', (e) => {
    e.preventDefault();
    showView('view-login');
});

document.getElementById('goto-register').addEventListener('click', (e) => {
    e.preventDefault();
    showView('view-register');
});

document.getElementById('goto-forgot').addEventListener('click', (e) => {
    e.preventDefault();
    showView('view-forgot');
});

document.getElementById('forgot-goto-login').addEventListener('click', (e) => {
    e.preventDefault();
    showView('view-login');
});

// ── Login submit ──────────────────────────────
loginBtn.addEventListener('click', async () => {
    const usernameOrEmail = usernameOrEmailInput.value.trim();
    const password = passwordInput.value;

    loginError.style.display = 'none';

    if (!usernameOrEmail && !password) {
        showError(loginError, 'Username/Email and password are required');
        return;
    }

    if (!usernameOrEmail) {
        showError(loginError, 'Username or email is required');
        return;
    }

    if (!password) {
        showError(loginError, 'Password is required');
        return;
    }

    loginBtn.textContent = 'Logging in...';
    loginBtn.disabled = true;

    try {
        const res = await post('/auth/login', {
            username_or_email: usernameOrEmail,
            password
        });
        const data = await res.json();

        if (!res.ok) {
            showError(loginError, data.error || 'Invalid credentials. Please try again.');
            return;
        }

        setAccessToken(data.access_token);
        setUser(data.user)
        window.location.href = 'feed.html';

    } catch {
        showError(loginError, 'Something went wrong. Please try again.');
    } finally {
        loginBtn.textContent = 'Log In';
        loginBtn.disabled = false;
    }
});

// ── Enter key support ─────────────────────────
passwordInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') loginBtn.click();
});

// ── Helpers ───────────────────────────────────
function showError(el, message) {
    el.textContent = message;
    el.style.display = 'block';
}