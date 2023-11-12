

class Model:
    def __init__(self, input_dim: int, output_dim: int, rnn_layers=5, rnn_units=128) -> None:
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.rnn_layers = rnn_layers
        self.rnn_units = rnn_units

        self.model = self.build_model()

    def build_model(self):
        pass

    def compute_loss(self):
        pass
