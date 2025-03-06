import os
from django.http import JsonResponse
from urllib.parse import urlencode
import requests
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.views.decorators.csrf import csrf_exempt

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")
SCOPES = ["openid", "email", "profile", "https://www.googleapis.com/auth/drive"]


def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile https://www.googleapis.com/auth/drive",
        "access_type": "offline",
    }
    auth_url = f"{google_auth_url}?{urlencode(params)}"
    return JsonResponse({"auth_url": auth_url})


def google_callback(request):
    code = request.GET.get("code")
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
        return JsonResponse({"error": "failed to get access token"})
    access_token = token_json["access_token"]
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_response = requests.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    )
    user_info = user_info_response.json()
    user_info["access_token"] = access_token
    print(access_token)
    request.session["google_access_token"] = access_token
    response = JsonResponse(user_info)
    response.set_cookie("google_access_token", access_token)
    return response


@csrf_exempt
def google_drive_upload(request):
    access_token = request.COOKIES.get("google_access_token")
    print(request.COOKIES)
    # access_token = request.session.get("google_access_token")
    print(access_token)
    # refresh_token = request.session.get("google_refresh_token")

    if not access_token:
        return JsonResponse(
            {"error": "Please connect to Google Drive first."}, status=400
        )

    if request.method == "POST" and request.FILES["file"]:
        try:
            service = build(
                "drive",
                "v3",
                credentials=None,
                developerKey=None,
                http=None,
                static_discovery=False,
            )
            service._http.request = (
                requests.Session().request
            )  # fix for google api client
            service.credentials = type(
                "credentials",
                (),
                {"token": access_token},
            )  # create mock credentials
            file = request.FILES["file"]
            file_metadata = {"name": file.name}
            media = (
                service.files()
                .create(body=file_metadata, media_body=file.read(), fields="id")
                .execute()
            )
            return JsonResponse(
                {"message": f"File uploaded successfully! File ID: {media.get('id')}"}
            )
        except Exception as e:
            return JsonResponse({"error": f"Upload failed: {e}"}, status=500)
    return JsonResponse({"error": "No file provided."}, status=400)
