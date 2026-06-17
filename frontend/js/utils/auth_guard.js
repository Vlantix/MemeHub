// ================================================
// AUTH GUARD
// Call this at the top of any protected page.
// Redirects to auth.html if the user is not logged in.
// ================================================

import { getAccessToken, getUser } from '../api/client.js';

const BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5001' 
    : 'https://your-api-domain.com';


export async function requireAuth() {
    const token = getAccessToken();
    const user = getUser();

    if (!token && !user) {
        window.location.href = 'auth.html?mode=login';
        return null;
    }

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
        const res = await fetch(`${BASE_URL}/auth/refresh`, {
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