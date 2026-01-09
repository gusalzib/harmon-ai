# Authors of code:
# - Muhamad Jawad Ahmad 

# install tqdm for progress bar: pip install tqdm 

import os
import pandas as pd
#from pandas.api.types import is_numeric_dtype
from tqdm import tqdm 

def validate_corresponding(song_dir, chroma_dir, majmin_dir):
    errors_list = []
    
    chordino_path = os.path.join(chroma_dir, song_dir)
    mirex_path = os.path.join(majmin_dir, song_dir)
    
    # Validate bothchroma.csv in chordino folder
    bothchroma_df = validate_bothchroma_exist(chordino_path)
    if bothchroma_df is None:
        errors_list.append(f"{song_dir}: bothchroma.csv missing")
        return False, errors_list
    
    # Validate majmin.lab in mirex folder
    majmin_df = validate_majmin_exist(mirex_path)
    if majmin_df is None:
        errors_list.append(f"{song_dir}: majmin.lab missing")
        return False, errors_list

    if not validate_bothchroma_columns(bothchroma_df):
        errors_list.append(f"Bothchroma of the song {song_dir} is missing columns")
        return False, errors_list

    if not validate_majmin_columns(majmin_df):        
        errors_list.append(f"Majmin of the song {song_dir} is missing columns")
        return False, errors_list
    
    # now that we used the 1 line check for existing and column count, 
    # we can load all the data for checking content
    try:
        bothchroma_full_path = os.path.join(chordino_path, "bothchroma.csv")
        bothchroma_full_df = pd.read_csv(bothchroma_full_path, header=None)

        majmin_full_path = os.path.join(mirex_path, "majmin.lab")
        majmin_full_df = pd.read_csv(majmin_full_path, sep='\t', header=None)
    except Exception:
        errors_list.append(f"error reading full file for song {song_dir}")
        return False, errors_list 
    
    if not is_bothchroma_missing_val(bothchroma_full_df):  
        errors_list.append(f"Bothchroma of the song {song_dir} is missing values or has null values")
        return False, errors_list

    if not is_majmin_missing_val(majmin_full_df):  
        errors_list.append(f"Majmin of the song {song_dir} is missing values or has null values")
        return False, errors_list

    if not is_bothchroma_val_in_range(bothchroma_full_df):
        errors_list.append(f"Bothchroma of the song {song_dir} has out of range values")

    if not is_bothchroma_numeric_val(bothchroma_full_df):
        errors_list.append(f"Bothchroma of the song {song_dir} has non-numeric values")

    if not is_majmin_timestamp_numerical(majmin_full_df):
        errors_list.append(f"Majmin of the song {song_dir} has non-numeric timestamps")

    if not is_majmin_timestamp_valid(majmin_full_df):
        errors_list.append(f"Majmin of the song {song_dir} has invalid timestamps") 

    if not is_majmin_chord_string(majmin_full_df):
        errors_list.append(f"Majmin chords of the song {song_dir} is not of type string")

    if not does_majmin_have_whitespaces(majmin_full_df):
        errors_list.append(f"Majmin chords of the song {song_dir} has white spaces")

    if not is_majmin_format_correct(majmin_full_df):
        errors_list.append(f"Majmin chords of the song {song_dir} are incorrectly formatted")
    
    if (len(errors_list) == 0): # no errors detected 
        valid = True
    else:  # there were some errors 
        valid = False
    
    return valid, errors_list

def validate_dataset(chroma_path, majmin_path):
    # Get common song folders
    chroma_subdirs = {f for f in os.listdir(chroma_path)
                    if os.path.isdir(os.path.join(chroma_path, f)) and not f.startswith('.')}
    majmin_subdirs = {f for f in os.listdir(majmin_path)
                 if os.path.isdir(os.path.join(majmin_path, f)) and not f.startswith('.')}
    # all_subdirs = chroma_subdirs | majmin_subdirs
    common_subdirs = chroma_subdirs & majmin_subdirs
    missing_majmin_subdirs = chroma_subdirs - majmin_subdirs
    missing_chroma_subdirs = majmin_subdirs - chroma_subdirs
    
    results = {}
    for song_dir in missing_chroma_subdirs:
        results[song_dir] = (False, [f"Song missing in chordino {song_dir}"])

    for song_dir in missing_majmin_subdirs: 
        results[song_dir] = (False, [f"Song missing in mirex {song_dir}"])    
    # using taqaddom to display progress with the validation
    for song_dir in tqdm(common_subdirs, desc="Validating", unit="song"):
        results[song_dir] = validate_corresponding(song_dir, chroma_path, majmin_path)    
    
    return results

# ----------------- bothchroma file validation ------------------
# validating if the "bothchroma" file exists.
def validate_bothchroma_exist(path_to_file):
    bothchroma_file = os.path.join(path_to_file, "bothchroma.csv")

    if not os.path.exists(bothchroma_file):
        # print(f"The file bothchromas.csv was not found at {bothchroma_file}")
        return None
    else:
        try: 
            df = pd.read_csv(bothchroma_file, header=None, nrows=1)
            return df
        except Exception:
            # print(f"Cannot read bothchromas.csv")
            return None

# validating if all the columns are there.
def validate_bothchroma_columns(data_frame):
    if len(data_frame.columns) != 26:
        # print(f"Bothchroma dataframe is missing columns")
        return False
    else:
        return True


