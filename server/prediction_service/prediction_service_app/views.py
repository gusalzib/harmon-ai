from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Song
import librosa
import numpy as np
from .methods import create_chroma, fetch_duration, get_tempo
from .prediction import predict, prediction_into_chords,structure_chords
from .file_handler import separate_audio, delete_audio_2_stems, delete_audio_4_stems
import tensorflow as tf
from spleeter.separator import Separator
from django import forms
import os

#this is the spleeter model
separator = Separator('spleeter:4stems')
#if you want to use 2 stems change the variable "stems" to 2
stems = 4

#this is our model
model = tf.saved_model.load("prediction_service_app/HarmonAi_v1-monday")

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

            #save audio in a folder and separate the audio
            audio_file_path, output_folder_name, prosessed_audio = separate_audio(audio, separator, stems)


            print("creating the waveform")
            #extract the samplingrate and create the waveform of the audio
            waveform, sampling_rate = librosa.load(prosessed_audio, sr=22050)
            #separate harmonics and percussives into two waveforms
            y_harmonic, y_percussive = librosa.effects.hpss(waveform)

            #call the methods to extract info from audio
            #chromagram = create_chroma(y_harmonic, y_percussive, sampling_rate)
            print("creating the chroma")
            chroma_T, index_of_the_beats, timestamps = create_chroma(y_harmonic, y_percussive, sampling_rate)




            print("getting the duration")
            print("TIMESTAMPS: ", timestamps)
            duration = fetch_duration(y_harmonic, sampling_rate)
            print("getting the tempo")
            tempo = get_tempo(y_percussive, sampling_rate)
            print("predicting")
            key_prediction, major_minor = predict(chroma_T,model)
            print("turn prediction into chords")
            chords = prediction_into_chords(key_prediction, index_of_the_beats, major_minor,timestamps)
            print("structure the chords")
            song_chords = structure_chords(chords)

            if stems == 2:
                print(delete_audio_2_stems(audio_file_path, output_folder_name,))
            else:
                print(delete_audio_4_stems(audio_file_path, output_folder_name,))
            
            #create the song object and save it to the db
            print("creates song object")
            new_song = Song.objects.create(
                title=title,
                artist=artist,
                genre=genre,
                tempo=tempo,
                duration=duration, 
                columns=["time","1=C", "2=C#", "3=D", "4=D#", "5=E", "6=F", "7=F#", "8=G", "9=G#", "10=A", "11=A#", "12=B"],
                chromogram=chroma_T.astype(float).tolist(),
                prediction=song_chords
                )
            new_song.save()

        

            response = JsonResponse({
                'title':title,
                'artist':artist,
                'genre':genre,
                'tempo':tempo,
                'duration':duration, 
                'chords':song_chords,
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


