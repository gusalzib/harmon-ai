import os
import pandas as pd

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
        print(f"DataFrame is missing columns")
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
        print(f"DataFrame has null values")
        return False
    else:
        print("All good :)")
        return True
    
