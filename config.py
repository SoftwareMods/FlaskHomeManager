"""Flask configuration."""
import os


#common variables
SECRET_KEY = os.urandom(50)
STATIC_FOLDER = 'static'
TEMPLATES_FOLDER = 'templates'
SESSION_SQLALCHEMY = True
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
BOOTSTRAP_SERVE_LOCAL = True
# SESSION_COOKIE_SAMESITE='Strict'
