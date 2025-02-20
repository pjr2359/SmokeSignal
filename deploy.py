import os

# Define paths
PROJECT_DIR = os.path.expanduser("~/SmokeSignal")
VENV_DIR = os.path.expanduser("~/.virtualenvs/venv")

# Pull the latest code from GitHub
os.system(f"cd {PROJECT_DIR} && git pull origin main")

# Activate virtual environment and install dependencies
os.system(f"source {VENV_DIR}/bin/activate && pip install -r {PROJECT_DIR}/requirements.txt")

# Collect static files (if using Django)
os.system(f"cd {PROJECT_DIR} && python manage.py collectstatic --noinput")

# Run migrations (if using Django)
os.system(f"cd {PROJECT_DIR} && python manage.py migrate")

# Restart the PythonAnywhere app
os.system("touch /var/www/pjr99_pythonanywhere_com_wsgi.py")
