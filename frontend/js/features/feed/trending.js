import { get, post, clearAuth } from '../../api/client.js';
import { requireAuth } from '../../utils/auth_guard.js';
import { timeAgo } from '../../utils/time_ago.js';

const rankBanners = document.getElementById('rank-banners');
const trendingContainer = document.getElementById('trending-container');
const trendingLoading = document.getElementById('trending-loading');
const trendingEmpty = document.getElementById('trending-empty');
const flashContainer = document.getElementById('flash-container');
const navProfilePic = document.getElementById('nav-profile-pic');
const logoutBtn = document.getElementById('btn-logout');
const filterTabs = document.querySelectorAll('.filter-tab');

let currentTimeframe = 'today';

init();

async function init() {
    const user = await requireAuth();
    if (!user) return;

    applyUserToNav(user);
    await loadTrending(currentTimeframe);
}

function applyUserToNav(user) {
    if (user.avatar_url) {
        navProfilePic.src = user.avatar_url;
    }
}

// ── Timeframe tab switching ─────────────────────
filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const timeframe = tab.dataset.timeframe;
        if (timeframe === currentTimeframe) return;

        filterTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        currentTimeframe = timeframe;
        loadTrending(currentTimeframe);
    });
});

// ── Load trending posts ──────────────────────────
async function loadTrending(timeframe) {
    trendingLoading.style.display = 'block';
    trendingContainer.style.display = 'none';
    trendingEmpty.style.display = 'none';
    rankBanners.innerHTML = '';

    try {
        const res = await get(`/trending?timeframe=${timeframe}&limit=10`);

        if (!res.ok) {
            const data = await res.json();
            showFlash(data.error || 'Failed to load trending posts', 'error');
            showEmptyState();
            return;
        }

        const data = await res.json();
        renderTrending(data.posts);

    } catch {
        showFlash('Something went wrong loading trending posts.', 'error');
        showEmptyState();
    } finally {
        trendingLoading.style.display = 'none';
    }
}

function showEmptyState() {
    trendingContainer.style.display = 'none';
    trendingEmpty.style.display = 'block';
}

function renderTrending(posts) {
    if (!posts || posts.length === 0) {
        showEmptyState();
        return;
    }

    const top3 = posts.slice(0, 3);
    const rest = posts.slice(3);

    rankBanners.innerHTML = top3.map(renderRankBanner).join('');

    trendingContainer.style.display = 'flex';
    trendingEmpty.style.display = 'none';
    trendingContainer.innerHTML = rest.map(post => renderPostCard(post)).join('');
}

function renderRankBanner(post, index) {
    const rankClasses = ['gold', 'silver', 'bronze'];
    const rankClass = rankClasses[index];
    const rankNum = index + 1;

    return `
        <div class="rank-banner">
            <div class="rank-number ${rankClass}">#${rankNum}</div>
            <div class="rank-info">
                <h4>${escapeHtml(post.caption || 'Untitled')}</h4>
                <p>by @${escapeHtml(post.username)} · ${post.time_ago}</p>
            </div>
            <div class="rank-stat">
                <span class="upvotes">❤️ ${post.like_count || 0}</span>
                <span class="comments">💬 ${post.comment_count || 0} comments</span>
            </div>
        </div>
    `;
}

function renderPostCard(post, rankIndex) {
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
                    <p>${post.time_ago}</p>
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
trendingContainer.addEventListener('click', async (e) => {
    const likeBtn = e.target.closest('.like-btn');
    if (!likeBtn) return;

    const postId = likeBtn.dataset.postId;
    const isLiked = likeBtn.classList.contains('liked');
    const likeCountSpan = likeBtn.querySelector('.like-count');
    const count = parseInt(likeCountSpan.textContent);

    try {
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
        // silently ignore
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