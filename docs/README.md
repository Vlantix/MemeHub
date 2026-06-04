# MemeHub - Social Media Platform for Memes 🎭

A full-stack web application where users can share, discover, and manage memes. Built as a first-year HCI project.

## Live Demo 🌐

[View Live Site](https://memehub-hci-project.onrender.com)

---

## Features ✨

### User Authentication
- Register new account with validation
- Login with username/email
- Secure logout with confirmation
- Session-based authentication

### Meme Management
- Upload memes with image preview
- Add captions, categories, and tags (max 5)
- Set visibility (Public, Followers, Private)
- Delete your own memes

### Feed & Discovery
- Dynamic feed showing all public memes
- "Time ago" display (e.g., "2 hours ago")
- Trending tags sidebar
- Suggested creators widget

### User Profile
- View and edit profile (display name, bio)
- See all your uploaded memes in a grid
- Post count automatically updates
- Empty states for future features (Liked, Saved)

### UI/UX Highlights
- Dark theme with purple accent
- Fully responsive (mobile, tablet, desktop)
- Floating auto-dismiss flash messages
- Confirmation dialogs for destructive actions
- Like button visual feedback

---

## Tech Stack 🛠️

| Category | Technologies |
|----------|--------------|
| Backend | Python, Flask |
| Database | SQLite, SQLAlchemy ORM |
| Frontend | HTML5, CSS3, JavaScript |
| Templating | Jinja2 |
| Authentication | Flask Sessions, Werkzeug |
| File Upload | Secure filename handling |
| Deployment | Render |

---

## Project Structure 📁

MemeHub/
├── app.py
├── config.py
├── docker-compose.yml
├── Dockerfile
├── postgresql_schema.sql
├── requirements.txt
├── schema.sql
├── db/
│   ├── connection.py
│   └── queries/
│       ├── comments.py
│       ├── likes.py
│       ├── posts.py
│       ├── profile.py
│       ├── reset_password.py
│       └── users.py
├── docs/
│   ├── README.md
│   ├── REST_API ERROR CODE.txt
│   └── VSCODE EXTENSION.txt
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── comments.py
│   ├── feed.py
│   ├── likes.py
│   ├── main.py
│   ├── posts.py
│   └── profile.py
├── static/
│   ├── css/
│   │   ├── auth.css
│   │   ├── base.css
│   │   ├── components.css
│   │   ├── feed.css
│   │   ├── footer.css
│   │   ├── landing.css
│   │   ├── main.css
│   │   ├── modal.css
│   │   ├── navbar.css
│   │   ├── profile.css
│   │   ├── responsive.css
│   │   ├── trending.css
│   │   └── upload.css
│   └── images/
├── templates/
│   ├── feed.html
│   ├── index.html
│   ├── login.html
│   ├── profile.html
│   ├── register.html
│   ├── trending.html
│   └── upload.html
├── tests/
│   ├── __init__.py
│   ├── test_db.py
│   └── test-api.http
└── utils/
    ├── __init__.py
    ├── decorators.py
    ├── email.py
    ├── helper.py
    ├── storage.py
    └── token.py
