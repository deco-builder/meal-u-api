#!/bin/bash

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --no-input

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Start the application
echo "Starting the application..."
exec gunicorn --bind 0.0.0.0:$PORT campus_meal_kit.wsgi:application
