import { post } from '../../api/client.js';
import { isValidEmail } from '../../utils/validators.js';
import { showView } from './login.js';

// ── DOM: Forgot Password ────────────────────────
const emailInput = document.getElementById('forgot-email');
const forgotBtn = document.getElementById('btn-forgot');
const forgotError = document.getElementById('forgot-error');
const forgotSuccess = document.getElementById('forgot-success');

// ── DOM: Verify OTP ──────────────────────────────
const otpInput = document.getElementById('otp-code');
const verifyOtpBtn = document.getElementById('btn-verify-otp');
const otpError = document.getElementById('otp-error');
const otpGotoForgot = document.getElementById('otp-goto-forgot');

// ── DOM: Reset Password ──────────────────────────
const newPasswordInput = document.getElementById('reset-new-password');
const confirmPasswordInput = document.getElementById('reset-confirm-password');
const resetBtn = document.getElementById('btn-reset-password');
const resetError = document.getElementById('reset-error');

// Carries the email across the 3 steps
let pendingEmail = '';

// ── Step 1: Send reset code ──────────────────────
forgotBtn.addEventListener('click', async () => {
    const email = emailInput.value.trim();

    forgotError.style.display = 'none';
    forgotSuccess.style.display = 'none';

    if (!email) {
        showError(forgotError, 'Email is required');
        return;
    }

    if (!isValidEmail(email)) {
        showError(forgotError, 'Please enter a valid email address');
        return;
    }

    forgotBtn.textContent = 'Sending...';
    forgotBtn.disabled = true;

    try {
        const res = await post('/auth/forgot-password', { email });
        const data = await res.json();

        if (!res.ok) {
            showError(forgotError, data.error || 'Something went wrong. Please try again.');
            return;
        }

        pendingEmail = email;
        showView('view-verify-otp');

    } catch {
        showError(forgotError, 'Something went wrong. Please try again.');
    } finally {
        forgotBtn.textContent = 'Send Reset Code';
        forgotBtn.disabled = false;
    }
});

// ── Step 2: Verify OTP ────────────────────────────
verifyOtpBtn.addEventListener('click', async () => {
    const otp = otpInput.value.trim();

    otpError.style.display = 'none';

    if (!otp) {
        showError(otpError, 'Verification code is required');
        return;
    }

    if (otp.length !== 6) {
        showError(otpError, 'Code must be 6 digits');
        return;
    }

    verifyOtpBtn.textContent = 'Verifying...';
    verifyOtpBtn.disabled = true;

    try {
        const res = await post('/auth/verify-otp', { email: pendingEmail, otp });
        const data = await res.json();

        if (!res.ok) {
            showError(otpError, data.error || 'Invalid or expired code');
            return;
        }

        showView('view-reset-password');

    } catch {
        showError(otpError, 'Something went wrong. Please try again.');
    } finally {
        verifyOtpBtn.textContent = 'Verify Code';
        verifyOtpBtn.disabled = false;
    }
});

// Resend → back to forgot view
otpGotoForgot.addEventListener('click', (e) => {
    e.preventDefault();
    showView('view-forgot');
});

// ── Step 3: Set new password ──────────────────────
resetBtn.addEventListener('click', async () => {
    const newPassword = newPasswordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    resetError.style.display = 'none';

    if (!newPassword || !confirmPassword) {
        showError(resetError, 'Both password fields are required');
        return;
    }

    if (newPassword.length < 6) {
        showError(resetError, 'Password must be at least 6 characters');
        return;
    }

    if (newPassword !== confirmPassword) {
        showError(resetError, 'Passwords do not match');
        return;
    }

    resetBtn.textContent = 'Resetting...';
    resetBtn.disabled = true;

    try {
        const res = await post('/auth/reset-password', {
            email: pendingEmail,
            otp: otpInput.value.trim(),
            newPassword
        });
        const data = await res.json();

        if (!res.ok) {
            showError(resetError, data.error || 'Something went wrong. Please try again.');
            return;
        }

        showView('view-login');

    } catch {
        showError(resetError, 'Something went wrong. Please try again.');
    } finally {
        resetBtn.textContent = 'Reset Password';
        resetBtn.disabled = false;
    }
});

// ── Helpers ────────────────────────────────────────
function showError(element, message) {
    element.textContent = message;
    element.style.display = 'block';
}