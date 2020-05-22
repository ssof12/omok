from state import State
from mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from pathlib import Path
from shutil import copy
import numpy as np


GAME_COUNT = 30
TEMPERATURE = 1.0


def black_point(ended_state):
    # 1: 흑 승, 0: 백 승, 0.5: 무승부
    if ended_state.check_lose():
        return 0 if ended_state.check_turn() else 1
    return 0.5


def play(next_actions):
    state = State()

    while True:
        if state.referee()[2] != 0:
            break

        next_action = next_actions[0] if state.check_turn() else next_actions[1]
        action = next_action(state)

        state = state.next(action)

    return black_point(state)


def update_best_player():
    copy('./model/latest.h5', './model/best.h5')
    print('Change model')


def evaluate_network():
    model0 = load_model('./model/latest.h5')
    model1 = load_model('./model/best.h5')

    next_action0 = pv_mcts_action(model0, TEMPERATURE)
    next_action1 = pv_mcts_action(model1, TEMPERATURE)
    next_actions = (next_action0, next_action1)


    total_point = 0
    for i in range(GAME_COUNT):
        if i % 2 == 0:
            total_point += play(next_actions)
        else:
            total_point += 1 - play(list(reversed(next_actions)))

        print('\rEvaluate {}/{}'.format(i + 1, GAME_COUNT), end='')
    print('')


    average_point = total_point / GAME_COUNT
    print('AveragePoint', average_point)

    K.clear_session()
    del model0
    del model1

    if average_point > 0.5:
        #update_best_player()
        return True
    else:
        return False


if __name__ == '__main__':
    evaluate_network()
