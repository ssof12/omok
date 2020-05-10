from tensorflow.keras.layers import Activation, Add, BatchNormalization, Conv2D, Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras import backend as K
import os


DN_FILTERS = 128
DN_RESIDUAL_NUM = 10
DN_INPUT_SHAPE = (15, 15, 3)
DN_OUTPUT_SIZE = 225


def conv(filters):
    return Conv2D(filters, 3, padding='same', use_bias=False,
                  kernel_initializer='he_normal', kernel_regularizer=l2(0.0005))


def residual_block():
    def f(x):
        sc = x
        x = conv(DN_FILTERS)(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = conv(DN_FILTERS)(x)
        x = BatchNormalization()(x)
        x = Add()([x, sc])
        x = Activation('relu')(x)
        return x
    return f


def dual_network():
    if os.path.exists('./model/best.h5'):
        return

    # 입력 레이어
    input = Input(shape=DN_INPUT_SHAPE)

    # 컨볼루션 레이어
    x = conv(DN_FILTERS)(input)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    # 레지듀얼 블록 x 10
    for i in range(DN_RESIDUAL_NUM):
        x = residual_block()(x)

    # 풀링 레이어
    x = GlobalAveragePooling2D()(x)

    # policy 출력
    p = Dense(DN_OUTPUT_SIZE, kernel_regularizer=l2(0.0005),
              activation='softmax', name='pi')(x)

    # value 출력
    v = Dense(1, kernel_regularizer=l2(0.0005))(x)
    v = Activation('tanh', name='v')(v)

    model = Model(inputs=input, outputs=[p, v])
    os.makedirs('./model/', exist_ok=True)  # 폴더가 없는 경우 생성
    model.save('./model/best.h5')  # 베스트 플레이어 모델

    K.clear_session()
    del model


if __name__ == '__main__':
    dual_network()