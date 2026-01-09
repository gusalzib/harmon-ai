# Authors of code:
# Rebecka Åkerblom - gusakerre@sudent.gu.se - rebake@chalmers.se 

from django import forms
import os
from google.cloud import storage
import numpy as np
import io

#Updated to not save the splitted audio in a file and later delete it. 
#Now we use it instantly and then it is gone
def separate_audio(waveform, separator, stems):
    #flip the waveform
    waveform_T = waveform.T
    
    separated = separator.separate(waveform_T)
    if stems==2:
        prosessed_audio = separated["accompaniment"]
        mono_audio = np.mean(prosessed_audio,axis=1)
        return mono_audio
    else:
        print("start splitting")
        prosessed_audio = separated["other"]
        print("first")
        percussive_audio = separated["drums"]
        print("second")
        mono_audio = np.mean(prosessed_audio,axis=1)
        print("third")
        mono_percussive = np.mean(percussive_audio,axis=1)
        print("splitting is done")
        return mono_audio, mono_percussive


    



def download_model_from_google(BUCKET_NAME, BASE_MODEL_PATH, MODEL_NAME):
    model_path = f"{BASE_MODEL_PATH}/{MODEL_NAME}/serving"
    local_dir = f"/tmp/{MODEL_NAME}"

    os.makedirs(local_dir, exist_ok=True)

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    found_any = False
    for blob in bucket.list_blobs(prefix=model_path):
        if blob.name.endswith("/"):
            continue
        found_any = True

        rel_path = blob.name[len(model_path):].lstrip("/")
        dst_path = os.path.join(local_dir, rel_path)

        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        blob.download_to_filename(dst_path)

    if not found_any:
        raise RuntimeError(f"No files found in google cloud at : {BUCKET_NAME}/{model_path}")

    return local_dir

