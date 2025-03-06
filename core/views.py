import os
from django.http import JsonResponse
from urllib.parse import urlencode
import requests


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


def google_callback(request):
    code = request.GET.get("code")
    print(code)
    if not code:
        return JsonResponse({"error": "no code provided"}, status=400)
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    if "access_token" not in token_json:
        return JsonResponse({"error": "failed to get access token"}, error=500)
    access_token = token_json["access_token"]
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_response = requests.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_response.json()
    user_info["access_token"] = access_token
    return JsonResponse(user_info)
