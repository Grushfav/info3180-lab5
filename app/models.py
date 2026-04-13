# Add any model classes for Flask-SQLAlchemy here
from datetime import datetime

from app import db


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster = db.Column(db.String(255), nullable=False)  # store filename/path
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
