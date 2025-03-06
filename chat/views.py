from django.shortcuts import render
import os

# Create your views here.


def chat_view(request):
    websocket_url = os.environ.get("WEBSOCKET_URL")
    return render(request, "index.html", {"websocket_url": websocket_url})
