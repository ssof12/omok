from state import State
from math import sqrt
from pathlib import Path
from tensorflow.keras.models import load_model
import numpy as np
from time import time

MCTS_COUNT = 10


def predict(model, state):
    a, b, c = (15, 15, 3)

    x = np.array([state.black, state.white, state.turn])
    x = x.reshape(c, a, b).transpose(1, 2, 0).reshape(1, a, b, c)

    y = model.predict(x, batch_size = 1)

    policies = y[0][0][list(state.referee()[0])]
    if sum(policies) != 0:
        policies /= sum(policies)
    value = y[1][0][0]

    return policies, value


def nodes_to_scores(nodes):
    scores = []
    for i in nodes:
        scores.append(i.n)
    return scores


def pv_mcts_action(model, temperature = 0):
    def pv_mcts_action(state):
        scores = pv_mcts_scores(model, state, temperature)
        return  np.random.choice(state.referee()[0], p = scores)
    return pv_mcts_action


def boltzman(xs, temperature):
    xs = [x ** (1 / temperature) for x in xs]
    return [x / sum(xs) for x in xs]


def pv_mcts_scores(model, state, temperature):
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
                if result[2] == 1: value = -1 # 패배
                else: value = 0               # 무승부
                self.w += value
                self.n += 1
                return value

            if not self.child_nodes:
                if self.previous_action != None:
                    self.state = self.state.next(self.previous_action)
                    self.previous_action = None
                policies, value = predict(model, self.state)
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

            for child_node in self.child_nodes:
                if child_node.n != 0:
                    a = (-child_node.w / child_node.n)
                else:
                    a = 0
                pucb_values.append(a + C_PUCT * child_node.p * sqrt(t) / (1 + child_node.n))
            return self.child_nodes[np.argmax(pucb_values)]


    root_node = Node(state, None, 0)

    for _ in range(MCTS_COUNT):
        root_node.evaluate()

    scores = nodes_to_scores(root_node.child_nodes)
    if temperature == 0:
        action = np.argmax(scores)
        scores = np.zeros(len(scores))
        scores[action] = 1
    else:
        scores = boltzman(scores, temperature)
    return scores

if __name__ == '__main__':
    path = sorted(Path('./model').glob('*.h5'))[-1]
    model = load_model(str(path))

    state = State()
    next_action = pv_mcts_action(model, 1.0)

    while True:
        if state.referee()[2] != 0:
            break

        action = next_action(state)
        state = state.next(action)

        for i in range(15):
            print(state.black[i])
        print()