import { post, clearAuth } from '../../api/client.js';

const logoutBtn = document.getElementById('btn-logout');

logoutBtn.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to log out?')) {
        return;
    }

    try {
        const res = await post('/auth/logout');
        const data = await res.json();

        if (!res.ok) {
            alert(data.error || 'Something went wrong. Please try again.');
            return;
        }

        clearAuth();
        window.location.href = 'auth.html';

    } catch {
        alert('Something went wrong. Please try again.');
    }
});