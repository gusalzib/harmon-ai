from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.http import JsonResponse
import json
from .models import Song
import librosa
import numpy as np
#from django import forms
from django.db import connections
import os
import tensorflow as tf
from dotenv import load_dotenv
load_dotenv()


from spleeter.separator import Separator #The Spleeter model

from .audio_features import create_chroma, fetch_duration, get_tempo, tempo_formatting, get_index_of_the_beats
from .prediction import predict, prediction_into_chords
from .file_handler import separate_audio, download_model_from_google
from .output import remove_NX, chord_per_beat, chords_into_bars

BUCKET_NAME = "harmon_ai"
BASE_MODEL_PATH = "models" # GCS "folder"
MODEL_NAME = os.environ.get("MODEL_NAME")
if not MODEL_NAME:
    raise RuntimeError("MODEL_NAME variable is not set")


local_dir = download_model_from_google(BUCKET_NAME, BASE_MODEL_PATH, MODEL_NAME)

#this is the spleeter model
separator = Separator('spleeter:4stems')
#there is two options for the spleeter model. use 2 stems or 4 stems.
#update the variable "stems" depending on what you choose
stems = 4

#this is our model
model = tf.saved_model.load(local_dir)

#the old way of loading our model when it was saved in repo
#model = tf.saved_model.load("prediction_service_app/HarmonAi_v1-monday")


#ping for google cloud storage connection
@require_GET
@csrf_exempt
def is_db_connected(request):
    try:
        db_connections = connections['default']
        db_connections.cursor()
        return JsonResponse({"message": "True"}, status=200)
    except Exception as e:
        return JsonResponse({"message": f"Error: {str(e)}"}, status=503)

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
            print("got the Audio")
            title = request.POST.get("title")
            artist = request.POST.get("artist")
            genre = request.POST.get("genre")
            audio = request.FILES['audio']
            #sr could be 22050 or 44100
            #create the waveform of the audio
            waveform, sampling_rate = librosa.load(audio, sr=44100, mono=False)
            hop_length = 1024
            #Separate the audio
            if stems==2:
                prosessed_audio = separate_audio(waveform, separator, stems)
                percussive = prosessed_audio
            else:
                prosessed_audio,percussive  = separate_audio(waveform, separator, stems)
                
            tempo, beat_times = get_tempo(percussive, sampling_rate)
            formated_tempo = tempo_formatting(tempo)

            print("separate audio")
            #create the chromagram
            chromagram = create_chroma(prosessed_audio, percussive, sampling_rate)
            print("create chroma")
            index_of_the_beats = get_index_of_the_beats(beat_times,sampling_rate,hop_length)
            #collect information from the audio file
            duration = fetch_duration(prosessed_audio, sampling_rate)
            
            #formated_tempo = tempo_formatting(tempo)
            print("tempo:",tempo)
            
            #getting the prediction from the model
            key_prediction, major_minor = predict(chromagram,model)
            print("predicted")

            #translate and structure the output
            chords = prediction_into_chords(key_prediction, major_minor)
            print("prediction translated")
            chords1 = remove_NX(chords)
            print("remove x and n")
            chords2 = chord_per_beat(chords1, index_of_the_beats)
            print("turn itno beats")
            chords3 = chords_into_bars(chords2)
            print("structure the chords")

            
            #create the song object and save it to the db
            print("creates song object")
            new_song = Song.objects.create(
                title=title,
                artist=artist,
                genre=genre,
                tempo=formated_tempo,
                duration=duration, 
                columns=["time","1=C", "2=C#", "3=D", "4=D#", "5=E", "6=F", "7=F#", "8=G", "9=G#", "10=A", "11=A#", "12=B"],
                chromogram=chromagram.astype(float).tolist(),
                prediction=chords3
                )
            new_song.save()

    
            response = JsonResponse({
                'title':title,
                'artist':artist,
                'genre':genre,
                'tempo':formated_tempo,
                'duration':duration, 
                'chords':chords3,
                'result': 'success',
                'message': 'Audio received',
            },status=200)
            
        except json.JSONDecodeError:
            print("Invalid JSON error:", e, flush=True)
            response = JsonResponse({
                'result': 'error',
                'message': 'Invalid JSON',
            },status=400)
        except Exception as e:
            print("Caught Exception:", e, flush=True)
            response = JsonResponse({'message': f"Exception: {str(e)}"}, status=500)
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
            updatedUser_rating = data.get("user_rating")
            Song.objects.filter(title=searchTitle).update(
                user_rating=updatedUser_rating
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



@csrf_exempt
def get_songs(request):
    if request.method == "GET":
        try:
            songs_query = Song.objects.all()

            searchGenre = request.GET.get("genre")
            if searchGenre:
                songs_query= Song.objects.filter(genre__icontains=searchGenre)

            searchArtist = request.GET.get("artist")
            if searchArtist:
                songs_query= Song.objects.filter(artist__icontains=searchArtist)
            searchTitle =request.GET.get("title")            
            if searchTitle:
                songs_query= Song.objects.filter(title__icontains=searchTitle)
            
        
            if not songs_query.exists():
                return JsonResponse({
                    'result': 'error',
                    'message': 'No songs found in this genre',
                    },status=404)
                
            #turn result of filter int a song object
            songs = list(songs_query.values(
                "title",
                "artist",
                "genre",
                "tempo",
                "duration",
                "prediction",
            ))

            response = JsonResponse({
                "songs": songs,
                'result': 'success',
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
    