import pandas as pd
import sqlite3
import os
import pandas.testing as tm

# defining a validation function to guarantee that
# sqlite db matches csv file via dataframe comparison
def validate_db_match(csv_p, sqlite_p):
    print("Starting csv to sqlite database verification...")
    df_csv = pd.read_csv(csv_p)
    conn = sqlite3.connect(sqlite_p)
    df_db = pd.read_sql("SELECT * FROM training_data_v0", conn)
    conn.close()

    try:
        tm.assert_frame_equal(df_csv, df_db)
        print("\nThe database is the same as the CSV.")
    except AssertionError as err:
        print("\nError: data-fames are not the same")
        print(err)    


# Pathing to current "cleaned_data" and new sqlite db to be generated
# Please place the cleaned_data.csv in the same directory as this file to process directly 
# sql db will be generated in the same directory
csv_path = 'cleaned_data.csv'
sqlite_path = 'cleaned_data.db'
chunksize = 1000
chunk_count = 0

conn = sqlite3.connect(sqlite_path)

print("starting csv to sqlite transformation!")

for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunksize)):
    chunk_count = chunk_count + 1
    # make sure if there are previous entries, append instead of replace
    chunk.to_sql('training_data_v0', conn, if_exists='append', index=False)

print(f"Saved to an sqlite db! \nThe number of chunks was {chunk_count}")
# calling dataframes match validation
validate_db_match(csv_path, sqlite_path)

conn.close()
print("SQLite DB is ready!")