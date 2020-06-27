from math import sqrt
import numpy as np
from random import randint

MCTS_COUNT = 100
PRUNING_COUNT = 5


def predict_policy(pb, pw, state):
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

    return policies


def predict_value(vb, vw, state):
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
        return 1.0
    elif len(defend_action) == 0 and attack_action:
        return 1.0
    elif len(defend_action) + len(defend2_action) >= 2:
        return 0.0

    a, b, c = (15, 15, 2)

    if state.check_turn():
        x = np.array([state.black, state.white])
        x = x.reshape(c, a, b).transpose(1, 2, 0).reshape(1, a, b, c)
        y = vb.predict(x, batch_size=1)
    else:
        x = np.array([state.white, state.black])

    x = x.reshape(c, a, b).transpose(1, 2, 0).reshape(1, a, b, c)
    y = vw.predict(x, batch_size = 1)
    value = y[0]

    return value


def nodes_to_scores(nodes):
    scores = []
    for i in nodes:
        scores.append(i.n)
    return scores


def p_pruning(nodes):
    def get_p(node):
        return node.p

    pruning = []
    for i in nodes:
        pruning.append(i)
    pruning.sort(key=get_p, reverse=True)

    return pruning[:PRUNING_COUNT]


def pv_mcts_action(p_model, v_model, temperature = 0):
    def pv_mcts_action(state):
        scores = pv_mcts_scores(p_model, v_model, state, temperature)
        return  np.random.choice(state.referee()[0], p = scores)
    return pv_mcts_action


def pv_mcts_scores(pb, pw, vb, vw, state):
    class Node:
        def __init__(self, p_s, p_action, p):
            self.state = p_s
            self.previous_action = p_action
            self.p = p
            self.w = 0
            self.n = 0
            self.child_nodes = None

        def evaluate(self):
            result = self.state.referee()
            # 게임 종료 시
            if result[2] != 0:
                if result[2] == 1:
                    value = -1  # 패배
                else:
                    value = 0  # 무승부
                self.w += value
                self.n += 1
                return value

            if not self.child_nodes:
                if self.previous_action != None:
                    self.state = self.state.next(self.previous_action)
                    self.previous_action = None

                policies = predict_policy(pb, pw, self.state)
                value = predict_value(vb, vw, self.state)

                self.w += value
                self.n += 1

                self.child_nodes = []

                for action, policy in zip(result[0], policies):
                    self.child_nodes.append(Node(self.state, action, policy))

                return value

            else:
                value = -self.next_child_node().evaluate()
                self.w += value
                self.n += 1
                return value

        def next_child_node(self):
            C_PUCT = 1.0
            t = sum(nodes_to_scores(self.child_nodes))
            pucb_values = []

            pruned_child_nodes = p_pruning(self.child_nodes)

            #print(self.child_nodes[84].previous_action, self.child_nodes[84].p)
            for child_node in pruned_child_nodes:
                if child_node.n != 0:
                    a = (-child_node.w / child_node.n)
                else:
                    a = 0
                pucb_values.append(a + C_PUCT * child_node.p * sqrt(t) / (1 + child_node.n))

            #for _ in range(5):
                #print(pruned_child_nodes[_].previous_action, pruned_child_nodes[_].p)
            return pruned_child_nodes[np.argmax(pucb_values)]
    root_node = Node(state, None, 0)

    for _ in range(MCTS_COUNT):
        root_node.evaluate()

    scores = nodes_to_scores(root_node.child_nodes)
    action = np.argmax(scores)
    scores = np.zeros(len(scores))
    scores[action] = 1

    return scores


def mcts_action(pb, pw, vb, vw, state):
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

    scores = pv_mcts_scores(pb, pw, vb, vw, state)

    # 랜덤성 부여
    #action = np.random.choice(state.referee()[0], p = scores)
    # 최선의 수 착수
    action = state.referee()[0][np.argmax(scores)]

    if defend2_action and action not in defend2_action:
        if state.count_4(action//15, action%15) == 0:
            return defend2_action[randint(0, len(defend2_action) - 1)]

    return action