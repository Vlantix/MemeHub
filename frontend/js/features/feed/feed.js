import { get, post, clearAuth } from '../../api/client.js';
import { requireAuth } from '../../utils/auth_guard.js';
import { timeAgo } from '../../utils/time_ago.js';

const feedContainer = document.getElementById('feed-container');
const feedLoading = document.getElementById('feed-loading');
const feedEmpty = document.getElementById('feed-empty');
const flashContainer = document.getElementById('flash-container');
const navProfilePic = document.getElementById('nav-profile-pic');
const logoutBtn = document.getElementById('btn-logout');

init();

async function init() {
    const user = await requireAuth();
    if (!user) return; // requireAuth already redirected

    applyUserToNav(user);
    await loadFeed();
}

function applyUserToNav(user) {
    if (user.avatar_url) {
        navProfilePic.src = user.avatar_url;
    }
}

// ── Load feed ────────────────────────────────────
async function loadFeed() {
    feedLoading.style.display = 'block';
    feedContainer.style.display = 'none';
    feedEmpty.style.display = 'none';

    try {
        const res = await get('/feed?limit=20&offset=0');

        if (res.status === 404) {
            showEmptyState();
            return;
        }

        if (!res.ok) {
            const data = await res.json();
            showFlash(data.error || 'Failed to load feed', 'error');
            showEmptyState();
            return;
        }

        const data = await res.json();
        renderPosts(data.data);

    } catch {
        showFlash('Something went wrong loading the feed.', 'error');
        showEmptyState();
    } finally {
        feedLoading.style.display = 'none';
    }
}

function showEmptyState() {
    feedContainer.style.display = 'none';
    feedEmpty.style.display = 'block';
}

function renderPosts(posts) {
    if (!posts || posts.length === 0) {
        showEmptyState();
        return;
    }

    feedContainer.style.display = 'flex';
    feedEmpty.style.display = 'none';
    feedContainer.innerHTML = posts.map(renderPostCard).join('');
}

function renderPostCard(post) {
    const initial = (post.display_name || post.username)[0].toUpperCase();

    const captionHtml = post.caption
        ? `<p>${escapeHtml(post.caption)}</p>`
        : '';

    const tagsHtml = post.tags
        ? `<div class="post-tags">${post.tags.split(',').map(t => `<span class="post-tag">#${escapeHtml(t.trim())}</span>`).join('')}</div>`
        : '';

    return `
        <div class="post-card" data-post-id="${post.id}">
            <div class="post-header">
                <div class="avatar"><span>${initial}</span></div>
                <div class="post-info">
                    <h4>${escapeHtml(post.display_name)} (@${escapeHtml(post.username)})</h4>
                    <p>${timeAgo(post.created_at)}</p>
                </div>
            </div>
            <div class="post-content">
                ${captionHtml}
                <div class="post-image">
                    <img src="${post.image_url}" alt="Meme">
                </div>
                ${tagsHtml}
            </div>
            <div class="post-stats">
                <span class="like-btn" data-post-id="${post.id}">
                    🤍 <span class="like-count">${post.like_count || 0}</span> likes
                </span>
                <span>💬 ${post.comment_count || 0} comments</span>
                <span>📌 0 saves</span>
            </div>
        </div>
    `;
}

// ── Like toggle (delegated) ─────────────────────
feedContainer.addEventListener('click', async (e) => {
    const likeBtn = e.target.closest('.like-btn');
    if (!likeBtn) return;

    const postId = likeBtn.dataset.postId;
    const isLiked = likeBtn.classList.contains('liked');
    const likeCountSpan = likeBtn.querySelector('.like-count');
    const count = parseInt(likeCountSpan.textContent);

    try {
        // NOTE: confirm actual like route/method against routes/likes.py
        const res = isLiked
            ? await post(`/posts/${postId}/unlike`)
            : await post(`/posts/${postId}/like`);

        if (!res.ok) return;

        if (isLiked) {
            likeBtn.classList.remove('liked');
            likeBtn.innerHTML = `🤍 <span class="like-count">${count - 1}</span> likes`;
        } else {
            likeBtn.classList.add('liked');
            likeBtn.innerHTML = `❤️ <span class="like-count">${count + 1}</span> likes`;
        }
    } catch {
        // silently ignore — like is non-critical
    }
});

// ── Logout ───────────────────────────────────────
logoutBtn.addEventListener('click', async (e) => {
    e.preventDefault();

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

// ── Helpers ──────────────────────────────────────
function showFlash(message, category) {
    flashContainer.innerHTML = `<div class="flash-message flash-${category}">${escapeHtml(message)}</div>`;
    setTimeout(() => {
        flashContainer.innerHTML = '';
    }, 4000);
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}