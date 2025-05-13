import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daansetu.settings')
django.setup()

from daansetu.core.models import User

test_users = [
    {
        'username': 'donor1',
        'email': 'donor1@example.com',
        'password': 'password123',
        'role': 'donor'
    },
    {
        'username': 'volunteer1',
        'email': 'volunteer1@example.com',
        'password': 'password123',
        'role': 'volunteer'
    }
]

created_count = 0
for user_data in test_users:
    username = user_data['username']
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username,
            email=user_data['email'],
            password=user_data['password'],
            role=user_data['role']
        )
        print(f"User '{username}' created successfully.")
        created_count += 1
    else:
        print(f"User '{username}' already exists.")

print(f"Created {created_count} test users.")