import os
import pandas as pd

# validating if the "bothchroma" file exists.

def validate_bothchroma_exist(path_to_file):
    bothchroma_file = os.path.join(path_to_file, "bothchroma.csv")

    if not os.path.exists(bothchroma_file):
        print(f"The file bothchromas.csv was not found at {bothchroma_file}")
        return False
    else:
        try: 
            df = pd.read_csv(bothchroma_file, header=None, nrows=1)
            return True
        except Exception:
            print(f"Cannot read bothchromas.csv")
            return False