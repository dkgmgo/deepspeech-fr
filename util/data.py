import pandas as pd
import tensorflow as tf
import keras

# TODO
class DataLoader():
    def __init__(self) -> None:
        data_path = "commond_dataset/"
        self.audio_path = data_path + "/audio/"
        self.metadata_path = data_path + "/validated.csv"
        print(self.metadata_path)


        metadata_df = self.load_data()  # save the result in metadata_df
        self.split_data(metadata_df)    # from  metadata_df to split_data


    def load_data(self) -> None:
        #we need a dataframe to manipulate information
        metadata_df = pd.read_csv(self.metadata_path, sep="|", header=None, quoting=3)
        metadata_df.columns = ["client_id", "path", "sentence", "up_votes", "down_votes", "age", "gender", "accents", "locale", "segment"]
        metadata_df = metadata_df[["path", "sentence"]]
        metadata_df = metadata_df.sample(frac=1).reset_index(drop=True)
        return(metadata_df)

        pass

    def split_data(self, metadata_df) -> None:
        # Split the data into training and validation sets
        split = int(len(metadata_df) * 0.80)
        df_train = metadata_df[:split]
        df_val = metadata_df[split:]

        print(f"Size of the training set: {len(df_train)}")
        print(f"Size of the validating set: {len(df_val)}")


class DataPrepocessor:
    def __init__(self, frame_length: int, frame_step: int, fft_length: int, audio_path) -> None:
        
        # Vocabulary Management
        characters = [c for c in "abcdefghijklmnopqrstuvwxyz'àâéèêëîïôûùçœæ-?! "]
        self.char_to_num = keras.layers.StringLookup(vocabulary=characters, oov_token="")
        self.num_to_char = keras.layers.StringLookup(vocabulary=self.char_to_num.get_vocabulary(), oov_token="", invert=True)

        # Audio Management (MP3) and Spectrogram 
        self.frame_length = frame_length
        self.frame_step = frame_step
        self.fft_length = fft_length
        self.audio_path = audio_path

    def process_audio_sample(self, audio_file, label) -> tuple:
        # Process the audio and label
        # 1. Find a mp3 file in the mp3 folder
        file = tf.io.read_file(self.audio_path + audio_file + ".mp3")

        # 2. Decode the audio
        audio = tf.audio.decode_mp3(file)
        audio = tf.squeeze(audio, axis=-1)
        
        # 3. Put the audio in float32
        audio = tf.cast(audio, tf.float32)

        # 4. Get the spectrogram
        spectrogram = tf.signal.stft(audio, frame_length=self.frame_length, frame_step=self.frame_step, fft_length=self.fft_length)
        
        # 5. Doing the abs and the sqrt
        spectrogram = tf.abs(spectrogram)
        spectrogram = tf.math.pow(spectrogram, 0.5)

        # 6. Normalize the spectrogram
        means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
        stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
        spectrogram = (spectrogram - means) / (stddevs + 1e-10)

        # 7. label in lower case
        label = tf.strings.lower(label)

        # 8.  UTF-8
        label = tf.strings.unicode_split(label, input_encoding="UTF-8")

        # 9. label to numbers
        label = self.char_to_num(label)

        # 10. Return label and spectrogram
        return spectrogram, label

    def create_dataset(self):
        batch_size = 32
        # Define the training dataset
        train_dataset = tf.data.Dataset.from_tensor_slices(
            (list(df_train["path"]), list(df_train["sentence"]))
        )
        train_dataset = (
            train_dataset.map(encode_single_sample, num_parallel_calls=tf.data.AUTOTUNE)
            .padded_batch(batch_size)
            .prefetch(buffer_size=tf.data.AUTOTUNE)
        )

        # Define the validation dataset
        validation_dataset = tf.data.Dataset.from_tensor_slices(
            (list(df_val["path"]), list(df_val["sentence"]))
        )
        validation_dataset = (
            validation_dataset.map(encode_single_sample, num_parallel_calls=tf.data.AUTOTUNE)
            .padded_batch(batch_size)
            .prefetch(buffer_size=tf.data.AUTOTUNE)
        )

        print(validation_dataset)



