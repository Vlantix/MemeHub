// ================================================
// AUTH GUARD
// Call this at the top of any protected page.
// Redirects to auth.html if the user is not logged in.
// ================================================

import { getAccessToken, getUser } from '../api/client.js';

export async function requireAuth() {
    const token = getAccessToken();
    const user = getUser();

    // No token at all — go to login
    if (!token && !user) {
        window.location.href = 'auth.html?mode=login';
        return null;
    }

    // Token exists but may be expired — try a silent refresh
    if (!token && user) {
        const newToken = await tryRefresh();
        if (!newToken) {
            window.location.href = 'auth.html?mode=login';
            return null;
        }
    }

    return getUser();
}

async function tryRefresh() {
    try {
        const res = await fetch('http://localhost:5001/auth/refresh', {
            method: 'POST',
            credentials: 'include',
        });

        if (!res.ok) return null;

        const data = await res.json();

        const { setAccessToken } = await import('../api/client.js');
        setAccessToken(data.access_token);
        return data.access_token;
    } catch {
        return null;
    }
}

export function redirectIfLoggedIn() {
    const token = getAccessToken();
    if (token) {
        window.location.href = 'feed.html';
    }
}