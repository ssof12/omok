import mcts
import random
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from game import Game
from state import State


def model_action(model, state):
    scores, v = mcts.predict(model, state)
    legal = state.referee()[0]
    actions = [0] * len(legal)
    for i in range(len(legal)):
        actions[i] = scores[i]
    action = actions.index(max(actions))
    action = legal[action]
    print(v)
    return action

def run():
    state = State()
    model = load_model('./model/latest.h5')
    i = 0
    win1 = 0
    win2 = 0
    draw = 0
    game_length = 0
    done = False
    while not done:
        if i % 2 == 0:
            if state.check_turn():
                #action = state.referee()[0][random.randint(0, len(state.referee()[0])-1)]
                #state = state.next(action)
                state = state.next(state.bot_action())
            else:
                action = model_action(model, state)
                state = state.next(action)
                # state.next(state.bot_action())
        else:
            if state.check_turn():
                action = model_action(model, state)
                state = state.next(action)
            else:
                #action = state.referee()[0][random.randint(0, len(state.referee()[0]) - 1)]
                #state = state.next(action)
                state = state.next(state.bot_action())
        game_length += 1
        if state.referee()[2] != 0:
            if state.check_lose():
                if state.check_turn():
                    if i % 2 == 0:
                        win2 += 1
                    else:
                        win1 += 1
                else:
                    if i % 2 == 0:
                        win1 += 1
                    else:
                        win2 += 1
            else:
                draw += 1
            i += 1
            state.__init__()
            print("random, model, draw", win1, win2, draw)
        if i == 10:
            break

if __name__ == '__main__':
    run()