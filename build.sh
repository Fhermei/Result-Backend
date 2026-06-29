#!/bin/bash

set -o errexit

echo "=========================================="
echo "Starting Build Process"
echo "=========================================="

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser (if not exists)..."
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

echo "=========================================="
echo "Build Completed Successfully!"
echo "=========================================="