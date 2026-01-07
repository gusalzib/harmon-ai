# Authors of code:
# - 

import os 
from dotenv import load_dotenv
from google.cloud import storage
import pandas as pd 
import numpy as np
import tensorflow as tf
import keras 
from keras import layers, models, Input
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from tensorflow.keras import regularizers
import sqlite3


TIMEFRAME = 30
BATCH_SIZE = 64
STRIDE = 5

def load_data():#should be given path as imput
    """
    Downloads the database file from Google Cloud Storage, loads the data into a
    pandas DataFrame, and then cleans up the downloaded file.
    """
    ####rename once we have upload and validation###
    bucket_name = "harmon_ai"
    source_blob_name = "data/clean_data/training_data_v0.db" ###should be path_to_data, we could store the sql in a temp file or get it from GCS
    destination_file_name = "/tmp/training_data"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    # download the clean sql dataset
    blob.download_to_filename(destination_file_name)
    # connect to the sqlite dataset 
    conn = sqlite3.connect(destination_file_name)
    try:
        dataset = pd.read_sql("SELECT * FROM training_data_v0", conn)
    finally:
        # Close the connection
        conn.close()
        # remove the sql dataset since we now have it as a pandas dataframe
        os.remove(destination_file_name)

    return dataset

def merge_chroma_bins(df):
    """
    Takes a dataframe with 24 columns.
    Adds the Bass (0-11) and Treble (12-23) bins together.
    Returns a dataframe with 12 columns.
    """
    # Slice the first 12 (Bass) and last 12 (Treble)
    bass = df.iloc[:, 0:12]
    treble = df.iloc[:, 12:24]

    # Sum them together. 
    # We use .values on treble to ignore column name mismatches
    merged_val = bass.values + treble.values

    #normalize the dataset so that it resembels output from librosa audioprocessing
    max_vals = np.max(merged_val, axis=1, keepdims=True)
    normalized_values = merged_val / (max_vals + 1e-9) # add a tiny number to avoid dividing by zero
    return pd.DataFrame(normalized_values, index=df.index)

def create_timeseries_dataset(dataset, sequence_length, stride,shuffle=False, is_y_data=False):
    """
    Creates a tf.keras.utils.timeseries_dataset_from_array from the given input.
    If `is_y_data` is True, it shifts the data by `TIMEFRAME - 1` steps. This is
    done for target data (y) to align it with the corresponding feature data (x),
    ensuring that each input sequence is mapped to the correct label from the end
    of its time window.
    """
    if is_y_data:
        # For target data (y), we shift it to align with the end of the input sequence.
        dataset = dataset[TIMEFRAME - 1:]

    #since the dataset becomes TIMEFRAME times bigger storing it as a reagular dataframe becomes to big
    dataset = tf.keras.utils.timeseries_dataset_from_array(
        data=dataset,
        targets=None,
        sequence_length=sequence_length,
        sequence_stride=stride,
        shuffle=shuffle,
        batch_size=BATCH_SIZE,
        seed = 42
    )
    return dataset


def y_mapping_reshaped(x, y_key, y_qual):
    # Squeeze removes the time dimension from Y since it's just 1 step now
    return x, {'key': tf.squeeze(y_key, axis=1), 'quality': tf.squeeze(y_qual, axis=1)}

#
def zip_and_map(x,key,quality):
    """
    Combines feature, key, and quality datasets into a single dataset formatted for
    the multi-output Keras model. Applies reshaping and prefetching.
    """
    dataset =tf.data.Dataset.zip((x, key, quality))
    dataset_mapped = dataset.map(y_mapping_reshaped, num_parallel_calls=tf.data.AUTOTUNE).prefetch(tf.data.AUTOTUNE)
    return dataset_mapped



