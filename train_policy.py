# 일괄 학습


import numpy as np
import codecs
from copy import deepcopy
from tensorflow.keras.layers import Activation, Dense, Dropout, Conv2D, Flatten, MaxPool2D
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from random import randint

from state import State
from feature import get_features

TRAIN_SIZE = 10000
TRAIN_COUNT = 1
TEST_SIZE = 2000


# 모델 생성
model = Sequential()

model.add(Conv2D(96, (3, 3), activation='relu', padding='same', input_shape=(15, 15, 9)))
for i in range(5):
    model.add(Conv2D(96, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(1, (1, 1), activation='relu', padding='same'))

model.add(Flatten())
model.add(Dense(225, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001), metrics=['acc'])
model.save('model1.h5')

# 모델 load
model = load_model('model1.h5')

# f = open("data.txt", 'r', encoding='utf-16')
f = codecs.open("data.txt", encoding='mac_roman')


def symmetry(i, r, c):
    if i == 0:
        return r, c
    elif i == 1:
        return r, 14 - c
    elif i == 2:
        return c, r
    elif i == 3:
        return c, 14 - r
    elif i == 4:
        return 14 - r, c
    elif i == 5:
        return 14 - r, 14 - c
    elif i == 6:
        return 14 - c, r
    elif i == 7:
        return 14 - c, 14 - r


for data_num in range(TRAIN_COUNT):
    count = 0
    state = np.zeros(shape=(TRAIN_SIZE,9,15,15))
    move = np.zeros(shape=TRAIN_SIZE)

    while True:
        line = f.readline()
        if not line:
            break
        if line[:6] != "<move>":
            continue

        i = 6
        black = []
        white = []
        turn = []

        for n in range(15):
            black.append([0] * 15)
            white.append([0] * 15)
            turn.append([1] * 15)

        sym = randint(0, 7)
        s = State()

        while 96 < ord(line[i]) < 112:
            r = ord(line[i]) - 97
            if 47 < ord(line[i + 2]) < 58:
                c = int(line[i + 1:i + 3]) - 1
                i += 4
            else:
                c = int(line[i + 1]) - 1
                i += 3

            r, c = symmetry(sym, r, c)
            legal_features, my_feature_4, my_feature_3, my_feature_2, enemy_feature_4, enemy_feature_3 = get_features(s)
            state[count] = [deepcopy(black), deepcopy(white), deepcopy(turn), legal_features, my_feature_4, my_feature_3, my_feature_2, enemy_feature_4, enemy_feature_3]
            move[count] = 15 * r + c
            count += 1
            s = s.next(15 * r + c)

            if turn[0][0] == 1:
                black[r][c] = 1
                turn = [[0] * 15] * 15
            else:
                white[r][c] = 1
                turn = [[1] * 15] * 15

            if count == TRAIN_SIZE:
                break

        if count == TRAIN_SIZE:
            break

    state = state.transpose(0, 2, 3, 1)
    move = to_categorical(move, 225)

    print("데이터", data_num + 1)
    print(state.shape)
    print(move.shape)
    print()

    # 모델 학습
    history = model.fit(state, move, batch_size=5120, epochs=20, validation_split=0.1)
    print()
    print()

    # 메모리 해제
    state = np.array([0])
    move = np.array([0])

    # 모델 저장
    model.save('train' + str(data_num + 1) + '.h5')


state = np.zeros(shape=(TEST_SIZE,3,15,15))
move = np.zeros(shape=TEST_SIZE)
count = 0
while True:
    line = f.readline()
    if not line:
        break
    if line[:6] != "<move>":
        continue

    i = 6
    black = []
    white = []
    turn = []

    for n in range(15):
        black.append([0] * 15)
        white.append([0] * 15)
        turn.append([1] * 15)

    sym = randint(0, 7)

    while 96 < ord(line[i]) < 112:
        r = ord(line[i]) - 97
        if 47 < ord(line[i + 2]) < 58:
            c = int(line[i + 1:i + 3]) - 1
            i += 4
        else:
            c = int(line[i + 1]) - 1
            i += 3

        r, c = symmetry(sym, r, c)
        state[count] = [deepcopy(black), deepcopy(white), deepcopy(turn)]
        move[count] = 15 * r + c
        count += 1

        if turn[0][0] == 1:
            black[r][c] = 1
            turn = [[0] * 15] * 15
        else:
            white[r][c] = 1
            turn = [[1] * 15] * 15

        if count == TEST_SIZE:
            break

    if count == TEST_SIZE:
        break

f.close()


state = state.transpose(0, 2, 3, 1)
move = to_categorical(move, 225)

print("테스트 데이터")
print(state.shape)
print(move.shape)
print()

# 평가
test_loss, test_acc = model.evaluate(state, move)

# 메모리 해제
state = np.array([0])
move = np.array([0])