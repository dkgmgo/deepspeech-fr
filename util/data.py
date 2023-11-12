
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
