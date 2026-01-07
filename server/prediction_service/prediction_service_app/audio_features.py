import librosa
import numpy as np
import scipy.stats
import essentia.standard as es
import traceback
#librosa chroma pitch-class comes in this order:
# [C, C#, D, D#, E, F, F#, G, G#, A, A#, B]
#Add timestamp (in seconds) as column 0, so you get the shape (n, 13)

def create_chroma(y_harmonic, y_percussive, sampling_rate):

    #this gives a 0.046 s between each frame, just like the McGill dataset
    sampling_rate=22050
    
    # how far to "jump" in each step
    hop_length=1024

    #create the chroma by using the harmonic wave
    the_chroma = librosa.feature.chroma_cqt(
        y=y_harmonic,
        sr=sampling_rate,
        hop_length=hop_length
    )
    
    chromagram_T= the_chroma.T
    
    return chromagram_T

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

def get_tempo(y_percussive, sampling_rate):
    #this method is using essentia rhytm extractor to calculate bpm
    audio = np.asarray(y_percussive, dtype=np.float32)
    outputs = es.RhythmExtractor2013(method="multifeature")(audio)
    initial_bpm = float(outputs[0])
    beat_times = np.asarray(outputs[1], dtype=float)

    if beat_times.size >= 10:
        intervals = np.diff(beat_times)
        positive_intervals = intervals[intervals > 0]
        
        if positive_intervals.size > 0:
            bpm = 60.0/np.median(positive_intervals)
        else:
            bpm = initial_bpm
    else:
        bpm = initial_bpm
    return float(bpm), beat_times.tolist()

def tempo_formatting(the_tempo):
    the_tempo = round(the_tempo)
    the_tempo = str(the_tempo)
    the_tempo = the_tempo + " Bpm"
    return the_tempo

def get_index_of_the_beats(beat_times,sample_rate,hop_length):
    beat_times = np.asarray(beat_times, dtype=float)
    #Change seconds into frames
    beat_frames = np.rint(beat_times * sample_rate / hop_length).astype(int)

    #remove frames with negative values and duplicate frames
    beat_frames = beat_frames[beat_frames >=0]
    beat_frames = np.unique(beat_frames)

    return beat_frames
