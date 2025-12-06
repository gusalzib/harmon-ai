import os
import pandas as pd
from pandas.api.types import is_numeric_dtype

# ----------------- bothchroma file validation ------------------

# validating if the "bothchroma" file exists.
def validate_bothchroma_exist(path_to_file):
    bothchroma_file = os.path.join(path_to_file, "bothchroma.csv")

    if not os.path.exists(bothchroma_file):
        print(f"The file bothchromas.csv was not found at {bothchroma_file}")
        return None
    else:
        try: 
            df = pd.read_csv(bothchroma_file, header=None, nrows=1)
            return df
        except Exception:
            print(f"Cannot read bothchromas.csv")
            return None

# validating if all the columns are there.
def validate_bothchroma_columns(data_frame):
    if len(data_frame.columns) != 26:
        print(f"Bothchroma dataframe is missing columns")
        return False
    else:
        return True


# validating if there are any nulls 
def is_bothchroma_missing_val(data_frame):
    df_to_check = data_frame.iloc[:, 1:26]
    print("are we getting here?")
    null_count = df_to_check.isnull().sum().sum()
    print(f"Count is: {null_count}")
    if (null_count > 0):
        print(f"Bothchroma dataframe has null values")
        return False
    else:
        print("All good :)")
        return True


# the maximum values returned from data analysis of chromas and timestamps are as follows: 
# chromas min: 0.0, max: 4.45774
# timestamps: min: 0.0, max: 150.883265306
# validating that all values of chromas and timestamps are in range
def is_bothchroma_val_in_range(data_frame):
    min_chroma = 0.0 
    max_chroma = 4.5
    min_timestamp = 0.0
    max_timestamp = 155.0
    df_to_check = data_frame.drop(columns=[0])
    if df_to_check.iloc[:, 2:26].min().min() < min_chroma or df_to_check.loc[:, 2:26].max().max() > max_chroma:
        print(f"There are abnormal chroma values")
        return False
    if df_to_check.iloc[:, 1].min() < min_timestamp or df_to_check.iloc[:, 1].max() > max_timestamp:
        print(f"There are abnormal timestamps values")
        return False
    else: 
        print("All values are in range!)")
        return True
    

def is_bothchroma_numeric_val(data_frame):
    df_to_check = data_frame.drop(columns=[0])
    for col in df_to_check.columns:
        if not pd.api.types.is_numeric_dtype(df_to_check[col]):
            print(f"Failed. there are non-numeric values in col {col}")
            return False
    return True


# ----------------- majmin file validation ------------------

# validating if the "bothchroma" file exists.
def validate_majmin_exist(path_to_file):
    majmin_file = os.path.join(path_to_file, "majmin.lab")

    if not os.path.exists(majmin_file):
        print(f"The file majmin.csv was not found at {majmin_file}")
        return None
    else:
        try: 
            df = pd.read_csv(majmin_file, sep='\t', header=None, nrows=1)
            return df
        except Exception:
            print(f"Cannot read majmin.lab")
            return None

# validating if all the columns are there.
def validate_majmin_columns(data_frame):
    if len(data_frame.columns) != 3:
        print(f"Majmin dataframe is missing columns")
        return False
    else:
        return True

# validating if there are any nulls 
def is_majmin_missing_val(data_frame):
    null_count = data_frame.isnull().sum().sum()
    print(f"Count is: {null_count}")
    if (null_count > 0).any():
        print(f"Majmin dataframe has null values")
        return False
    else:
        print("No missing values")
        return True

def is_majmin_timestamp_numerical(data_frame):
    df_to_check = data_frame.iloc[:, 0:2]
    for col in df_to_check.columns:
        if not pd.api.types.is_numeric_dtype(df_to_check[col]):
            print(f"Failed. there are non-numeric values in col {col}")
            return False
    return True

# the maximum values returned from data analysis of chromas and timestamps are as follows: 
# chromas min: 0.0, max: 4.45774
# timestamps: min: 0.0, max: 150.883265306
# validating that all values of chromas and timestamps are in range
def is_majmin_timestamp_valid(data_frame):
    min_timestamp = 0.0
    max_timestamp = 155.0
    current_ts_start = data_frame.iloc[1:, 0].reset_index(drop=True)
    previous_ts_end = data_frame.iloc[:-1, 1].reset_index(drop=True)
    epsilon = 1e-6
    if (data_frame.iloc[:, 1] < data_frame.iloc[:, 0]).any():
        print(f"timestamp is corrupted")
        return False
    if data_frame.iloc[:, 0:2].min().min() < min_timestamp or data_frame.iloc[:, 0:2].max().max() > max_timestamp:
        print(f"There are abnormal timestamps values: out of range")
        return False

    if (current_ts_start + epsilon < previous_ts_end).any():
        print(f"There are abnormal timestamps values")
        return False
    else: 
        print("all time stamps are valid!!)")
        return True

def is_majmin_chord_string(data_frame):
    if pd.api.types.infer_dtype(data_frame.iloc[1:, 2], skipna=False) != 'string':
        print("Not all values in column 2 are strings")
        return False
    else: 
        print("all values of chords are Strings")
        return True

def does_majmin_have_whitespaces(data_frame):
    if data_frame.iloc[:, 2].str.contains(r'\s', na=False).any():
        print("there are white spaces in chord labels!")
        return False
    else: 
        print("there are no white spaces")
        return True
    
