#!/bin/bash

# Run migrations
echo "Run migrations"
python manage.py makemigrations
python manage.py migrate

# Start the application
gunicorn calendar_service.wsgi:application --bind 0.0.0.0:8000
