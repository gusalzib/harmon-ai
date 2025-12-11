
import tensorflow as tf
import librosa
import numpy as np
import collections
from collections import Counter

N = 12
MAJOR = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B", "N", "X"]
MINOR = ["Cm", "C#m", "Dm", "Ebm", "Em", "Fm", "F#m", "Gm", "Abm", "Am", "Bbm", "Bm", "N", "X"]
N = 'N'


def predict(chroma_T, model):
    # features = np.array(chromagram, dtype=np.float32)
    features= tf.constant(chroma_T, dtype=tf.float32)
    result = model(features)
    key=result['key_probs'].numpy()
    quality=result['quality_probs'].numpy()
    key_predictions=np.argmax(key,axis=1)
    major_minor = np.argmax(quality,axis=1)
    
    return key_predictions,major_minor

def chord_filter(interval, **kwargs):
    counts = collections.Counter(interval).most_common()
    first_chord = counts[0][0]
    if first_chord == N:
        if len(counts) <=1:
            strongest_chord= counts[0][0]
        else:
            strongest_chord= counts[1][0]
    else:
        strongest_chord = counts[0][0]
    
    return strongest_chord

def prediction_into_chords(key_prediction, index_of_the_beats, major_minor, timestamps):
    prediction_with_quality=np.stack((key_prediction, major_minor), axis=1)
    condition = (prediction_with_quality[:,1] == 2)
    result_true = (np.array(MAJOR)[ prediction_with_quality[:,0]])
    result_false = ((np.array(MINOR)[ prediction_with_quality[:,0]]))
    quality_chords = np.where(condition, result_true, result_false)

    chords_beat= librosa.util.sync(
        data=quality_chords,
        idx=index_of_the_beats.astype(int),
        aggregate=chord_filter,
        pad=False
    )
     
    #[0] 7, [1] none, [2] Major , [3] MINOR
    return chords_beat

def structure(interval,**kwargs):
    bar=[]
    last_chord= None
    for chord in interval:
        if chord != last_chord:
            bar.append(chord)
        last_chord = chord

    chord_string = " ".join(bar)
    return chord_string


def structure_chords(chords_beat):
    chords_array = np.array(chords_beat, dtype='<U8')
    chords_array = chords_array[1:]
    #first_chord=chords_array[0]
    #chords_array = np.insert(chords_array, 0,first_chord)
    total_beats = len(chords_beat)
    bars = np.arange(0, total_beats, 4)

    chords_bar= librosa.util.sync(
    data=chords_array,
    idx= bars,
    aggregate=chord_filter,
    pad=False
    )
    chords_bar_list = chords_bar.tolist()

    joined_chords_bar = " | ".join(chords_bar_list)
    final_chords_bar = "| " + joined_chords_bar.strip()

    print("CHORDS_BEAT : ", chords_beat)
    print("PRINT THE CHORDS",final_chords_bar)
    return final_chords_bar
