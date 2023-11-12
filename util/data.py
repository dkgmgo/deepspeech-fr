import pandas as pd

# TODO
class DataLoader():
    def __init__(self) -> None:
        data_path = "commond_dataset/"
        self.audio_path = data_path + "/audio/"
        self.metadata_path = data_path + "/validated.csv"
        print(self.metadata_path)


        metadata_df = self.load_data()  # Stockez le résultat dans metadata_df
        self.split_data(metadata_df)    # Passez metadata_df à split_data


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

        pass


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
        pass
