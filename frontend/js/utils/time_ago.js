// ================================================
// TIME AGO
// Mirrors the backend time_ago() helper in helper.py
// Converts a date string into a relative time label
// ================================================
 
export function timeAgo(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // seconds
 
    if (diff < 60) {
        return 'Just now';
    }
 
    const minutes = Math.floor(diff / 60);
    if (minutes < 60) {
        return minutes === 1 ? '1 minute ago' : `${minutes} minutes ago`;
    }
 
    const hours = Math.floor(minutes / 60);
    if (hours < 24) {
        return hours === 1 ? '1 hour ago' : `${hours} hours ago`;
    }
 
    const days = Math.floor(hours / 24);
    if (days === 1) return 'Yesterday';
    return `${days} days ago`;
}
 