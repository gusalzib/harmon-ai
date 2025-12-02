from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, requires_csrf_token
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json

# Create your views here.
# Some info about queries: https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Models#model_primer
# Might use index to redirect to either login or main-page. Some code from (https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/skeleton_website):
# from django.views.generic import RedirectView
# urlpatterns += [
#     path('', RedirectView.as_view(url='catalog/', permanent=True)),
# ]
def index(request):
    return JsonResponse({
        "message": "hey xD"
    }, status=200)

@ensure_csrf_cookie
def set_csrf_cookie(request):
    return JsonResponse({"message": "cookie 4 u"})


# @csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            request_body = json.loads(request.body)
            email = request_body.get("email")
            password = request_body["password"]
            new_user = User.objects.create_user(username=email, password=password)
            return JsonResponse({
                "message": "Signup successful"
            }, status=201)
        except:
            return JsonResponse({
                "message":"Registration failed, and we don't know why"
            }, status=400)
    else:
        return JsonResponse({"message": "Registration failed xD"},status=404)

# @csrf_exempt
@requires_csrf_token
def login(request): # Maybe call this in register()?
    if request.method != "POST":
        return JsonResponse({}, status=404)
    print(1)
    try:
        req_body = json.loads(request.body)
        print(req_body)
        user = authenticate(username=req_body["email"], password=req_body["password"])
        print(3)
        if user is None:
            return JsonResponse({
                "message": "Login failed: User is None"
            }, status=400)
        else:
            return JsonResponse({
                "message": "Login successfull"
            }, status=201)
            login(request)
    except:
        return JsonResponse({
            "message": "Login failed: Exception"
        }, status=400)