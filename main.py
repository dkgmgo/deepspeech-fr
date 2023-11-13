from util.data import DataLoader, DataPrepocessor
from util.model import Model
from util.train import Trainer

if __name__ == "__main__":
    data_loader = DataLoader()
    preprocessor = DataPrepocessor(frame_length=256, frame_step=160, fft_length=384, audio_path=data_loader.audio_path)
    
    train_dataset, validation_dataset = preprocessor.create_dataset_objets(data_loader=data_loader)
    
    ds_model = Model(input_dim=preprocessor.fft_length//2 + 1, output_dim=preprocessor.char_to_num.vocabulary_size(), rnn_units=512)
    ds_model.model.summary(line_length=110)
    
    trainer = Trainer(model=ds_model.model, train_dataset=train_dataset, validation_dataset=validation_dataset, preprocessor=preprocessor)
    trainer.train(10)   