# validating if there are any nulls 
def is_bothchroma_missing_val(data_frame):
    df_to_check = data_frame.iloc[:, 1:26]
    # print("are we getting here?")
    null_count = df_to_check.isnull().sum().sum()
    # print(f"Count is: {null_count}")
    if (null_count > 0):
        # print(f"Bothchroma dataframe has null values")
        return False
    else:
        # print("All good :)")
        return True


# the maximum values returned from data analysis of chromas and timestamps are as follows: 
# chromas min: 0.0, max: 4.86386
# timestamps: min: 0.0, max: 702.275918367 seconds 
# validating that all values of chromas and timestamps are in range
def is_bothchroma_val_in_range(data_frame):
    min_chroma = 0.0 
    max_chroma = 10.0
    min_timestamp = 0.0
    max_timestamp = 800.0
    df_to_check = data_frame.drop(columns=[0])
    if df_to_check.iloc[:, 2:26].min().min() < min_chroma or df_to_check.iloc[:, 2:26].max().max() > max_chroma:
        # print(f"There are abnormal chroma values")
        return False
    if df_to_check.iloc[:, 1].min() < min_timestamp or df_to_check.iloc[:, 1].max() > max_timestamp:
        # print(f"There are abnormal timestamps values")
        return False
    else: 
        # print("All values are in range!)")
        return True
    

def is_bothchroma_numeric_val(data_frame):
    df_to_check = data_frame.drop(columns=[0])
    for col in df_to_check.columns:
        if not pd.api.types.is_numeric_dtype(df_to_check[col]):
            # print(f"Failed. there are non-numeric values in col {col}")
            return False
    return True


# ----------------- majmin file validation ------------------

# validating if the "bothchroma" file exists.
def validate_majmin_exist(path_to_file):
    majmin_file = os.path.join(path_to_file, "majmin.lab")

    if not os.path.exists(majmin_file):
        # print(f"The file majmin.csv was not found at {majmin_file}")
        return None
    else:
        try: 
            df = pd.read_csv(majmin_file, sep='\t', header=None, nrows=1)
            return df
        except Exception:
            # print(f"Cannot read majmin.lab")
            return None

# validating if all the columns are there.
def validate_majmin_columns(data_frame):
    if len(data_frame.columns) != 3:
        # print(f"Majmin dataframe is missing columns")
        return False
    else:
        return True

# validating if there are any nulls 
def is_majmin_missing_val(data_frame):
    null_count = data_frame.isnull().sum().sum()
    # print(f"Count is: {null_count}")
    if (null_count > 0):
        # print(f"Majmin dataframe has null values")
        return False
    else:
        # print("No missing values")
        return True

def is_majmin_timestamp_numerical(data_frame):
    df_to_check = data_frame.iloc[:, 0:2]
    for col in df_to_check.columns:
        if not pd.api.types.is_numeric_dtype(df_to_check[col]):
            # print(f"Failed. there are non-numeric values in col {col}")
            return False
    return True

# the maximum values returned from data analysis of chromas and timestamps are as follows: 
# chromas min: 0.0, max: 4.86386
# timestamps: min: 0.0, max: 702.275918367 seconds 
# validating that all values of chromas and timestamps are in range
def is_majmin_timestamp_valid(data_frame):
    min_timestamp = 0.0
    max_timestamp = 800.0
    current_ts_start = data_frame.iloc[1:, 0].reset_index(drop=True)
    previous_ts_end = data_frame.iloc[:-1, 1].reset_index(drop=True)
    epsilon = 1e-6
    if (data_frame.iloc[:, 1] < data_frame.iloc[:, 0]).any():
        # print(f"timestamp is corrupted")
        return False
    if data_frame.iloc[:, 0:2].min().min() < min_timestamp or data_frame.iloc[:, 0:2].max().max() > max_timestamp:
        # print(f"There are abnormal timestamps values: out of range")
        return False

    if (current_ts_start + epsilon < previous_ts_end).any():
        # print(f"There are abnormal timestamps values")
        return False
    else: 
        # print("all time stamps are valid!!)")
        return True

def is_majmin_chord_string(data_frame):
    if pd.api.types.infer_dtype(data_frame.iloc[1:, 2], skipna=False) != 'string':
        # print("Not all values in column 2 are strings")
        return False
    else: 
        # print("all values of chords are Strings")
        return True

def does_majmin_have_whitespaces(data_frame):
    if data_frame.iloc[:, 2].str.contains(r'\s', na=False).any():
        # print("there are white spaces in chord labels!")
        return False
    else: 
        # print("there are no white spaces")
        return True

def is_majmin_format_correct(data_frame):
    chord_key = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 
                 'B', 'Db', 'Eb', 'Gb', 'Ab', 'Bb', 'Cb', 'Fb']
    no_key_labels = ['X', 'N']
    chord_quality = ['maj', 'min']

    label_column = data_frame.iloc[:, 2]

    excludable = label_column.isin(no_key_labels)
    
    chords_to_check = label_column[~excludable]
    if chords_to_check.empty:
        # print("Note: labels are all either N or X")
        return True 
    
    if not chords_to_check.str.contains(':', na=False).all():
        # print("Some chord labels are incorrectly formatted")
        return False
    
    split_chords = chords_to_check.str.split(':', expand=True)
    if split_chords.shape[1] != 2:
        # print("Some chord labels are incorrectly formatted")
        return False
        
    valid_key = split_chords.iloc[:, 0].isin(chord_key)
    valid_quality = split_chords.iloc[:, 1].isin(chord_quality)

    if (valid_key & valid_quality).all():
        # print("chords correctly formatted")
        return True
    else: 
        # print("invalid labels found")
        return False
