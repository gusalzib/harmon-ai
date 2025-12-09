
import tensorflow as tf
import librosa
import numpy as np
import collections
from collections import Counter

N = 12
MAJOR = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B", "N", "X"]
MINOR = ["Cm", "C#m", "Dm", "Ebm", "Em", "Fm", "F#m", "Gm", "Abm", "Am", "Bbm", "Bm", "N", "X"]

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
    prediction_with_quality=np.stack((key_prediction, major_minor), axis=1)
    condition = (prediction_with_quality[:,1] == 3)
    result_true = (np.array(MAJOR)[ prediction_with_quality[:,0]])
    result_false = ((np.array(MINOR)[ prediction_with_quality[:,0]]))
    quality_chords = np.where(condition, result_true, result_false)

    
    
    
    
    #[0] 7, [1] none, [2] Major , [3] MINOR?
    
    
 

    #chords = [translate[i] for i in prediction_with_beat]
    #length_of_chords = len(chords)
    #print("CHORDS: ", chords)
    #print("LENGTH OF CHORDS: ",length_of_chords )
    #print("most common in the interval: ")
    
    return quality_chords


