import os
import subprocess
import sys

def activate_venv(venv_path):
    activate_script = os.path.join(venv_path, "bin", "activate_this.py")
    if not os.path.exists(activate_script):
        raise FileNotFoundError(f"Cannot find {activate_script}")
    with open(activate_script) as f:
        code = compile(f.read(), activate_script, 'exec')
        exec(code, dict(__file__=activate_script))
        
def create_api(project_name, app_name, project_path, venv_name):
    print(f"Creating project directory '{project_path}'")
    project_dir = project_path
    os.makedirs(project_dir, exist_ok=True)

    print(f"Creating virtual environment '{venv_name}'")
    venv_path = os.path.join(project_path, venv_name)
    subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    
    print("Activating virtual environment")
    try:
        activate_venv(venv_path)
    except FileNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "virtualenv"])
        subprocess.check_call([sys.executable, "-m", "virtualenv", venv_path])
        activate_venv(venv_path)

    print("Installing Django, djangorestframework, and drf-spectacular")
    venv_python_executable = os.path.join(venv_path, "bin", "python")
    subprocess.check_call([venv_python_executable, "-m", "pip", "install", "django", "djangorestframework", "drf-spectacular"])
    
    print(f"Creating Django project '{project_name}'")
    django_admin = os.path.join(venv_path, "bin", "django-admin")
    subprocess.check_call([django_admin, "startproject", project_name, project_dir])

    print("Calling setup_django.py script")
    subprocess.check_call(["python3", "setup_django.py", project_name, app_name, "--project-path", project_path])

    print("Call setup_django_api.py script")
    subprocess.check_call(["python3", "setup_django_api.py", project_name, app_name])

if __name__ == "__main__":
    project_name = input("Enter the name of the Django project to create (default: myproject): ") or "myproject"
    app_name = input("Enter the name of the Django app to create (default: myapp): ") or "myapp"
    entered_directory = input(f"Enter the directory to create the Django project in (default: {project_name}): ") or project_name
    project_path = os.path.join(os.path.expanduser("~"), entered_directory)
    venv_name = input("Enter the name of the virtual environment to create (default: venv): ") or "venv"

     # Call create_api function
    create_api(project_name, app_name, project_path, venv_name)

    # Call run_django.py script
    subprocess.check_call(["python3", "run_django.py", project_name, venv_name])
