from network import DN_INPUT_SHAPE
from tensorflow.keras.callbacks import LearningRateScheduler, LambdaCallback
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from pathlib import Path
import numpy as np
import pickle


RN_EPOCHS = 100


def load_data():
    history_path = sorted(Path('./data').glob('*.history'))[-1]
    with history_path.open(mode='rb') as f:
        return pickle.load(f)


def train_network():
    history = load_data()
    xs, y_policies, y_values = zip(*history)

    a, b, c = DN_INPUT_SHAPE
    xs = np.array(xs)
    xs = xs.reshape(len(xs), c, a, b).transpose(0, 2, 3, 1)
    y_policies = np.array(y_policies)
    y_values = np.array(y_values)

    model = load_model('./model/best.h5')
    model.compile(loss=['categorical_crossentropy', 'mse'], optimizer='adam')

    def step_decay(epoch):
        '''
        x = 0.001
        if epoch >= 50: x = 0.0005
        if epoch >= 80: x = 0.00025
        '''

        '''
        x = 0.2
        if epoch >= 100:
            x = 0.02
        elif epoch >= 300:
            x = 0.002
        elif epoch >= 500000:
            x = 0.0002
        '''
        x = 0.02
        if epoch >= 100:
            x = 0.002
        elif epoch >= 500000:
            x = 0.0002

        return x

    lr_decay = LearningRateScheduler(step_decay)

    print_callback = LambdaCallback(
        on_epoch_begin=lambda epoch, logs:
        print('\rTrain {}/{}'.format(epoch + 1, RN_EPOCHS), end=''))

    model.fit(xs, [y_policies, y_values], batch_size=512, epochs=RN_EPOCHS,
              verbose=0, callbacks=[lr_decay, print_callback])
    print('')

    model.save('./model/latest.h5')
    K.clear_session()
    del model


if __name__ == '__main__':
    train_network()