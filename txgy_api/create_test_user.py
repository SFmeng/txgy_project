#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.authentication.models import User

def create_test_user():
    try:
        # Try to create a test user
        user = User.objects.create_user(
            username='admin',
            password='admin123',
            user_type='individual'
        )
        print(f'Successfully created user: {user.username}')
        return user
    except Exception as e:
        print(f'Error creating user: {e}')
        # Try to get existing user and reset password
        try:
            user = User.objects.get(username='admin')
            user.set_password('admin123')
            user.save()
            print(f'User already exists, password reset: {user.username}')
            return user
        except User.DoesNotExist:
            print('No user found')
            return None

if __name__ == '__main__':
    create_test_user()
