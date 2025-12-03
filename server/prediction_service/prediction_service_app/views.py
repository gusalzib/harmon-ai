from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Song
import librosa
import numpy as np
from .methods import create_chroma, fetch_duration, get_tempo


@csrf_exempt
def create_song(request):
    if request.method == "POST":
        try:
            #get the file from the request
            if 'audio' not in request.FILES:
                response = {
                    'result': 'error',
                    'status': 400,
                    'message': 'No audio file provided',
                }
                return response
            
            title = request.POST.get("title")
            artist = request.POST.get("artist")
            genre = request.POST.get("genre")
        
            audio = request.FILES['audio']
        
            #extract the samplingrate and create the waveform of the audio
            waveform, sampling_rate = librosa.load(audio, sr=None)

            #separate harmonics and percussives into two waveforms
            y_harmonic, y_percussive = librosa.effects.hpss(waveform)
            jump_time = 0.05 #this is good for tweaking the chroma

            #call the methods to extract info from audio
            chromagram = create_chroma(y_harmonic, y_percussive, sampling_rate,jump_time)
            duration = fetch_duration(y_harmonic, sampling_rate)
            tempo = get_tempo(y_percussive, sampling_rate)
            name = audio.name

            #create the song object and save it to the db
            new_song = Song.objects.create(
                title=title,
                artist=artist,
                genre=genre,
                tempo=tempo,
                duration=duration, 
                columns=["time","1=C", "2=C#", "3=D", "4=D#", "5=E", "6=F", "7=F#", "8=G", "9=G#", "10=A", "11=A#", "12=B"],
                chromogram=chromagram.astype(float).tolist()
                )
            new_song.save()

            response = JsonResponse({
                'result': 'success',
                'message': 'Audio received',
            },status=200)
            
        except json.JSONDecodeError:
            response = JsonResponse({
                'result': 'error',
                'message': 'Invalid JSON',
            },status=400)
    else:
        response = JsonResponse({
            'result': 'error',
            'message': 'Invalid request method',
        },status=400)

    return response

@csrf_exempt
def update_song(request):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            searchTitle = data.get("title")
            apdatedUser_rating = data.get("user_rating")
            Song.objects.filter(title=searchTitle).update(
                user_rating=apdatedUser_rating
            )

            response = JsonResponse({
                'result': 'success',
                'message': 'Song updated',
            }, status=200)
            
        except json.JSONDecodeError:
            response = JsonResponse({
                'result': 'error',
                'message': 'Invalid JSON',
            },status=400)
    else:
        response = JsonResponse({
            'result': 'error',
            'message': 'Invalid request method',
            },status=400)
        
    return response


