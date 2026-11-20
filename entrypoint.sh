#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py makemigrations academy --noinput
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding initial Persian content and default admin (if empty)..."
python manage.py seed_initial_data

echo "Starting Gunicorn server..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
