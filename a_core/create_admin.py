import os
import sys
from dotenv import load_dotenv

# Ensure the app root is in the Python path
sys.path.append('/app')

# Load environment variables from .env
load_dotenv()

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "a_core.settings"))

import django
django.setup()

from django.contrib.auth import get_user_model

# Create admin user only if it doesn't exist
User = get_user_model()
username = "admin"
email = "admin@example.com"
password = "adminpassword"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' created.")
else:
    print(f"ℹ️ Superuser '{username}' already exists.")
