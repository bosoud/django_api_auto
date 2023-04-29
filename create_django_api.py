import os
import subprocess
import sys

# Global variable
global venv_path
global venv_python_executable

def activate_venv():
    print("Activation Of Virtualenv")
    try:
        activate_script = os.path.join(venv_path, "bin", "activate_this.py")
    except FileNotFoundError:
        print(f"Error Handling activate venv where path: {venv_path}")

    if not os.path.exists(activate_script):
        raise FileNotFoundError(f"Cannot find {activate_script}")
    with open(activate_script) as f:
        code = compile(f.read(), activate_script, 'exec')
        exec(code, dict(__file__=activate_script))
    print(f"Virtual environment activated: {venv_path}")

def create_venv():
    print("Creating Of Virtualenv")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "virtualenv"])
        subprocess.check_call([sys.executable, "-m", "virtualenv", venv_path])
        activate_venv()
    except FileNotFoundError:
        print(f"Error Handling activate venv where path: {venv_path}")


def create_api(project_name, app_name, project_path, venv_name):
    os.makedirs(project_path, exist_ok=True)
    subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    
    #Create And Activate virtualenv
    create_venv()
    global venv_python_executable
    venv_python_executable = os.path.join(venv_path, "bin", "python")
    subprocess.check_call([venv_python_executable, "-m", "pip", "install", "django", "djangorestframework", "drf-spectacular"])
    print("installed all pip requerment")
    django_admin = os.path.join(venv_path, "bin", "django-admin")
    subprocess.check_call([django_admin, "startproject", project_name, project_path])
    subprocess.check_call(["python3", "setup_django.py", project_name, app_name, "--project-path", project_path])
    subprocess.check_call(["python3", "setup_django_api.py", project_path, project_name, app_name])

    # Call run_django.py script
    subprocess.check_call(["python3", "run_django.py", project_path, project_name])


if __name__ == "__main__":
    project_name = input("Enter the name of the Django project to create (default: myproject): ") or "myproject"
    app_name = input("Enter the name of the Django app to create (default: myapp): ") or "myapp"
    entered_directory = input(f"Enter the directory to create the Django project in (default: {project_name}): ") or project_name
    project_path = os.path.join(os.path.expanduser("~"), entered_directory)
    venv_name = input("Enter the name of the virtual environment to create (default: venv): ") or "venv"
    venv_path = os.path.join(project_path, venv_name)
    manage_path = os.path.join(project_path, "manage.py")

     # Call create_api function
    create_api(project_name, app_name, project_path, venv_name)


# Run Django development server
command = [venv_python_executable, manage_path, "runserver"]

try:

    server_process = subprocess.Popen(command)

    # Wait for the server process to finish
    server_process.wait()
    print(f"\nDjango project '{project_name}' has been created successfully in '{project_path}'.")
    print(f"Use 'cd {project_name}' to move to the project directory.")
    print(f"Use 'source {venv_name}/bin/activate' to activate the virtual environment.")
    print(f"To start the development server, run 'python {manage_path} runserver'.")
    print(f"Open your web browser and go to http://127.0.0.1:8000/ to access your Django project.")
    # Read the output from the server process and print it
    while True:
        output = server_process.stdout.readline()
        if output == '' and server_process.poll() is not None:
            break
        if output:
            print(output.strip())

except KeyboardInterrupt:
    print("\nDjango development server stopped by user.")
    server_process.terminate()
    server_process.wait()
