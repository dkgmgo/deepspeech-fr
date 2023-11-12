import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from IPython import display
from jiwer import wer

#les data sont sur git (on peut faire ça pour tous collaborer dessus)
data_url = "https://url.du.dataset"
data_path = keras.utils.get_file("dataSpeech", data_url, untar=True)

#chemin du csv
metadata_path = data_path + "/dataset.csv"

#on lit metadata
metadata_df = pd.read_csv(metadata_path, sep="|", header=None, quoting=3)

metadata_df.columns = ["file_name", "transcription", "normalized_transcription"] #le nom des colonnes (à voir si on change)
metadata_df = metadata_df[["file_name", "normalized_transcription"]] #on sélectionne l'eesentiel
metadata_df = metadata_df.sample(frac=1).reset_index(drop=True) #pour mélanger le dataframe pour avoir un ordre aléatoire
metadata_df.head(3) #pour avoir un aperçu du dataframe