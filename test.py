from tensorflow.keras.models import load_model
from mcts import mcts_action
from predict import predict_p
from game import Game

pb = load_model('./model/policy_black.h5', compile=False)
pw = load_model('./model/policy_white.h5', compile=False)
vb = load_model('./model/value_black_t3.h5', compile=False)
vw = load_model('./model/value_white_t3.h5', compile=False)


game = Game()
a, b = 0, 0

for i in range(15):
    while True:
        if game.state.check_turn():
            game.next(mcts_action(pb, pw, vb, vw, game.state))
        else:
            game.next(predict_p(pb, pw, game.state))

        if game.end >= 1:
            a += game.w1
            b += game.w2
            game.__init__()
            break

print("mcts(흑)", a, ":", b, "예측 네트워크(백)")
a, b = 0, 0

for i in range(15):
    while True:
        if game.state.check_turn():
            game.next(predict_p(pb, pw, game.state))
        else:
            game.next(mcts_action(pb, pw, vb, vw, game.state))

        if game.end >= 1:
            a += game.w1
            b += game.w2
            game.__init__()
            break

print("예측 네트워크(흑)", a, ":", b, "mcts(백)")