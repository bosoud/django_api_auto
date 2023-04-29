import os
import subprocess
import sys

print("Start Run Django Script. run_django.py")

# Get project name and virtual environment name from arguments
project_path = sys.argv[1]
project_name = sys.argv[2]
manage_path = os.path.join(project_path, "manage.py")

# Apply migrations
print("Applying migrations...")
migrate_result = subprocess.run([sys.executable, manage_path, "migrate"], capture_output=True)
if migrate_result.returncode != 0:
    print(f"Error: Couldn't apply migrations. Return code: {migrate_result.returncode}")
    print(migrate_result.stderr.decode('utf-8'))
    sys.exit(1)

# Create super user
print("Creating superuser...")
try:
    subprocess.run([sys.executable, manage_path, "createsuperuser"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: Couldn't create superuser. Return code: {e.returncode}")
    print(e.stderr.decode('utf-8'))
    sys.exit(1)