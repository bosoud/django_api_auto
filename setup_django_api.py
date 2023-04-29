import os
import sys

# Get project path and app name from command line arguments
project_path = os.path.abspath(os.path.expanduser(sys.argv[1]))
project_name = os.path.basename(sys.argv[2])
app_name = sys.argv[3]


# Create directories for app and templates
app_dir = os.path.join(project_path, app_name)
os.makedirs(app_dir, exist_ok=True)
templates_dir = os.path.join(app_dir, "templates")
os.makedirs(templates_dir, exist_ok=True)

# Add DRF Spectacular to settings.py
settings_file = os.path.join(project_path, project_name, "settings.py")
print(f"Settings file path: {settings_file}")
with open(settings_file, "a") as f:
    f.write("\nREST_FRAMEWORK = {\n    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'\n}\n")
print(f"\nDRF Spectacular added to settings.py at {settings_file}.")

# Create serializers.py file for user registration serializer
serializers_file = os.path.join(app_dir, "serializers.py")
with open(serializers_file, "w") as f:
    f.write("from rest_framework import serializers\nfrom django.contrib.auth.models import User\n\n")
    f.write("class UserSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = User\n        fields = ['username', 'email', 'password']\n        extra_kwargs = {'password': {'write_only': True}}\n\n")
print(f"\nserializers.py file for user registration created successfully at {serializers_file}.")

# Create views.py file for user registration view
views_file = os.path.join(app_dir, "views.py")
with open(views_file, "w") as f:
    f.write("from rest_framework.views import APIView\nfrom rest_framework.response import Response\nfrom rest_framework import status\nfrom .serializers import UserSerializer\n\n")
    f.write("class UserRegistrationView(APIView):\n    serializer_class = UserSerializer\n\n    def post(self, request):\n        serializer = self.serializer_class(data=request.data)\n        if serializer.is_valid():\n            serializer.save()\n            return Response(serializer.data, status=status.HTTP_201_CREATED)\n        else:\n            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)\n\n")
print(f"\nviews.py file for user registration created successfully at {views_file}.")

# Update urls.py file to include user registration URL
# Update project's urls.py file to include DRF Spectacular schema view and UI
project_urls_file = os.path.join(project_path, project_name, "urls.py")
with open(project_urls_file, "a") as f:
    f.write(f"\nfrom drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView\n\n")
    f.write(f"\nfrom django.urls import include\n\n")
    f.write(f"urlpatterns += [\n")
    f.write(f"    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),\n")
    f.write(f"    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),\n")
    f.write(f"    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),\n")
    f.write(f"    path('api/{app_name}/', include('{app_name}.urls')),\n")
    f.write(f"]\n")
print(f"\nURL pattern for app {app_name} added successfully to {project_urls_file}.")
print(f"\nDRF Spectacular schema view and UI added to {project_urls_file}.")

app_urls_file = os.path.join(project_path, app_name, "urls.py")
# Create the app's urls.py file before appending content
with open(app_urls_file, "w") as f:
    f.write(f"\nfrom {app_name} import views\nfrom django.urls import path\n\n")
    f.write(f"urlpatterns = [\n    path('register/', views.UserRegistrationView.as_view()),\n]\n")
print(f"\nURL pattern for user registration added successfully to {app_urls_file}.")
