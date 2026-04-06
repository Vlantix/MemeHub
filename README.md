# Dynamic MemeHub

A Flask-based meme sharing website.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Open http://127.0.0.1:5000/

## Features

- User registration and login
- Upload memes with images
- View feed of posts
- Profile page

## Database

The app uses SQLite. The database is created automatically on first run.

## Routes

- `/` - Landing page
- `/register` - User registration
- `/login` - User login
- `/home` - Main feed
- `/upload` - Upload new meme
- `/profile` - User profile
- `/trending` - Trending memes
- `/logout` - Logout