def create_test_train_validationset(dataset):
    # divide the dataset into training and test data 80/20 split
    n_samples = len(dataset)
    train_end = int(0.80 * n_samples)
    #drop "ground-truth" for the x data
    x_data = dataset.drop(columns=['key','quality','timestamp'])
    key_data = dataset['key']
    quality_data = dataset['quality']
    #normalize and make the chroma more like the mcgill dataset
    x_data = merge_chroma_bins(x_data)

    train_x = x_data[:train_end]
    train_key = key_data[:train_end]
    train_quality = quality_data[:train_end]
    
    test_x = x_data[train_end:]
    test_key = key_data[train_end:]
    test_quality = quality_data[train_end:]

    #split training data into training and validation data 75/15
    x_train, x_val, key_train, key_val, y_quality_train, y_quality_val = train_test_split(train_x, 
    train_key, 
    train_quality, 
    test_size=0.15, 
    shuffle=False)

    #create timeseries datasets eg datasets wtih sliding windows
    x_train= create_timeseries_dataset(x_train, TIMEFRAME, STRIDE, shuffle=True)
    x_val = create_timeseries_dataset(x_val, TIMEFRAME, STRIDE, shuffle=False)
    x_test = create_timeseries_dataset(test_x, TIMEFRAME, STRIDE, shuffle=False)

    key_train =create_timeseries_dataset(key_train, 1, STRIDE, shuffle=True, is_y_data=True)
    key_val = create_timeseries_dataset(key_val, 1, STRIDE, shuffle=False, is_y_data=True)
    key_test = create_timeseries_dataset(test_key, 1, STRIDE, shuffle=False, is_y_data=True)

    quality_train =create_timeseries_dataset(y_quality_train, 1, STRIDE, shuffle=True, is_y_data=True)
    quality_val = create_timeseries_dataset(y_quality_val, 1, STRIDE, shuffle=False, is_y_data=True)
    quality_test = create_timeseries_dataset(test_quality, 1, STRIDE, shuffle=False, is_y_data=True)

    train_dataset = zip_and_map(x_train, key_train, quality_train)
    val_dataset = zip_and_map(x_val, key_val, quality_val)
    test_dataset = zip_and_map(x_test, key_test, quality_test)

    return train_dataset, val_dataset, test_dataset

KEY_MAP = {
        0: "A",
        1: "A#",
        2: "B",
        3: "C",
        4: "C#",
        5: "D",
        6: "D#",
        7: "E",
        8: "F",
        9: "F#",
        10: "G",
        11: "G#",
        12: "N",
        13: "X"
    }

def save_testdata_to_tfrecord(output_path,test_dataset):
    """
    Generates the validation set and writes it to a TFRecord file
    formatted specifically for TFMA analysis.
    """     
    # 2. Ensure directory exists, using tf.io.gfile to support GCS paths
    tf.io.gfile.makedirs(os.path.dirname(output_path))

    # 3. Write to TFRecord
    with tf.io.TFRecordWriter(output_path) as writer:
        # Unbatch ensures we process one window (30x12) at a time
        for x, y in test_dataset.unbatch():
            
            # Flatten the window: (30, 12) -> (360,)
            # We must convert to list for it to work with the Protobuf format
            features_flat = tf.reshape(x, [-1]).numpy().tolist()
            
            # Extract 
            key_label = int(y['key'].numpy())
            quality_label = int(y['quality'].numpy())
            
            slice_key_str = KEY_MAP.get(key_label, str(key_label))
            slice_quality_str = str(quality_label)

            # Create the serialized Example
            example = tf.train.Example(features=tf.train.Features(feature={
                'features': tf.train.Feature(float_list=tf.train.FloatList(value=features_flat)),
                'key_label': tf.train.Feature(int64_list=tf.train.Int64List(value=[key_label])),
                'quality_label': tf.train.Feature(int64_list=tf.train.Int64List(value=[quality_label])),
                # Slice key for filtering in the dashboard
                'slice_key': tf.train.Feature(bytes_list=tf.train.BytesList(value=[slice_key_str.encode('utf-8')])),
                # Slice quality for filtering in the dashboard
                'slice_quality': tf.train.Feature(bytes_list=tf.train.BytesList(value=[slice_quality_str.encode('utf-8')]))
            }))
            
            writer.write(example.SerializeToString())
            
    print("TFRecord export complete.")   