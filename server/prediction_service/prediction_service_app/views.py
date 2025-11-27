from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.db import models
from .models import Song


@csrf_exempt
def create_song(request):
    if request.method == "POST":
        try:
            audio = json.loads(request.body)
            print("Received data:", audio)
            Song.objects.create(title=audio)

            response = {
                'status': 'success',
                'message': 'Audio received',
            }
            
        except json.JSONDecodeError:
            response = {
                'status': 'error',
                'message': 'Invalid JSON',
            }
    else:
        response = {
            'status': 'error',
            'message': 'Invalid request method',
        }
    return JsonResponse(response)

