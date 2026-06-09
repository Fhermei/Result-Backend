#!/bin/bash

# Exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

# Install additional packages if needed
pip install gunicorn whitenoise

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@gmail.com').exists():
    User.objects.create_superuser('admin@gmail.com', 'admin123', first_name='Admin', last_name='User')
    print("Superuser created")
else:
    print("Superuser already exists")
EOF

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"