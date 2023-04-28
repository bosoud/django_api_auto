import os
import subprocess
import sys

# Check if project name and virtual environment name are passed as arguments
if len(sys.argv) != 3:
    print("Usage: python3 run_django.py <project_name> <virtualenv_name>")
    sys.exit(1)

# Get project name and virtual environment name from arguments
project_name = sys.argv[1]
venv_name = sys.argv[2]

# Change to project directory
os.chdir(project_name)

# Activate virtual environment
activate_this = os.path.join(venv_name, "bin/activate_this.py")
try:
    with open(activate_this) as file:
        exec(file.read(), dict(__file__=activate_this))
except FileNotFoundError:
    print(f"Error: Couldn't find 'activate_this.py' in '{activate_this}'. Make sure the virtual environment is set up correctly.")
    sys.exit(1)

# Apply migrations
try:
    subprocess.run([sys.executable, "manage.py", "migrate"])
except Exception as e:
    print(f"Error: Couldn't apply migrations. Error message: {e}")
    sys.exit(1)

# Create super user
try:
    subprocess.run([sys.executable, "manage.py", "createsuperuser"])
except Exception as e:
    print(f"Error: Couldn't create superuser. Error message: {e}")
    sys.exit(1)

# Run Django development server
try:
    subprocess.run([sys.executable, "manage.py", "runserver"])
except Exception as e:
    print(f"Error running Django development server: {e}")
    sys.exit(1)

    print(f"\nDjango project '{project_name}' has been created successfully in '{project_path}'.")
    print(f"Use 'cd {project_name}' to move to the project directory.")
    print(f"Use 'source {venv_name}/bin/activate' to activate the virtual environment.")
    print(f"To start the development server, run 'python manage.py runserver'.")
    print(f"Open your web browser and go to http://127.0.0.1:8000/ to access your Django project.")