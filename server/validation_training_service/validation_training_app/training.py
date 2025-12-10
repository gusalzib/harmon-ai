import os 
from dotenv import load_dotenv
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



def build_model():
    inputs = Input(shape= (TIMEFRAME,12))
    output = layers.GaussianNoise(0.05)(inputs)
    output = layers.Conv1D(filters=32, kernel_size=3,strides=1,padding='same',activation='relu')(output)
    output = layers.BatchNormalization()(output)
    output = layers.Conv1D(64, kernel_size=5, padding='same', activation='relu')(output)
    output = layers.BatchNormalization()(output)
    output = layers.MaxPooling1D(pool_size=2)(output)
    output = layers.Dropout(0.4)(output)
    output = layers.Bidirectional(layers.GRU(32, return_sequences=True, dropout=0.3, unroll=True))(output)
    output = layers.Bidirectional(layers.GRU(64, return_sequences=False, dropout=0.3, unroll=True))(output)
    output = layers.Dropout(0.4)(output)


    keyInput= layers.Dense(128,activation='relu')(output)
    key= layers.Dense(14,activation= 'softmax',name='key',kernel_regularizer=regularizers.l2(0.001))(keyInput)

    shapeInput = layers.Dense(64,activation='relu')(output)
    quality = layers.Dense(4,activation='softmax',name='quality',kernel_regularizer=regularizers.l2(0.001))(shapeInput)

    model3x = models.Model(inputs=inputs, outputs = [key, quality])
    model3x.compile(optimizer=Adam(learning_rate=0.001),
                  loss= 'sparse_categorical_crossentropy',
                  metrics=['accuracy'],
                  )
    return model3x



def train_model(model, train_dataset, val_dataset):
    
     

    lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', 
        factor=0.2,       # Reduce LR by 5x (multiply by 0.2)
        patience=2,       # Wait 2 epochs with no improvement
        min_lr=0.00001,   # Don't go below this
        verbose=1
    )

    model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=10,
        callbacks = [
            tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True), lr_scheduler
        ]
    )


def evaluate_model(model, test_dataset):
    model.evaluate(test_dataset)

    return


    
def save_serving_model(model, path):

    #wrapp model so that we can save it with preprocessing steps included
    class ModelWrapper(tf.Module):

        def __init__(self, keras_model, timeframe=30):
            super().__init__()
            self.keras_model = keras_model
            self.timeframe = timeframe

        @tf.function(input_signature=[tf.TensorSpec(shape=[None, 12], dtype=tf.float32)])

        def __call__(self, features):
            # 1. Create Padding (Repeat the first row 39 times)
            # We take features[0], expand dims to (1, 24), and tile it
            first_frame = tf.expand_dims(features[0], 0)
            padding = tf.tile(first_frame, [self.timeframe - 1, 1])

            # 2. Stick padding on top
            padded_features = tf.concat([padding, features], axis=0)

            # 3. Frame it
            windows = tf.signal.frame(padded_features, frame_length=self.timeframe, frame_step=1, axis=0)

            # 4. Predict
            predictions = self.keras_model(windows)

            return {"key_probs": predictions[0], "quality_probs": predictions[1]}
   

    model.optimizer = None
    model.compiled_loss = None
    model.compiled_metrics = None
    wrapped_model = ModelWrapper(model, timeframe=TIMEFRAME)

    tf.saved_model.save(
        wrapped_model,
        path,
        signatures={'serving_default': wrapped_model.__call__}
    )


def save_model_for_tfma(model, save_path):


    @tf.function(input_signature=[tf.TensorSpec(shape=[None], dtype=tf.string)])
    def TMFA_serving(tf_record):
        features = {'features': tf.io.fixedLenFeature([TIMEFRAME * 12], out_type=tf.float32)}

        parsed_features = tf.io.parse_example(tf_record, features)

        reshaped_input = tf.reshape(parsed_features['features'], [-1, TIMEFRAME, 12])

        predictions = model(reshaped_input)


    model.save(
    save_path,
    signatures={'serving_default': TMFA_serving}
)
                 
