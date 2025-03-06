from django.urls import path
from .views import google_login, google_callback, google_drive_upload

urlpatterns = [
    path("auth/login", google_login, name="google_login"),
    path("auth/callback/", google_callback, name="google_callback"),
    path("drive/upload", google_drive_upload, name="google_drive_upload"),
]
