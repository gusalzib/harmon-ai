from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
import json

# Create your views here.
def index(request):
    return JsonResponse({
        "message": "hey xD"
    }, status=200)

@csrf_exempt
def register(request):
    if request.method == "POST":
        request_body = json.loads(request.body)
        email = request_body.get("email")
        password = request_body["password"]
        new_user = User.objects.create_user(username=email, password=password)
        return JsonResponse({
            "message": "Signup successful"
        }, status=201)
    else:
        return JsonResponse({"message": "Registration failed xD"},status=404)