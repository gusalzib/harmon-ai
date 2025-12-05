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
    df_to_check = data_frame.drop(columns=[0])
    print("are we getting here?")
    null_count = df_to_check.isnull().sum().sum()
    print(f"Count is: {null_count}")
    if (null_count > 0).any():
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
        print("All good :)")
        return True
