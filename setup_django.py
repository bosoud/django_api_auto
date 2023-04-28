import argparse
import os
import subprocess
import sys

def create_app(project_name, app_name, project_path):
    print(f"Creating Django app '{app_name}' in '{project_path}'")

    os.chdir(project_path)
    manage_py = os.path.join(project_path, "manage.py")
    subprocess.check_call([sys.executable, manage_py, "startapp", app_name])

    print(f"Updating settings.py for app '{app_name}'")

    settings_py = os.path.join(project_path, project_name, "settings.py")
    with open(settings_py, "r") as file:
        content = file.read()

    content = content.replace(
        "INSTALLED_APPS = [",
        f"INSTALLED_APPS = [\n    '{app_name}',\n    'rest_framework',\n    'drf_spectacular',",
    )

    content = content.replace(
        "ALLOWED_HOSTS = []",
        "ALLOWED_HOSTS = ['*']",
    )

    content += "\n\nCORS_ALLOW_ALL_ORIGINS = True\n\n"
    content += "SPECTACULAR_SETTINGS = {\n    'TITLE': 'Your API',\n    'DESCRIPTION': 'Your API description',\n}\n\n"

    with open(settings_py, "w") as file:
        file.write(content)

    print(f"App '{app_name}' has been created and configured in '{project_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up a Django app with a REST API.")
    parser.add_argument("project_name", help="The name of the Django project.")
    parser.add_argument("app_name", help="The name of the Django app to create.")
    parser.add_argument("--project-path", help="The path to the Django project directory.", default=".")

    args = parser.parse_args()

    create_app(args.project_name, args.app_name, args.project_path)
