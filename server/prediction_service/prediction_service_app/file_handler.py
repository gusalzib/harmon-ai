from django import forms
import os

#save audio in a folder

def separate_audio(audio, separator, stems):

    temp_audio_folder = "./prediction_service_app/temp_audio"
    temp_output_folder = "./prediction_service_app/temp_output"
    
    output_folder_name = os.path.splitext(audio.name)[0]
    audio_file_path= os.path.join(temp_audio_folder, audio.name)
    with open(audio_file_path, "wb+") as destination:
        for chunk in audio.chunks():
            destination.write(chunk)

    temp_output_folder = "./prediction_service_app/temp_output"
    separator.separate_to_file(audio_file_path, temp_output_folder)
    
    
    if stems == 2:
        prosessed_audio = os.path.join(temp_output_folder,output_folder_name,"accompaniment.wav")
    else:
        prosessed_audio = os.path.join(temp_output_folder,output_folder_name,"other.wav")
    
    return(audio_file_path, output_folder_name, prosessed_audio)


def delete_audio_2_stems(audio_file_path, output_folder_name):
    #remove file in temp_audio
    os.remove(audio_file_path)

    output_folder_path = os.path.join("./prediction_service_app/temp_output", output_folder_name)

    #remove files in the output_folder
    accompaniment_path = os.path.join(output_folder_path,"accompaniment.wav")
    vocals_path = os.path.join(output_folder_path,"vocals.wav")
    os.remove(accompaniment_path)
    os.remove(vocals_path)

    #remove folder in temp_output
    os.rmdir(output_folder_path)

    return "audio deleted" 

def delete_audio_4_stems(audio_file_path, output_folder_name):
    #remove file in temp_audio
    os.remove(audio_file_path)

    output_folder_path = os.path.join("./prediction_service_app/temp_output", output_folder_name)

    #remove files in the output_folder
    bass_path = os.path.join(output_folder_path,"bass.wav")
    drums_path = os.path.join(output_folder_path,"drums.wav")
    other_path = os.path.join(output_folder_path,"other.wav")
    vocals_path = os.path.join(output_folder_path,"vocals.wav")
    os.remove(bass_path)
    os.remove(drums_path)
    os.remove(other_path)
    os.remove(vocals_path)

    #remove folder in temp_output
    os.rmdir(output_folder_path)

    return "audio deleted" 
