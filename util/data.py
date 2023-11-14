import pandas as pd
import tensorflow as tf
import tensorflow_io as tfio
import keras


# This class contains informations and method about data loading and dataframes creation
class DataLoader():
    def __init__(self) -> None:
        data_path = "common_dataset/"
        self.audio_path = data_path + "clips/"
        self.metadata_path = data_path + "metadata.csv"

        metadata_df = self.load_data()
        self.split_data(metadata_df)

    def load_data(self) -> None:
        # we need a dataframe to manipulate information
        metadata_df = pd.read_csv(
            self.metadata_path, sep="|", header=0, quoting=3)
        metadata_df.columns = ["client_id", "path", "sentence", "up_votes",
                               "down_votes", "age", "gender", "accents", "locale", "segment"]
        metadata_df = metadata_df[["path", "sentence"]]
        metadata_df = metadata_df.sample(frac=1).reset_index(drop=True)
        return metadata_df

    def split_data(self, metadata_df) -> None:
        # Split the data into training and validation sets
        split = int(len(metadata_df) * 0.80)
        self.df_train = metadata_df[:split]
        self.df_val = metadata_df[split:]

        print(f"Size of the training set: {len(self.df_train)}")
        print(f"Size of the validating set: {len(self.df_val)}")


class DataPrepocessor:
    def __init__(self, frame_length: int, frame_step: int, fft_length: int, audio_path) -> None:

        # Vocabulary Management
        characters = [
            c for c in "abcdefghijklmnopqrstuvwxyzàâéèêëîïôûùçœæ'-,?! "]
        self.char_to_num = keras.layers.StringLookup(
            vocabulary=characters, oov_token="")
        self.num_to_char = keras.layers.StringLookup(
            vocabulary=self.char_to_num.get_vocabulary(), oov_token="", invert=True)

        # Audio Management (MP3) and Spectrogram
        self.frame_length = frame_length
        self.frame_step = frame_step
        self.fft_length = fft_length
        self.audio_path = audio_path

    def process_audio_sample(self, audio_file, label) -> tuple:
        # Process the audio and label

        # Get audio data
        file = tf.io.read_file(self.audio_path + audio_file)
        audio = tfio.audio.decode_mp3(file)
        audio = tf.squeeze(audio, axis=-1)
        audio = tf.cast(audio, tf.float32)

        # Get the spectrogram
        spectrogram = tf.signal.stft(
            audio, frame_length=self.frame_length, frame_step=self.frame_step, fft_length=self.fft_length)
        # we don't use the phase at the moment
        spectrogram = tf.abs(spectrogram)
        spectrogram = tf.math.pow(spectrogram, 0.5)

        # Normalize the spectrogram
        means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
        stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
        spectrogram = (spectrogram - means) / (stddevs + 1e-10)

        # Process the label
        label = tf.strings.lower(label)
        label = tf.strings.unicode_split(label, input_encoding="UTF-8")
        label = self.char_to_num(label)

        # Return label and spectrogram
        return spectrogram, label

    def create_dataset_objets(self, data_loader, batch_size):
        # Define the training dataset
        train_dataset = tf.data.Dataset.from_tensor_slices(
            (list(data_loader.df_train["path"]),
             list(data_loader.df_train["sentence"]))
        )
        train_dataset = (
            train_dataset.map(self.process_audio_sample,
                              num_parallel_calls=tf.data.AUTOTUNE)
            .padded_batch(batch_size)
            .prefetch(buffer_size=tf.data.AUTOTUNE)
        )

        # Define the validation dataset
        validation_dataset = tf.data.Dataset.from_tensor_slices(
            (list(data_loader.df_val["path"]),
             list(data_loader.df_val["sentence"]))
        )
        validation_dataset = (
            validation_dataset.map(self.process_audio_sample,
                                   num_parallel_calls=tf.data.AUTOTUNE)
            .padded_batch(batch_size)
            .prefetch(buffer_size=tf.data.AUTOTUNE)
        )

        return train_dataset, validation_dataset
