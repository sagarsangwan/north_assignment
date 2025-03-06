from django.urls import path
from .views import google_login, google_callback

urlpatterns = [
    path("api/auth/login", google_login, name="google_login"),
    path("api/auth/callback/", google_callback, name="google_callback"),
]
