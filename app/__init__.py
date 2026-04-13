import re

from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)

# Top-level origins are required: nested-only origins can leave Flask-CORS on its default "*",
# which breaks fetch(..., { credentials: "include" }).
# Regex covers any Vite port (5173, 5174 if 5173 is busy, etc.).
CORS(
    app,
    origins=[
        re.compile(r"^http://localhost:\d+$"),
        re.compile(r"^http://127\.0\.0\.1:\d+$"),
    ],
    # Match all paths under /api (explicit .*; * alone is a broken glob in regex).
    resources={r"^/api/.*": {}},
    supports_credentials=True,
    # Wildcard lets preflight succeed when the browser requests extra headers
    # (e.g. devtools, A11y, or X-CSRF-Token vs X-CSRFToken).
    allow_headers=["*"],
    methods=["GET", "POST", "OPTIONS"],
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import Movie

from app import views