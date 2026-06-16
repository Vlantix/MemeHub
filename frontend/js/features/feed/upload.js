import { post, clearAuth } from '../../api/client.js';
import { requireAuth } from '../../utils/auth_guard.js';

const fileInput = document.getElementById('file-input');
const previewBox = document.getElementById('preview-box');
const previewUsername = document.getElementById('preview-username');
const previewCategory = document.getElementById('preview-category');
const previewVisibility = document.getElementById('preview-visibility');
const captionInput = document.getElementById('caption');
const categorySelect = document.getElementById('category');
const tagOptions = document.querySelectorAll('.tag-option');
const visibilityOptions = document.querySelectorAll('.visibility-option');
const uploadBtn = document.getElementById('btn-upload');
const uploadError = document.getElementById('upload-error');
const flashContainer = document.getElementById('flash-container');
const navProfilePic = document.getElementById('nav-profile-pic');
const logoutBtn = document.getElementById('btn-logout');

let selectedTags = [];
let selectedFile = null;

init();

async function init() {
    const user = await requireAuth();
    if (!user) return;

    applyUserToNav(user);
}

function applyUserToNav(user) {
    if (user.avatar_url) {
        navProfilePic.src = user.avatar_url;
    }
    if (user.username) {
        previewUsername.textContent = `@${user.username}`;
    }
}

// ── Image preview ───────────────────────────────
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    selectedFile = file;

    const reader = new FileReader();
    reader.onload = (event) => {
        previewBox.innerHTML = `<img src="${event.target.result}" alt="Preview">`;
    };
    reader.readAsDataURL(file);
});

// ── Tag selection (max 5) ────────────────────────
tagOptions.forEach(button => {
    button.addEventListener('click', () => {
        const tag = button.dataset.tag;

        if (button.classList.contains('selected')) {
            button.classList.remove('selected');
            selectedTags = selectedTags.filter(t => t !== tag);
        } else {
            if (selectedTags.length < 5) {
                button.classList.add('selected');
                selectedTags.push(tag);
            } else {
                alert('You can only select up to 5 tags');
            }
        }
    });
});

// ── Category preview ─────────────────────────────
categorySelect.addEventListener('change', () => {
    previewCategory.textContent = categorySelect.options[categorySelect.selectedIndex].text;
});

// ── Visibility selection ─────────────────────────
visibilityOptions.forEach(option => {
    option.addEventListener('click', () => {
        visibilityOptions.forEach(o => o.classList.remove('active'));
        option.classList.add('active');

        const radio = option.querySelector('input[type="radio"]');
        radio.checked = true;
        previewVisibility.textContent = option.querySelector('span').textContent;
    });
});

// ── Submit upload ────────────────────────────────
uploadBtn.addEventListener('click', async () => {
    uploadError.style.display = 'none';

    if (!selectedFile) {
        showError('Please select an image to upload');
        return;
    }

    const visibility = document.querySelector('input[name="visibility"]:checked').value;

    const formData = new FormData();
    formData.append('meme_image', selectedFile);
    formData.append('caption', captionInput.value.trim());
    formData.append('category', categorySelect.value || '');
    formData.append('visibility', visibility);
    selectedTags.forEach(tag => formData.append('tags', tag));

    uploadBtn.textContent = 'Publishing...';
    uploadBtn.disabled = true;

    try {
        const res = await post('/upload', formData);
        const data = await res.json();

        if (!res.ok) {
            showError(data.message || data.error || 'Upload failed. Please try again.');
            return;
        }

        showFlash('Meme uploaded successfully! 🎉', 'success');
        setTimeout(() => {
            window.location.href = 'feed.html';
        }, 1200);

    } catch {
        showError('Something went wrong. Please try again.');
    } finally {
        uploadBtn.textContent = 'Publish Meme';
        uploadBtn.disabled = false;
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
function showError(message) {
    uploadError.textContent = message;
    uploadError.style.display = 'block';
}

function showFlash(message, category) {
    flashContainer.innerHTML = `<div class="flash-message flash-${category}">${escapeHtml(message)}</div>`;
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}