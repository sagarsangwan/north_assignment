import os
from django.http import JsonResponse
from urllib.parse import urlencode
import requests
from google_auth_oauthlib.flow import Flow


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
    print(token_json)
    if "access_token" not in token_json:
        return JsonResponse({"error": "failed to get access token"})
    access_token = token_json["access_token"]
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_response = requests.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_response.json()
    user_info["access_token"] = access_token
    return JsonResponse(user_info)


SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
]
# Store tokens temporarily
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8000/api/drive/callback/"

TOKEN_STORAGE = {}


def google_drive_auth(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

    return JsonResponse({"auth_url": auth_url})


def google_drive_callback(request):
    code = request.GET.get("code")
    print(code)
    if not code:
        return JsonResponse({"error": "code not provided"})
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = REDIRECT_URI
    flow.fetch_token(code=code)
    credentials = flow.credentials
    TOKEN_STORAGE["access_token"] = credentials.token
    return JsonResponse(
        {"message": "Drive connected successfully!", "access_token": credentials.token}
    )


def upload_file_to_drive(request):
    access_token = TOKEN_STORAGE.get("access_token")

    if not access_token:
        return JsonResponse({"error": "User not authenticated"}, status=401)

    file = request.FILES.get("file")

    if not file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    headers = {"Authorization": f"Bearer {access_token}"}
    metadata = {"name": file.name}

    files = {
        "data": ("metadata", json.dumps(metadata), "application/json"),
        "file": file,
    }

    response = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files,
    )

    return JsonResponse(response.json())
