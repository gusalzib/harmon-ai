# Authors of code:
# -

import pandas as pd
import sqlite3
import os
from sklearn.preprocessing import LabelEncoder


all_possible_keys = [
    "N", "X", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
]

all_possible_qualities = [
    "None", "min", "maj", "7"
]

tones_normalized_equiv = {
    # Flat notes
    "Cb": "B",
    "Db": "C#",
    "Eb": "D#",
    "Fb": "E",
    "Gb": "F#",
    "Ab": "G#",
    "Bb": "A#"
    # Maybe Sharp notes too for future data updates
}

def equalize_tone(tone):
    if tone in tones_normalized_equiv:
        return tones_normalized_equiv[tone]
    else:
        return tone

def build_sqlite_from_dataset(dataset_version,combined_path, valid_songs, database_name="billboard_data.db", chunksize=1000):
    
    print(f"\nProcessing {len(valid_songs)} songs...")

    key_encoder = LabelEncoder()
    key_encoder.fit(all_possible_keys)

    quality_encoder = LabelEncoder()
    quality_encoder.fit(all_possible_qualities)
    
    # setting up the database
    conn = sqlite3.connect(database_name)
    total_rows = 0
    
    # looping through songs
    for record, song_dir in enumerate(valid_songs):
        song_path = os.path.join(combined_path, song_dir)
        
        if not os.path.exists(song_path):
            print(f"  Skipping {song_dir} (not found)")
            continue
        
        # Progress indicator, not too frequently printing, to avoid slowing down and cluttering the terminal
        if record % 50 == 0 and record > 0:
            print(f" * Processed {record} songs...")
        
        try:

            chroma_cols = ['filepath', 'timestamp'] + [f'chroma_{i}' for i in range(24)]
            df_chroma = pd.read_csv(
                os.path.join(song_path, "bothchroma.csv"), 
                header=None, 
                names=chroma_cols
            )
            df_chroma = df_chroma.drop(columns=['filepath'])

            # loading the labels
            df_labels = pd.read_csv(
                os.path.join(song_path, "majmin.lab"), 
                sep='\t', 
                header=None, 
                names=['start_time', 'end_time', 'chord']
            )

            df_merged = pd.merge_asof(
                df_chroma, 
                df_labels, 
                left_on='timestamp', 
                right_on='start_time',
                direction='backward'
            )
            
            df_aligned = df_merged[df_merged['timestamp'] < df_merged['end_time']].copy()
            
            if len(df_aligned) == 0:
                continue
            

            df_aligned[["key", "quality"]] = ["X", "None"]
            
            if df_aligned["chord"].str.contains(":", na=False).any():
                df_aligned[["key", "quality"]] = df_aligned["chord"].str.split(":", n=1, expand=True)
            else:
                df_aligned["key"] = df_aligned["chord"]
            

            df_aligned["key"] = df_aligned["key"].apply(equalize_tone)
            
            # encoding 
            df_aligned["key"] = key_encoder.transform(df_aligned["key"])
            df_aligned["quality"] = quality_encoder.transform(df_aligned["quality"])
            
            df_aligned = df_aligned.drop(columns=['start_time', 'end_time', 'chord'])
            
            song_rows = len(df_aligned)
            
            if_table_exists = 'replace' if total_rows == 0 else 'append'
            
            df_aligned.to_sql(
                'training_data_v'+str(dataset_version), 
                conn, 
                if_exists=if_table_exists, 
                index=False,
                chunksize=chunksize
            )
            
            total_rows += song_rows
            
        except Exception as e:
            print(f"Error encountered while processing {song_dir}")
            continue
    
    conn.close()
    
    print(f"\nComplete dataset: {total_rows:,} rows in {database_name}")
    return database_name