"""
Production settings for the project.
"""

from .settings import *  # Import all settings from the base settings file
import os

# ----------- PRODUCTION OVERRIDES -----------

# Disable debugging in production for security reasons
DEBUG = False

# Define allowed hosts (replace with your actual domain)
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']  # List of allowed hostnames

# ----------- CORS SETTINGS -----------

# Allow requests from your production frontend domain
CORS_ALLOWED_ORIGINS = [
    "https://www.yourfrontend.com",  # Frontend production domain
]

# ----------- DATABASE SETTINGS -----------

# Use PostgreSQL for production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL database engine
        'NAME': os.getenv('DB_NAME', 'mydatabase'),  # Database name (from environment variable)
        'USER': os.getenv('DB_USER', 'myuser'),  # Database user (from environment variable)
        'PASSWORD': os.getenv('DB_PASSWORD', 'mypassword'),  # Database password (from environment variable)
        'HOST': os.getenv('DB_HOST', 'localhost'),  # Database host (from environment variable)
        'PORT': os.getenv('DB_PORT', '5432'),  # Database port (default: 5432)
    }
}

# ----------- STATIC FILES -----------

# Set the directory where static files will be collected
STATIC_ROOT = BASE_DIR / 'staticfiles'  # This is where static files will be stored in production

# ----------- SECURITY SETTINGS -----------

# Force SSL redirects to ensure secure connections
SECURE_SSL_REDIRECT = True

# Ensure cookies are transmitted only over HTTPS
SESSION_COOKIE_SECURE = True  # Use secure cookies for sessions
CSRF_COOKIE_SECURE = True  # Secure the CSRF cookie

# Enable XSS filter for added security
SECURE_BROWSER_XSS_FILTER = True

# Prevent the site from being embedded in an iframe
X_FRAME_OPTIONS = 'DENY'

# ----------- LOGGING SETTINGS -----------

# Configure logging to store error logs in a file
LOGGING = {
    'version': 1,  # Logging configuration version
    'disable_existing_loggers': False,  # Don't disable existing loggers
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',  # Log to a file
            'filename': BASE_DIR / 'logs/django.log',  # Path to log file
        },
    },
    'root': {
        'handlers': ['file'],  # Use the file handler for root logger
        'level': 'ERROR',  # Log errors and above (critical issues)
    },
}

# ----------- EMAIL CONFIGURATION -----------

# Use SMTP for sending emails in production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# SMTP server settings (using environment variables for security)
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')  # Email server (Gmail example)
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))  # SMTP port (default: 587 for TLS)
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1')  # Enable TLS if set
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() in ('true', '1')  # Enable SSL if set
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Email account username
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Email account password
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)  # Default "From" email address
