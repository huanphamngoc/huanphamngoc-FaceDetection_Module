from keras.models import Sequential
from keras.layers import(
    Conv2D,
    MaxPooling2D,
    Dense, 
    Activation, 
    Flatten, 
    BatchNormalization
)

class CNN():
    def __init__(self, input_shape, num_of_classes):
        self.input_shape = input_shape
        self.num_of_classes = num_of_classes

    def cnn_model(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3), input_shape = self.input_shape, padding='same'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())

        model.add(Conv2D(64, kernel_size=(3, 3), padding='same'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())

        model.add(Conv2D(128, kernel_size=(3, 3), padding='same'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())
        model.add(Dense(256, activation='relu'))

        model.add(BatchNormalization())
        model.add(Dense(self.num_of_classes, activation='softmax'))
        
        model.compile(loss='sparse_categorical_crossentropy',
                        optimizer='adam',
                        metrics=['accuracy'])

        return model