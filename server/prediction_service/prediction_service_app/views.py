from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Song
import librosa
import numpy as np



#librosa chroma pitch-class comes in this order:
# [C, C#, D, D#, E, F, F#, G, G#, A, A#, B]
#Add timestamp (in seconds) as column 0, so you get the shape (n, 13)

def create_chroma(y_harmonic, y_percussive, sampling_rate, jump_time):
    # how far to "jump" in each step
    hop_length = int(sampling_rate * jump_time)

    #create the chroma by using the harmonic wave
    the_chroma = librosa.feature.chroma_cqt(
        y=y_harmonic,
        sr=sampling_rate,
        hop_length=hop_length
    )
    #get the tempo and an array of all the frame indices where there is a beat
    tempo, index_of_the_beats = librosa.beat.beat_track(
        y=y_percussive, 
        sr=sampling_rate,
        hop_length=hop_length
    )
    #put together the beat with the frames so that you 
    #have a list of the frames that is within two beats.
    beat_chroma = librosa.util.sync(
        the_chroma,
        index_of_the_beats,
        aggregate=np.median,
        pad=False
    )
    #make the array show what time the beats occur insted of what index
    beat_into_time = librosa.frames_to_time(
        index_of_the_beats,
        sr=sampling_rate,
        hop_length=hop_length
    )
    #flip the columns and rows in the chroma
    beat_chroma_T = beat_chroma.T

    #remove the extra line so the sizes matches
    sliced_beat_into_time = 0.5 * (beat_into_time[:-1] + beat_into_time[1:])
    #add time to the chroma
    chroma = np.column_stack((sliced_beat_into_time, beat_chroma_T))
    
    return chroma

def fetch_duration(y_harmonic,sampling_rate):
    the_duration = librosa.get_duration(y=y_harmonic,sr= sampling_rate)
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

def get_tempo(y_percussive, samling_rate):
    the_tempo = librosa.feature.tempo(y=y_percussive,sr=samling_rate)
    the_tempo = round(the_tempo[0])
    the_tempo = str(the_tempo)
    the_tempo = the_tempo + " Bpm"
    return the_tempo


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


