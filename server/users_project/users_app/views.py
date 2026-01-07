# Authors of code:
# - 

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, requires_csrf_token
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse
from django.contrib.auth.models import User
from users_app.models import Profile, Preferences
from django.contrib.auth import authenticate, login, logout
from django.db import connections
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
        "message": "True"
    }, status=200)

### WELLNESS CHECKS ###
@require_GET
@csrf_exempt
def is_db_connected(request):
    try:
        db_connections = connections['default']
        db_connections.cursor()
        return JsonResponse({"message": "True"}, status=200)
    except Exception as e:
        return JsonResponse({"message": f"Error: {str(e)}"}, status=503)



### USER FEATURES ENDPOINTS ###
@ensure_csrf_cookie
def set_csrf_cookie(request):
    return JsonResponse({"message": "cookie 4 u"})


# @csrf_exempt
@require_POST
def register(request):
    try:
        request_body = json.loads(request.body)

        # Check if username is already taken
        username = request_body["username"]
        users = User.objects.filter(username=username)
        if len(users) != 0:
            return JsonResponse({"message": f"Username {username} already taken"}, status=409)

        password = request_body["password"]
        email = request_body["email"]

        # Create user and preferences, and store them in a profile
        new_user = User.objects.create_user(username=username, password=password, email=email)
        new_preferences = Preferences.objects.create()
        new_profile = Profile.objects.create(user=new_user, preferences=new_preferences)

        # Sanity check + example of syntax
        is_darkmode = new_user.profile.preferences.darkmode 
        print(f"Is darkmode? {is_darkmode}")

        return JsonResponse({"message": "Signup successful"}, status=201)
    except Exception as e:
        return JsonResponse({"message":f"Registration failed: {str(e)}"}, status=400)

# @csrf_exempt
@require_POST
@requires_csrf_token
def login(request): # Maybe call this in register()?
    try:
        req_body = json.loads(request.body)
        print(req_body)
        username = req_body["username"]
        password = req_body["password"]
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({
                "message": "Login failed: User is None"
            }, status=401)
        else:
            request.session["email"] = user.email
            request.session["username"] = user.username
            request.session.modified = True

            return JsonResponse({
                "message": "Login successful"
            }, status=201)
    except Exception as e:
        return JsonResponse({
            "message": f"Login failed: Exception: {str(e)}"
        }, status=500)
    
@require_POST
@requires_csrf_token
def logout_user(request):
    try:
        request.session.flush()
        return JsonResponse({"message": "Logout succesful"}, status=200)
    except Exception as e:
        return JsonResponse({"message": f"Logout failed: {str(e)}"}, status=500)

@require_GET
@requires_csrf_token
def get_user_preferences(request):
    try:
        username = request.session["username"]
        user = User.objects.get(username=username)
        if user is None:
            return JsonResponse({"message": "User not found"}, status=404)
        else:
            preferences = user.profile.preferences
            return JsonResponse({
                "preferences": {
                    "darkmode": preferences.darkmode
                }
            }, status=200)
    except Exception as e:
        return JsonResponse({"message": f"Internal Error: {str(e)}"}, status=500)
    
@require_GET
@requires_csrf_token
def get_user_info(request):
    try:
        email = request.session["email"]
        username = request.session["username"]
        print(f"email: {email}")
        print(f"username: {username}")
        if email and username:
            return JsonResponse({
                "email": email,
                "username": username
            }, status=200)
        else:
            return JsonResponse({
                "message": "Email couldn't be retrieved from session. Are you logged in?"
            }, status=400)
        
    except KeyError:
       return JsonResponse({
           "message": "KeyError"
       }, status=500)
    except:
       return JsonResponse({
           "message": "Catastrophic error"
       }, status=500)

@require_http_methods(["PUT"])
@requires_csrf_token
def change_password(request):
    try:
        # Get password deets
        req_body = json.loads(request.body)
        old_pass = req_body["oldPassword"]
        new_pass = req_body["newPassword"]

        if old_pass and new_pass:
            # Verify correct password
            username = request.session["username"]
            user = authenticate(username=username, password=old_pass)
            if user is not None:
                # If correct, change pass and save. Success
                user.set_password(new_pass)
                user.save()
                return JsonResponse({"message": "Password updated"}, status=200)
            else:
                return JsonResponse({"message": "user not found"}, status=404)
        else:
            return JsonResponse({"message": "Expected oldPassword and newPassword"}, status=400)
    except KeyError as e:
        # Means getting session data went wrong. Maybe redirect to logout then login??
        return JsonResponse({"message": f"KeyError. Session may be invalid: {str(e)}"}, status=500)
    except Exception as e:
        return JsonResponse({"message": f"Internal Error: {str(e)}"}, status=500)
    
@require_http_methods(["PUT"])
@requires_csrf_token
def edit_profile(request):
    try:
        # Retrieve email
        req_body = json.loads(request.body)
        new_email = req_body["email"]

        # Query for user and set new email
        username = request.session["username"]
        user = User.objects.get(username=username)
        user.email = new_email
        user.save()

        # Refresh session email value
        request.session["email"] = new_email
        return JsonResponse({"message": "Successfully updated profile"}, status=200)
    except KeyError as e:
        # Means getting session data went wrong. Maybe redirect to logout then login??
        return JsonResponse({"message": f"KeyError. Session may be invalid: {str(e)}"}, status=500)
    except Exception as e:
        return JsonResponse({"message": f"Internal Error: {str(e)}"}, status=500)

@require_GET
@requires_csrf_token
def check_status(request):
    response = {
        "logged_in": False,
        "is_superuser": False
    }

    try:
        # Check if logged in
        username = request.session["username"]
        user = User.objects.get(username=username)
        if user is not None:
            response["logged_in"] = True

        # Is admin?
        response["is_superuser"] = user.is_superuser
        return JsonResponse(response, status=200)
    except Exception as e:
        return JsonResponse(response, status=200)

# Experimental dataset upload eldpoint

def upload_dataset(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('datasetFile')
        
        if not uploaded_files:
            print('not files')
            return JsonResponse({
                'message': 'No files received'
            }, status=400)
        
        file_list = []
        total_size = 0

        for file in uploaded_files:
            file_name = file.name
            file_size = file.size
            total_size = total_size + file_size

            file_list.append({
                'name': file_name,
                'size': file_size,
                'content_type': file.content_type
            })
        total_size = total_size / (1024 / 1024)
        return JsonResponse({
            'message': f'Successfully received {len(uploaded_files)} files totalSize {total_size} MB',
            'uploaded_file_names': [f['name'] for f in file_list]
        }, status=200)
    
    return JsonResponse({
        'message': 'Something went wrong'
    }, status=500)