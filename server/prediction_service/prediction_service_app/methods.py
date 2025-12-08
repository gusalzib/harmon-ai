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
    chromagram_T= the_chroma.T

    #remove the extra line so the sizes matches
    sliced_beat_into_time = 0.5 * (beat_into_time[:-1] + beat_into_time[1:])
    #add time to the chroma
    chroma = np.column_stack((sliced_beat_into_time, beat_chroma_T))
    
    return chromagram_T,index_of_the_beats

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
