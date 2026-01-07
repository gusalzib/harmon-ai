import librosa
import numpy as np
import collections
from collections import Counter

N = 'N'
X = 'X'

def remove_NX (translated_prediction):

    NX_removed = []
    chord_tracker = ""
    for chord in translated_prediction:
        if chord_tracker == "":
            if chord not in ("N","X"):
                chord_tracker = chord
            NX_removed.append(chord_tracker)
        
        else:
            if chord in ("N","X"):
                NX_removed.append(chord_tracker)
            else:
                chord_tracker = chord
                NX_removed.append(chord_tracker)

    np.set_printoptions(threshold=np.inf)
    print("NX_removed: ", NX_removed)
    return np.asarray(NX_removed, dtype=str)


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

def chord_per_beat(NX_removed, index_of_the_beats):
    #takes the intervals of frames between 2 beats and calculates which chord is the most common chord in this beat. 
    print(len(NX_removed))
    print(index_of_the_beats[:10])
    print(index_of_the_beats[-10:])
    print(index_of_the_beats.min(),index_of_the_beats.max())
    print(np.all(np.diff(index_of_the_beats.astype(int)) > 0))
    
    chord_beats= librosa.util.sync(
        data=NX_removed,
        idx=index_of_the_beats.astype(int),
        aggregate=chord_filter, #uses chord_filter to calculate most common and remove 'N' values
        pad=False
    )
    return chord_beats

def bar_structure(interval,**kwargs):
    bar=[]
    last_chord= None
    for chord in interval:
        if chord != last_chord:
            bar.append(chord)
        last_chord = chord

    chord_string = " ".join(bar)
    return chord_string

def chords_into_bars(chord_beats):
    final_chords=[]
    if len(chord_beats) == 0:
        final_chords = "| "
    else:
        chords_array = np.array(chord_beats, dtype='<U8')
        total_beats = len(chord_beats)
        bars = np.arange(0, total_beats, 4)

        chords_bar= librosa.util.sync(
        data=chords_array,
        idx= bars,
        aggregate=bar_structure,
        pad=False
        )
        chords_bar_list = chords_bar.tolist()
        joined_chords_bar = " | ".join(chords_bar_list)
        final_chords = "| " + joined_chords_bar.strip()

    return final_chords


