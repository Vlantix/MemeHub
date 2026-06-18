# MemeHub

A full-stack meme-sharing platform — rebuilt from the ground up as a decoupled REST API + static frontend, deployed live as a production-style portfolio project.

**Live:** [memehub-v2.vercel.app](https://memehub-v2.vercel.app) · API: `https://memehub-services.onrender.com`

> v1 of this project was a monolithic Flask + Jinja2 + SQLite app (server-rendered HTML, session-based auth). v2 is a full rewrite: a stateless Flask REST API backend and a vanilla JS frontend talking to it over HTTP, each deployed and scaled independently.

---

## Why a rewrite instead of an iteration

v1 worked, but server-rendered templates and session auth don't reflect how most production systems are actually built today, and they don't transfer to mobile clients or other frontends. Rebuilding instead of patching meant making (and owning) real architectural decisions: stateless auth instead of sessions, a database I don't control the runtime for, and a frontend that only knows about the API contract, not the server's internals.

| Decision | Instead of | Why |
|---|---|---|
| Decoupled API + static frontend | Server-rendered Jinja2 | Frontend/backend can scale, deploy, and fail independently; API is reusable by any future client |
| JWT access + refresh tokens | Flask sessions | Stateless backend, no server-side session store, works across origins (Vercel to Render) |
| Refresh token in httpOnly cookie, access token in memory/localStorage | Both in cookies, or both in localStorage | Refresh token never touches JS (XSS-resistant); access token stays short-lived and disposable |
| Supabase Postgres + Storage | SQLite + local filesystem | Real concurrent-write database and object storage that survive redeploys (Render's filesystem is ephemeral) |
| Vanilla JS, no framework | React/Vue | Forces understanding of the DOM, fetch, and state management directly before reaching for abstractions |

---

## Auth flow

- Register/Login: password hashed with Werkzeug, never stored or returned in plaintext.
- Access token: short-lived JWT, returned in the JSON response body, kept client-side.
- Refresh token: longer-lived JWT, set as an `httpOnly`, `Secure`, `SameSite=Strict` cookie. Never readable by JS, which is the actual point of splitting the two tokens.
- Refresh rotation: every call to `/auth/refresh` issues a new refresh token, not just a new access token, so a stolen refresh token has a shrinking window of validity.
- Password reset: OTP-based. `/auth/forgot-password` always returns the same generic message whether or not the email exists, which prevents account enumeration. The OTP is verified via `/auth/verify-otp` and exchanged for a short-lived, single-purpose `password_reset` token, which is the only thing accepted by `/auth/reset-password`. Each token type (access, refresh, password_reset) is checked against its expected type on decode, so a leaked reset token can't be replayed as an access token.

---

## API surface

| Domain | Routes |
|---|---|
| Auth | `POST /auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`, `/auth/forgot-password`, `/auth/verify-otp`, `/auth/reset-password` |
| Feed | `GET /feed`, `GET /trending` |
| Posts | `GET /post/<id>`, `POST /upload`, `DELETE /delete_post/<id>` |
| Profile | `GET /profile`, `PATCH /profile/update`, `PATCH /profile/photo`, `PATCH /profile/cover` |
| Comments | `GET/POST /posts/<id>/comments`, `PATCH/DELETE /posts/comments/<id>` |
| Likes | `POST /posts/<id>/like`, `POST /posts/<id>/unlike`, `GET /posts/<id>/status`, `GET /posts/<id>/likes` |

All routes that mutate or return user-specific data require a valid access token via `Authorization: Bearer <token>`.

---

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python, Flask, gunicorn |
| Database | PostgreSQL via Supabase (session pooler), raw parameterized SQL, no ORM |
| File storage | Supabase Storage (profile photos, cover photos, meme uploads) |
| Auth | PyJWT (access/refresh/reset tokens), Werkzeug password hashing |
| Email | Resend (OTP delivery) |
| Frontend | Vanilla HTML/CSS/JavaScript (ES modules, no framework) |
| Backend hosting | Render (gunicorn, `/healthz` pinged by UptimeRobot every 5 min to avoid cold starts) |
| Frontend hosting | Vercel |

---

## Architecture
 
```
MemeHub/
├── backend/                 Flask REST API
│   ├── app.py                App factory, blueprint registration, CORS config
│   ├── wsgi.py                gunicorn entrypoint
│   ├── config.py              Env var loading and startup validation
│   ├── routes/                 Blueprints: auth, feed, posts, profile, likes, comments
│   ├── db/
│   │   ├── connection.py        Supabase/Postgres connection and schema validation
│   │   └── queries/              Parameterized SQL per domain, no ORM
│   ├── utils/                  token.py (JWT), email.py (Resend), storage.py (Supabase Storage), decorators.py, validators.py
│   └── tests/                  .http request collections per route group
│
├── frontend/                 Static vanilla JS app
│   ├── *.html                  One page per route (auth, feed, upload, profile, trending)
│   ├── js/
│   │   ├── api/client.js         Fetch wrapper: attaches JWT, auto-refreshes on 401, retries once
│   │   ├── utils/auth_guard.js   requireAuth() / redirectIfLoggedIn() for page-level guards
│   │   ├── utils/time_ago.js     Relative timestamp formatting
│   │   └── features/             Per-page logic (auth, feed, profile), each with an init()
│   └── css/                     One stylesheet per page/component
```

Request flow: every protected frontend page calls `requireAuth()` on load. `client.js` attaches the JWT access token to outgoing requests. On a 401, the client silently calls `/auth/refresh` (which reads the httpOnly refresh cookie), gets a new access token, and retries the original request once. If refresh also fails, the user is redirected to login.

---

## Running locally
 
Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in SECRET_KEY, DATABASE_URL, SUPABASE_*, RESEND_*
python app.py           # runs on :5001, fails loudly if any required env var is missing
```
 
Frontend
 
Any static file server works, since this is plain HTML/CSS/JS with no build step.
 
Option 1: Python's built-in server
```bash
cd frontend
python -m http.server 5500
```
 
Option 2: VS Code Live Server extension
```
Open the frontend/ folder in VS Code, right-click any .html file, and select "Open with Live Server."
```
 
The frontend auto-detects `localhost` and points API calls at `http://localhost:5001` instead of the production Render URL, no config needed to switch.
 
---

## Roadmap

- Comment UI (backend routes exist, frontend not yet built)
- Notifications
- Rate limiting on auth endpoints
- Local Postgres dev mode (see `backend/docker-compose.yml`), so contributors can run the database without a Supabase account
- Liked and Saved tabs on profile page (Memes tab is wired up, Liked and Saved are still placeholders)
- UI polish and responsiveness improvements
 