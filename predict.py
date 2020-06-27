import numpy as np
from random import randint


# 예측 네트워크 시각화에 사용
def get_policy(pb, pw, state):
    a, b, c = (15, 15, 2)

    if state.check_turn():
        x = np.array([state.black, state.white])
    else:
        x = np.array([state.white, state.black])

    x = x.reshape(c, a, b).transpose(1, 2, 0).reshape(1, a, b, c)
    # x = x.transpose(1, 2, 0).reshape(1, a, b, c)

    if state.check_turn():
        y = pb.predict(x, batch_size=1)
    else:
        y = pw.predict(x, batch_size=1)
    policies = y[0][list(state.referee()[0])]

    if sum(policies) != 0:
        policies /= sum(policies)

    m = np.argmax(policies)

    return policies, policies[m]


# 예상 승률 출력에 사용
def get_value(vb, vw, state):
    a, b, c = (15, 15, 2)

    if state.check_turn():
        x = np.array([state.black, state.white])
        x = x.reshape(c, a, b).transpose(1, 2, 0).reshape(1, a, b, c)
        y = vb.predict(x, batch_size=1)
    else:
        x = np.array([state.white, state.black])
        x = x.reshape(c, a, b).transpose(1, 2, 0).reshape(1, a, b, c)
        y = vw.predict(x, batch_size=1)

    value = y[0]
    return value


# 예측 네트워크만으로 착수 (0.02초)
def predict_p(pb, pw, state):
    if state.black == [[0]*15]*15 and state.white == [[0]*15]*15:
        return 112

    win_action = []
    defend_action = []
    attack_action = []
    defend2_action = []

    if state.check_turn():
        me = state.black
        enemy = state.white
    else:
        me = state.white
        enemy = state.black

    for i in range(15):
        for j in range(15):

            if state.black[i][j] == 0 and state.white[i][j] == 0 and state.check_5(i, j):
                win_action.append(15 * i + j)

            if not state.check_turn():
                if state.black[i][j] == 0 and state.white[i][j] == 0 and state.check_6(i, j):
                    win_action.append(15 * i + j)

            if not win_action and enemy[i][j] == 1:
                for k in state.check_defend(i, j):
                    if k not in defend_action and state.check_legal(k // 15, k % 15)[0]:
                        defend_action.append(k)

            if not win_action and not defend_action and me[i][j] == 1:
                for k in state.check_attack(i, j):
                    if k not in attack_action and state.check_legal(k // 15, k % 15)[0]:
                        attack_action.append(k)

            if not win_action and not defend_action and state.black[i][j] == 0 and state.white[i][j] == 0:
                if state.check_finish(i, j):
                    attack_action.append(15 * i + j)

            if not win_action and not defend_action and not attack_action and enemy[i][j] == 1:
                for k in state.check_defend2(i, j):
                    if k not in defend2_action and state.check_legal(k // 15, k % 15)[0]:
                        defend2_action.append(k)

    if win_action:
        return win_action[randint(0, len(win_action) - 1)]
    elif defend_action:
        return defend_action[randint(0, len(defend_action) - 1)]
    elif attack_action:
        return attack_action[randint(0, len(attack_action) - 1)]

    a, b, c = (15, 15, 2)

    if state.check_turn():
        x = np.array([state.black, state.white])
        x = x.reshape(c, a, b).transpose(1, 2, 0).reshape(1, a, b, c)
        y = pb.predict(x, batch_size=1)
    else:
        x = np.array([state.white, state.black])
        x = x.reshape(c, a, b).transpose(1, 2, 0).reshape(1, a, b, c)
        y = pw.predict(x, batch_size=1)

    policies = y[0][list(state.referee()[0])]

    if sum(policies) != 0:
        policies /= sum(policies)

    move = np.random.choice(state.referee()[0], p=policies)

    if defend2_action and move not in defend2_action:
        if state.count_4(move//15, move%15) == 0:
            return defend2_action[randint(0, len(defend2_action) - 1)]
    return move
