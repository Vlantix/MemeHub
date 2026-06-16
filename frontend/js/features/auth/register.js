import { post } from '../../api/client.js';
import { isValidEmail } from '../../utils/validators.js';

const displayNameInput = document.getElementById('register-display-name');
const usernameInput = document.getElementById('register-username');
const emailInput = document.getElementById('register-email');
const passwordInput = document.getElementById('register-password');
const confirmPasswordInput = document.getElementById('register-confirm-password');
const registerBtn = document.getElementById('btn-register');
const registerError = document.getElementById('register-error');

registerBtn.addEventListener('click', async () => {
    const displayName = displayNameInput.value.trim();
    const username = usernameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    registerError.style.display = 'none';

    if (!displayName && !username && !email && !password && !confirmPassword) {
        showError(registerError, 'All fields are required');
        return;
    }

    if (!displayName) {
        showError(registerError, 'Display name is required');
        return;
    }

    if (!username) {
        showError(registerError, 'Username is required');
        return;
    }

    if (!email) {
        showError(registerError, 'Email is required');
        return;
    }

    if (!isValidEmail(email)) {
        showError(registerError, 'Please enter a valid email address');
        return;
    }

    if (!password) {
        showError(registerError, 'Password is required');
        return;
    }

    if (username.length < 3) {
        showError(registerError, 'Username must be at least 3 characters');
        return;
    }

    if (email.length < 6) {
        showError(registerError, 'Email must be at least 6 characters');
        return;
    }

    if (password.length < 6) {
        showError(registerError, 'Password must be at least 6 characters');
        return;
    }

    if (password !== confirmPassword) {
        showError(registerError, 'Passwords do not match');
        return;
    }

    registerBtn.textContent = 'Registering...';
    registerBtn.disabled = true;

    try {
        const res = await post('/auth/register', { 
            display_name: displayName, 
            username, 
            email,
            password,
            confirm_password: confirmPassword
        });
        const data = await res.json();

        if (!res.ok) {
            showError(registerError, data.error || 'Registration failed');
            return;
        }

        window.location.href = 'login.html';
    
    } catch {
        showError(registerError, 'Something went wrong. Please try again.');
    } finally {
        registerBtn.textContent = 'Register';
        registerBtn.disabled = false;
    }
});

// ── Helpers ───────────────────────────────────
function showError(el, message) {
    el.textContent = message;
    el.style.display = 'block';
}