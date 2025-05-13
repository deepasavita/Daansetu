import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daansetu.settings')
django.setup()

from daansetu.core.models import User

# Check if admin exists
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

try:
    # Create admin user with admin role
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role='admin'  # Set the role to admin
        )
        print(f"Superuser '{username}' created successfully.")
    else:
        print(f"Superuser '{username}' already exists.")
        
except Exception as e:
    print(f"Error creating superuser: {e}")