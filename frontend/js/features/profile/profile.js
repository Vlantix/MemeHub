import { get, post, patch, del, clearAuth } from '../../api/client.js';
import { requireAuth } from '../../utils/auth_guard.js';
import { timeAgo } from '../../utils/time_ago.js';

const flashContainer = document.getElementById('flash-container');
const navProfilePic = document.getElementById('nav-profile-pic');
const logoutBtn = document.getElementById('btn-logout');

const coverPhoto = document.getElementById('cover-photo');
const profilePhoto = document.getElementById('profile-photo');
const displayNameEl = document.getElementById('profile-display-name');
const usernameEl = document.getElementById('profile-username');
const joinedEl = document.getElementById('profile-joined');
const bioEl = document.getElementById('profile-bio');
const statPosts = document.getElementById('stat-posts');
const statTotalLikes = document.getElementById('stat-total-likes');

const memesGrid = document.getElementById('memes-grid');
const memesEmpty = document.getElementById('memes-empty');
const memesLoading = document.getElementById('memes-loading');

const tabButtons = document.querySelectorAll('.profile-tab');
const tabContents = document.querySelectorAll('.tab-content');

const btnEditProfile = document.getElementById('btn-edit-profile');
const editModal = document.getElementById('edit-profile-modal');
const btnCloseModal = document.getElementById('btn-close-modal');
const btnCancelModal = document.getElementById('btn-cancel-modal');
const btnSaveProfile = document.getElementById('btn-save-profile');
const editError = document.getElementById('edit-profile-error');
const editDisplayName = document.getElementById('edit-display-name');
const editBio = document.getElementById('edit-bio');

// Elements that get a shimmer while profile data is loading
const skeletonTargets = [coverPhoto, profilePhoto, displayNameEl, usernameEl, joinedEl, bioEl, statPosts, statTotalLikes];

let currentUserInfo = null;

init();

async function init() {
    const user = await requireAuth();
    if (!user) return; // requireAuth already redirected

    applyUserToNav(user);
    showSkeletons();
    await loadProfile();
}

function applyUserToNav(user) {
    if (user.avatar_url) {
        navProfilePic.src = user.avatar_url;
    }
}

// ── Skeleton states ───────────────────────────────
function showSkeletons() {
    skeletonTargets.forEach(el => el.classList.add('skeleton-text'));

    memesLoading.style.display = 'none';
    memesEmpty.style.display = 'none';
    memesGrid.style.display = 'grid';
    memesGrid.innerHTML = Array(6)
        .fill('<div class="meme-grid-item-skeleton skeleton"></div>')
        .join('');
}

function hideSkeletons() {
    skeletonTargets.forEach(el => el.classList.remove('skeleton-text'));
}

// ── Load profile ─────────────────────────────────
async function loadProfile() {
    try {
        const res = await get('/profile');

        if (!res.ok) {
            const data = await res.json();
            showFlash(data.error || 'Failed to load profile', 'error');
            return;
        }

        const { data } = await res.json();
        currentUserInfo = data.user_info;

        renderProfileInfo(data.user_info, data.total_posts, data.total_likes);
        renderMemes(data.recent_posts);

    } catch {
        showFlash('Something went wrong loading your profile.', 'error');
    } finally {
        hideSkeletons();
    }
}

function renderProfileInfo(userInfo, totalPosts, totalLikes) {
    displayNameEl.textContent = userInfo.display_name;
    usernameEl.textContent = `@${userInfo.username}`;
    joinedEl.textContent = timeAgo(userInfo.created_at);
    bioEl.textContent = userInfo.bio || 'No bio yet';

    statPosts.textContent = totalPosts || 0;
    statTotalLikes.textContent = totalLikes || 0;

    if (userInfo.profile_photo_url) {
        profilePhoto.src = userInfo.profile_photo_url;
    }
    if (userInfo.cover_photo_url) {
        coverPhoto.src = userInfo.cover_photo_url;
    }
}

// ── Render memes grid ────────────────────────────
function renderMemes(posts) {
    if (!posts || posts.length === 0) {
        memesGrid.style.display = 'none';
        memesEmpty.style.display = 'block';
        return;
    }

    memesGrid.style.display = 'grid';
    memesEmpty.style.display = 'none';
    memesGrid.innerHTML = posts.map(renderMemeCard).join('');
}

