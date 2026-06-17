// ================================================
// API CLIENT
// Base fetch wrapper with JWT token handling
// and automatic access token refresh
// ================================================

const BASE_URL = (() => {
    // Local Development
    if (window.location.hostname === 'localhost') {
        return 'http://localhost:5000/api';
    }

    // Production Development
    return 'https://memehub-services.onrender.com';
})();

// ── Token helpers ──────────────────────────────
export function getAccessToken() {
    return localStorage.getItem('access_token');
}

export function setAccessToken(token) {
    localStorage.setItem('access_token', token);
}

export function clearAuth() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
}

export function getUser() {
    const raw = localStorage.getItem('user');
    return raw ? JSON.parse(raw) : null;
}

export function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

// ── Token refresh ──────────────────────────────
async function refreshAccessToken() {
    try {
        const res = await fetch(`${BASE_URL}/auth/refresh`, {
            method: 'POST',
            credentials: 'include',   // sends the httpOnly refresh_token cookie
        });

        if (!res.ok) return null;

        const data = await res.json();
        setAccessToken(data.access_token);
        return data.access_token;
    } catch {
        return null;
    }
}

// ── Core request function ──────────────────────
// Automatically attaches Authorization header.
// On 401, attempts one token refresh then retries.
export async function request(endpoint, options = {}) {
    const token = getAccessToken();

    const headers = {
        ...options.headers,
    };

    // Only set Content-Type to JSON if not sending FormData
    if (!(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    let res = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers,
        credentials: 'include',
    });

    // Token expired — try refresh once then retry
    if (res.status === 401) {
        const newToken = await refreshAccessToken();

        if (!newToken) {
            clearAuth();
            window.location.href = 'auth.html?mode=login';
            return null;
        }

        headers['Authorization'] = `Bearer ${newToken}`;

        res = await fetch(`${BASE_URL}${endpoint}`, {
            ...options,
            headers,
            credentials: 'include',
        });
    }

    return res;
}

// ── Convenience methods ────────────────────────
export async function get(endpoint) {
    return request(endpoint, { method: 'GET' });
}

export async function post(endpoint, body) {
    return request(endpoint, {
        method: 'POST',
        body: body instanceof FormData ? body : JSON.stringify(body),
    });
}

export async function patch(endpoint, body) {
    return request(endpoint, {
        method: 'PATCH',
        body: body instanceof FormData ? body : JSON.stringify(body),
    });
}

export async function del(endpoint) {
    return request(endpoint, { method: 'DELETE' });
}