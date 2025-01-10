#!/usr/bin/env bash

set -o errexit  # This will stop the script if any command fails

# Install dependencies
pip install -r requirements.txt

# Collect static files (this is usually done for deployment)
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Create superuser if none exists (based on your custom management command)
python manage.py create_superuser_if_none_exists
