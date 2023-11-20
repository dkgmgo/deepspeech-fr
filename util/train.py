import tensorflow as tf
import keras
import numpy as np
from jiwer import wer
from time import time


# Here we have our trainer, decoder and the different callbacks
class Trainer:
    def __init__(self, model, train_dataset, validation_dataset, preprocessor):
        self.model = model
        self.train_dataset = train_dataset
        self.validation_dataset = validation_dataset
        self.preprocessor = preprocessor

    def decode_batch_predictions(self, pred):
        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        results = keras.backend.ctc_decode(
            pred, input_length=input_len, greedy=True)[0][0]
        # Iterate over the results and get back the text
        output_text = []
        for result in results:
            result = tf.strings.reduce_join(
                self.preprocessor.num_to_char(result)).numpy().decode("utf-8")
            output_text.append(result)
        return output_text

    def train(self, epochs, save_every_n_hours):
        # Callbacks
        validation_callback = CallbackEval(self)
        saver_callback = CallbackSave(self, save_every_n_hours)

        # Train the model
        history = self.model.fit(
            self.train_dataset,
            validation_data=self.validation_dataset,
            epochs=epochs,
            callbacks=[validation_callback, saver_callback],
        )


# A callback class to output a few transcriptions during training
class CallbackEval(keras.callbacks.Callback):
    """Displays a batch of outputs after every epoch."""

    def __init__(self, trainer):
        super().__init__()
        self.trainer = trainer

    def on_epoch_end(self, epoch: int, logs=None):
        predictions = []
        targets = []
        for batch in self.trainer.validation_dataset:
            X, y = batch
            batch_predictions = self.trainer.model.predict(X)
            batch_predictions = self.trainer.decode_batch_predictions(
                batch_predictions)
            predictions.extend(batch_predictions)
            for label in y:
                label = (
                    tf.strings.reduce_join(self.trainer.preprocessor.num_to_char(
                        label)).numpy().decode("utf-8")
                )
                targets.append(label)
        wer_score = wer(targets, predictions)
        print("-" * 100)
        print(f"Word Error Rate: {wer_score:.4f}")
        print("-" * 100)
        for i in np.random.randint(0, len(predictions), 2):
            print(f"Target    : {targets[i]}")
            print(f"Prediction: {predictions[i]}")
            print("-" * 100)


# A callback class to save the model periodically during the training
class CallbackSave(keras.callbacks.Callback):
    """Saves the model peridically"""

    def __init__(self, trainer, save_every_n_hours=2):
        super().__init__()
        self.trainer = trainer
        self.checkpoint_dir = 'trainings/'
        self.save_every_n_seconds = save_every_n_hours * 3600  # Convert hours to seconds
        self.last_save_time = 0

    def on_batch_end(self, batch, logs=None):
        current_time = time()
        if current_time - self.last_save_time >= self.save_every_n_seconds:
            self.save_model()
            self.last_save_time = current_time

    def save_model(self):
        date_time = tf.keras.backend.get_value(tf.timestamp())
        path = self.checkpoint_dir + f'deepspeech_fr_{date_time}'
        self.trainer.model.save_weights(path)
        print(f"Model checkpoint saved to {path}")
