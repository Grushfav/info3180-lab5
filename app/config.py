import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if it exists.

# Project root (parent of app/)
_basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_instance_dir = os.path.join(_basedir, "instance")
os.makedirs(_instance_dir, exist_ok=True)
_default_sqlite_uri = "sqlite:///" + os.path.join(_instance_dir, "app.db").replace(os.sep, "/")


def _database_uri():
    uri = (os.environ.get("DATABASE_URL") or "").strip()
    if uri:
        return uri.replace("postgres://", "postgresql://", 1)
    return _default_sqlite_uri


class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed