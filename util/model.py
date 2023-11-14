import tensorflow as tf
from keras import layers
import keras


class Model:
    def __init__(self, input_dim: int, output_dim: int, rnn_layers=5, rnn_units=128) -> None:
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.rnn_layers = rnn_layers
        self.rnn_units = rnn_units

        self.model = self.build_model()

    def build_model(self):
        """Model similar to DeepSpeech2."""
        # Model's input
        input_spectrogram = layers.Input((None, self.input_dim), name="input")

        # Expand the dimension to use 2D CNN.
        x = layers.Reshape((-1, self.input_dim, 1),
                           name="expand_dim")(input_spectrogram)

        # Convolution layer 1
        x = layers.Conv2D(
            filters=32,
            kernel_size=[11, 41],
            strides=[2, 2],
            padding="same",
            use_bias=False,
            name="conv_1",
        )(x)
        x = layers.BatchNormalization(name="conv_1_bn")(x)
        x = layers.ReLU(name="conv_1_relu")(x)

        # Convolution layer 2
        x = layers.Conv2D(
            filters=32,
            kernel_size=[11, 21],
            strides=[1, 2],
            padding="same",
            use_bias=False,
            name="conv_2",
        )(x)
        x = layers.BatchNormalization(name="conv_2_bn")(x)
        x = layers.ReLU(name="conv_2_relu")(x)

        # Reshape the resulted volume to feed the RNNs layers
        x = layers.Reshape((-1, x.shape[-2] * x.shape[-1]))(x)
        # RNN layers
        for i in range(1, self.rnn_layers + 1):
            recurrent = layers.GRU(
                units=self.rnn_units,
                activation="tanh",
                recurrent_activation="sigmoid",
                use_bias=True,
                return_sequences=True,
                reset_after=True,
                name=f"gru_{i}",
            )
            x = layers.Bidirectional(
                recurrent, name=f"bidirectional_{i}", merge_mode="concat"
            )(x)
            if i < self.rnn_layers:
                x = layers.Dropout(rate=0.5)(x)
        # Dense layer
        x = layers.Dense(units=self.rnn_units * 2, name="dense_1")(x)
        x = layers.ReLU(name="dense_1_relu")(x)
        x = layers.Dropout(rate=0.5)(x)
        # Classification layer
        output = layers.Dense(units=self.output_dim + 1,
                              activation="softmax")(x)
        # Model
        model = keras.Model(input_spectrogram, output, name="DeepSpeech_2")
        # Optimizer
        opt = keras.optimizers.Adam(learning_rate=1e-4)
        # Compile the model and return
        model.compile(optimizer=opt, loss=self.compute_loss)
        return model

    @keras.saving.register_keras_serializable(package="custom_losses", name="compute_loss")
    def compute_loss(self, y_true, y_pred):
        # Compute the training-time loss value
        batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
        in_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
        l_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

        in_length = in_length * tf.ones(shape=(batch_len, 1), dtype="int64")
        l_length = l_length * tf.ones(shape=(batch_len, 1), dtype="int64")

        loss = keras.backend.ctc_batch_cost(
            y_true, y_pred, in_length, l_length)
        return loss
