#!/bin/bash
set -e

# Check if the command being executed is the Gunicorn web server (or other web service)
if [ "$1" = "gunicorn" ]; then
    echo "Running Django setup commands for Web service..."

    # Ensure directories exist for static files and media
    mkdir -p /app/staticfiles /app/media
    chown -R appuser:appuser /app/staticfiles /app/media

    # 1. Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    # 2. Run database migrations (uncomment to enable)
    # echo "Running migrations..."
    # python manage.py migrate --noinput

    echo "Web service setup complete."
else
    echo "Skipping Django setup commands (running Celery or custom command)."
fi

# Execute the main command (e.g., gunicorn, celery worker, celery beat)
echo "Starting: $@"
exec "$@"
