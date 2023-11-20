import os
import re
import tempfile
import shutil
import keras
import numpy as np
import tensorflow as tf
from util.data import DataPrepocessor
from util.model import Model

preprocessor = DataPrepocessor(
    frame_length=256, frame_step=160, fft_length=384, audio_path="")
ds_model = Model(input_dim=preprocessor.fft_length//2 + 1,
                 output_dim=preprocessor.char_to_num.vocabulary_size(), rnn_units=512)


def load_model(model_weights="deepspeech_fr_1_10_epochs"):
    print("Model Loaded")
    ds_model.model.load_weights("trainings/"+model_weights)


def list_models():
    sortie = os.listdir("trainings/")
    sortie = [item.split(".")[0] for item in sortie if re.match(
        r'^(?!checkpoint$).*[^index]$', item)]
    return sortie


def recognize_mp3(file):

    try:
        # Save the file to a temporary directory
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        # get prediction of the model
        test_sample, _ = preprocessor.process_audio_sample(file_path, "")
        test_sample = np.expand_dims(test_sample, axis=0)
        pred = ds_model.model.predict(test_sample)

        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        result = keras.backend.ctc_decode(
            pred, input_length=input_len, greedy=True)[0][0]

        result = tf.strings.reduce_join(
            preprocessor.num_to_char(result)).numpy().decode("utf-8")

        print(result)
        return ({'prediction': result}, 200)
    finally:
        # Remove the temporary directory and its contents
        shutil.rmtree(temp_dir, ignore_errors=True)
