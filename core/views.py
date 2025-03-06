import os
from django.http import JsonResponse
from urllib.parse import urlencode


def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    print(os.environ.get("GOOGLE_REDIRECT_URI"))
    auth_url = f"{google_auth_url}?{urlencode(params)}"
    return JsonResponse({"auth_url": auth_url})
