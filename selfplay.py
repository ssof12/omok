from state import State
from mcts import pv_mcts_scores, boltzman, predict
from network import DN_OUTPUT_SIZE
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from pathlib import Path
import numpy as np
import pickle
import os
from random import randint
from test import model_action

GAME_COUNT = 500
TEMPERATURE = 1.0


def black_value(ended_state):
    # 1: 흑 승, -1: 백 승, 0: 무승부
    if ended_state.check_lose():
        return -1 if ended_state.check_turn() else 1
    return 0


def write_data(history):
    now = datetime.now()
    os.makedirs('./data/', exist_ok=True)
    path = './data/{:04}{:02}{:02}{:02}{:02}{:02}.history'.format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    with open(path, mode='wb') as f:
        pickle.dump(history, f)


# def play():
def play(model):
    history = []

    state = State()
    while True:
        if state.referee()[2] != 0:
            break

        # mcts
        # scores = pv_mcts_scores(model, state, TEMPERATURE)

        policies = [0] * DN_OUTPUT_SIZE
        '''
        for action, policy in zip(state.referee()[0], scores):
            policies[action] = policy
        history.append([[state.black, state.white, state.turn], policies, None])
        '''

        # action = np.random.choice(state.referee()[0], p=scores)
        action = state.bot_action()
        policies[action] = 1
        history.append([[state.black, state.white, state.turn], policies, None])

        scores, v = predict(model, state)
        scores = boltzman(scores, TEMPERATURE)
        action = np.random.choice(state.referee()[0], p=scores)
        state = state.next(action)

    value = black_value(state)
    for i in range(len(history)):
        history[i][2] = value
        value = -value
    return history


def self_play():
    history = []

    model = load_model('./model/best.h5')

    for i in range(GAME_COUNT):
        h = play(model)
        history.extend(h)
        print('\rSelfPlay {}/{}'.format(i+1, GAME_COUNT), end='')
    print('')

    write_data(history)

    K.clear_session()
    del model


if __name__ == '__main__':
    self_play()