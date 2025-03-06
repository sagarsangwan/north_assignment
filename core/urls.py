from django.urls import path
from .views import (
    google_login,
    google_callback,
    google_drive_auth,
    google_drive_callback,
    upload_file_to_drive,
)

urlpatterns = [
    path("auth/login", google_login, name="google_login"),
    path("auth/callback/", google_callback, name="google_callback"),
    path("auth/drive", google_drive_auth, name="google_drive_auth"),
    path("drive/callback", google_drive_callback),
    path("drive/upload-to-drive", upload_file_to_drive),
]
