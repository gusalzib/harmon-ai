
import tensorflow as tf
import librosa
import numpy as np
import collections
from collections import Counter

N = 12

def predict(chroma_T, model):
    # features = np.array(chromagram, dtype=np.float32)
    features= tf.constant(chroma_T, dtype=tf.float32)
    result = model(features)
    key=result['key_probs'].numpy()
    quality=result['quality_probs'].numpy()
    key_predictions=np.argmax(key,axis=1)
    major_minor = np.argmax(quality,axis=1)
    
    return key_predictions,major_minor

def prediction_into_chords(key_prediction, index_of_the_beats, major_minor):
    prediction_with_beat = []
    chords = []
    indices = index_of_the_beats.astype(int)
    print("DUR MOLL: ", major_minor)
    #[0] major, [1] minor, [2] 'N', [3] 7?
    #prediction_intervals =key_prediction[start_frame:end_frame]
    for i in range(len(indices)-1):
        start_frame = indices[i]
        end_frame = indices[i+1]
        prediction_intervals =key_prediction[start_frame:end_frame]
        if len(prediction_intervals) > 0:
            #counter = Counter(prediction_intervals)

            #most_common_prediction=counter.most_common()
            counts = collections.Counter(prediction_intervals).most_common()
            most_common_index = counts[0][0]

            if most_common_index == N:
                fallback_index = None
                for label_index, label_count in counts:
                    if label_index < N:
                        fallback_index = label_index
                        break
                if fallback_index is not None:
                    final_index = fallback_index
                else:
                    final_index = most_common_index
                
                prediction_with_beat.append(final_index)


    translate =["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "N", "X"]
    #translate = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "N", "X"]
    
    chords = [translate[i] for i in prediction_with_beat]
    length_of_chords = len(chords)
    print("CHORDS: ", chords)
    print("LENGTH OF CHORDS: ",length_of_chords )
    print("most common in the interval: ")
    
    return chords


