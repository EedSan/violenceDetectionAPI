from tensorflow.keras.models import *
from tensorflow.keras.layers import *


def create_LSTM_model(sequence_length, image_height, image_width, classes_list):
    # We will use a Sequential model for model construction.
    model = Sequential()
    # Define the Model Architecture.
    model.add(TimeDistributed(Conv2D(32, (3, 3), padding='same', activation='relu'),
                              input_shape=(sequence_length, image_height, image_width, 3)))
    model.add(TimeDistributed(MaxPooling2D((4, 4))))
    model.add(TimeDistributed(Conv2D(64, (3, 3), padding='same', activation='relu')))
    model.add(TimeDistributed(MaxPooling2D((4, 4))))
    model.add(TimeDistributed(Conv2D(128, (3, 3), padding='same', activation='relu')))
    model.add(TimeDistributed(MaxPooling2D((2, 2))))
    model.add(TimeDistributed(Conv2D(256, (2, 2), padding='same', activation='relu')))
    model.add(TimeDistributed(MaxPooling2D((2, 2))))
    model.add(TimeDistributed(Flatten()))
    model.add(LSTM(16, return_sequences=True))
    model.add(Flatten())
    model.add(Dropout(0.3))
    model.add(Dense(len(classes_list), activation='softmax'))

    model.summary()
    return model