function renderMemeCard(post) {
    return `
        <div class="meme-grid-item" data-post-id="${post.id}">
            <img src="${post.image_url}" alt="Meme">
            <div class="meme-grid-overlay">
                <span>❤️ ${post.like_count || 0}</span>
                <span>💬 ${post.comment_count || 0}</span>
                <button type="button" class="btn-delete-meme delete-btn" data-post-id="${post.id}">🗑️</button>
            </div>
        </div>
    `;
}

// ── Delete meme (delegated) ──────────────────────
memesGrid.addEventListener('click', async (e) => {
    const deleteBtn = e.target.closest('.btn-delete-meme');
    if (!deleteBtn) return;

    const postId = deleteBtn.dataset.postId;

    if (!confirm('Delete this meme?')) {
        return;
    }

    try {
        const res = await del(`/delete_post/${postId}`);
        const data = await res.json();

        if (!res.ok) {
            showFlash(data.message || data.error || 'Failed to delete meme', 'error');
            return;
        }

        const card = memesGrid.querySelector(`.meme-grid-item[data-post-id="${postId}"]`);
        if (card) card.remove();

        const newCount = Math.max(0, parseInt(statPosts.textContent) - 1);
        statPosts.textContent = newCount;

        if (memesGrid.children.length === 0) {
            memesGrid.style.display = 'none';
            memesEmpty.style.display = 'block';
        }

        showFlash('Meme deleted', 'success');

    } catch {
        showFlash('Something went wrong. Please try again.', 'error');
    }
});

// ── Tabs ──────────────────────────────────────────
tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tab = button.dataset.tab;

        tabButtons.forEach(b => b.classList.remove('active'));
        button.classList.add('active');

        tabContents.forEach(content => {
            content.style.display = content.id === `tab-${tab}` ? 'block' : 'none';
        });
    });
});

// ── Edit profile modal ───────────────────────────
btnEditProfile.addEventListener('click', () => {
    editError.style.display = 'none';
    editDisplayName.value = currentUserInfo?.display_name || '';
    editBio.value = (currentUserInfo?.bio && currentUserInfo.bio !== 'No bio yet')
        ? currentUserInfo.bio
        : '';
    editModal.style.display = 'flex';
});

btnCloseModal.addEventListener('click', closeEditModal);
btnCancelModal.addEventListener('click', closeEditModal);

function closeEditModal() {
    editModal.style.display = 'none';
}

btnSaveProfile.addEventListener('click', async () => {
    editError.style.display = 'none';

    const displayName = editDisplayName.value.trim();
    const bio = editBio.value.trim();

    if (displayName && displayName.length < 3) {
        showEditError('Display name must be at least 3 characters');
        return;
    }
    if (displayName && displayName.length > 50) {
        showEditError('Display name must be less than 50 characters');
        return;
    }
    if (bio.length > 160) {
        showEditError('Bio must be less than 160 characters');
        return;
    }

    const payload = {};
    if (displayName && displayName !== currentUserInfo.display_name) {
        payload.display_name = displayName;
    }
    if (bio !== (currentUserInfo.bio || '')) {
        payload.bio = bio;
    }

    if (Object.keys(payload).length === 0) {
        closeEditModal();
        return;
    }

    btnSaveProfile.textContent = 'Saving...';
    btnSaveProfile.disabled = true;

    try {
        const res = await patch('/profile/update', payload);
        const data = await res.json();

        if (!res.ok) {
            showEditError(data.error || 'Failed to update profile');
            return;
        }

        currentUserInfo = data.user_info;
        renderProfileInfo(
            currentUserInfo,
            statPosts.textContent,
            statTotalLikes.textContent
        );

        closeEditModal();
        showFlash('Profile updated successfully! 🎉', 'success');

    } catch {
        showEditError('Something went wrong. Please try again.');
    } finally {
        btnSaveProfile.textContent = 'Save Changes';
        btnSaveProfile.disabled = false;
    }
});

function showEditError(message) {
    editError.textContent = message;
    editError.style.display = 'block';
}

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