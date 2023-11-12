import pandas as pd
import tensorflow as tf
# TODO
class DataLoader:
    def __init__(self) -> None:
        data_path = "commond_dataset/"
        self.audio_path = data_path + "/audio/"
        self.metadata_path = data_path + "/validated.csv"
        print(self.metadata_path)


        metadata_df = self.load_data()  # save the result in metadata_df
        self.split_data(metadata_df)    # from  metadata_df to split_data

    def fetch_data(self) -> None:
        # Download data from the specified URL and return paths
        pass

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
    def __init__(self, frame_length: int, frame_step: int, fft_length: int) -> None:
        self.frame_length = frame_length
        self.frame_step = frame_step
        self.fft_length = fft_length
        self.characters = [c for c in ""]

    def process_audio_sample(audio_file, ) -> tuple:
        # Process the audio and label
        pass

    def char_to_num(self):
        pass

    def num_to_char(self):
        pass

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



