from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.db import models
from .models import Song
import librosa
import numpy as np



#librosa chroma pitch-class comes in this order:
# [C, C#, D, D#, E, F, F#, G, G#, A, A#, B]
#Add timestamp (in seconds) as column 0, so you get the shape (n, 13)

def create_chroma(waveform, sampling_rate):
    return chroma

def fetch_duration(waveform,sampling_rate):
    the_duration = librosa.get_duration(y=waveform,sr= sampling_rate)
    minutes = int(the_duration/60)
    sec = int(the_duration % 60)
    minutes = str(minutes)
    if(sec < 10):
        sec = str(sec)
        sec = str("0"+sec)
    else:
        sec = str(sec)
    transformed_duration = minutes + ":"+ sec
    return transformed_duration

def get_tempo(waveform, samling_rate):
    tempo = librosa.feature.tempo(waveform, samling_rate)
    return tempo


@csrf_exempt
def create_song(request):
    if request.method == "POST":
        try:
            #get the file from the request
            audio = request.FILES['audio']
            name = audio.name
            print("file is:", name)

            #extract the samplingrate and create the waveform of the audio
            waveform, sampling_rate = librosa.load(audio, sr=None)
            duration = librosa.get_duration(y=waveform,sr= sampling_rate)
            duration = fetch_duration(waveform, sampling_rate)
            print("duration", duration)
            new_song = Song.objects.create(title=name,duration=duration)
            new_song.save()
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



