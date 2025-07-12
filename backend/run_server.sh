#!/bin/bash
echo "===================================================================================="

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Make migrations
echo ""
echo "Making migrations..."
python manage.py makemigrations
python manage.py makemigrations ipo_app
python manage.py makemigrations home
python manage.py makemigrations broker
echo "Making migrations... Done"

# Apply migrations
echo ""
echo "Applying migrations..."
python manage.py migrate
echo "Applying migrations... Done"

# Create superuser if it doesn't exist
echo ""
echo "Creating Django superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('✅ Django superuser created successfully (username: admin, password: admin)')
else:
    print('✅ Django superuser already exists')
"

# Run the development server
python manage.py runserver