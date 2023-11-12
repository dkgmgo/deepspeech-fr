import tensorflow as tf
from tensorflow import keras

# TODO
class DataLoader:
    def __init__(self, data_url: str) -> None:
        self.data_url = data_url
        data_path = ""
        self.audio_path = data_path + "/audio/"
        self.metadata_path = data_path + "/metadata.csv"

        self.fetch_data()
        self.load_data()
        self.split_data()

    def fetch_data(self) -> None:
        # Download data from the specified URL and return paths
        pass

    def load_data(self) -> None:
        # Read metadata file and parse it
        pass

    def split_data(self) -> None:
        # Split the data into training and validation sets
        pass


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
        pass
