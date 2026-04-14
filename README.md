# INFO3180 Lab 5 — Movies (Vue + Flask)
## Gavin Seaton -620043505

A small full-stack app: **Vue 3** (Vite) on the front end and a **Flask** JSON API on the back end. Users can add movies with a title, description, and poster image, and browse saved movies as cards.

## Features
- **Add movie** (`/movies/create`) — form with validation; poster file saved under `uploads/`, metadata in the database.
- **Movie list** (`/movies`) — fetches movies from the API and displays them as cards with poster images.
- **CSRF protection** — token fetched from the API and sent with `POST` requests (`X-CSRFToken` header).
- **Success / error feedback** — flash-style success after save; validation and server errors shown on the form.
## Tech stack
| Layer    | Technologies |
|----------|----------------|
| Frontend | Vue 3, Vue Router, Vite, Bootstrap (via CDN in `index.html`) |
| Backend  | Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF, Flask-CORS |
| Database | PostgreSQL via `DATABASE_URL` |
## Prerequisites
- **Node.js** (for `npm`)
- **Python 3** with `pip`
- A virtual environment is recommended for Python dependencies
## Environment variables
Create a `.env` file in the project root (see your course materials). Typical values:
```
FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=8080
SECRET_KEY= secret_key
DATABASE_URL=postgresql://tester:password@localhost/lab5
```

## Setup
### 1. Python (API)
```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
Apply database migrations:
flask db init
flask db upgrade
flask --app app run --debug
Terminal 2 — Vite
2. Node (frontend)
npm install
3. Run the app
npm run dev
```


# Snapshot
<img src = "photo/movies.png" alt = "List of movies">

<img src = "photo/add_movies.jpeg" alt = "Add movies">
