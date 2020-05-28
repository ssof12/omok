from state import State


class Tree:
    def __init__(self, state, p_action):
        self.state = state
        self.child_node = []
        self.v = None
        self.previous_action = p_action


class Ai:
    def __init__(self):
        pass


    def vcf_cycle(self, current):
        for i in range(15):
            for j in range(15):
                if current.state.black[i][j] == 0 and current.state.white[i][j] == 0:
                    if current.state.check_finish(i, j):
                        current.child_node.append(Tree(current.state.next(15 * i + j), 15*i + j))
                        current.child_node[-1].v = True
                        return True
                    if current.state.count_4(i, j) > 0 and current.state.check_legal(i, j)[0]:
                        current.child_node.append(Tree(current.state.next(15 * i + j), 15*i + j))

        if len(current.child_node) > 0:
            for c in current.child_node:
                for k in c.state.defend_list():
                    c.child_node.append(Tree(c.state.next(k), k))

                if len(c.child_node) > 0:
                    for k in c.child_node:
                        if c.v == True or c.v == None:
                            c.v = self.vcf_cycle(k)
                        if c.v == False:
                            break

                # k가 없는 경우
                else:
                    return True

                # k가 전부 True인 경우
                if c.v == True:
                    return True

            # c가 다 False인 경우
            return False

        # c가 없는 경우
        else:
            return False


    def vct_cycle(self, current):
        for i in range(15):
            for j in range(15):
                if current.state.black[i][j] == 0 and current.state.white[i][j] == 0:
                    if current.state.check_finish(i, j) or current.state.check_finish2(i, j):
                        current.child_node.append(Tree(current.state.next(15 * i + j), 15*i + j))
                        current.child_node[-1].v = True
                        return True
                    if (current.state.count_3(i, j) > 0 or current.state.count_4(i, j) > 0) and current.state.check_legal(i, j)[0]:
                        current.child_node.append(Tree(current.state.next(15 * i + j), 15 * i + j))

        if len(current.child_node) > 0:
            for c in current.child_node:
                for k in c.state.defend_list():
                    c.child_node.append(Tree(c.state.next(k), k))

                for k in c.state.defend_list2():
                    c.child_node.append(Tree(c.state.next(k), k))

                if len(c.child_node) > 0:
                    for k in c.child_node:
                        if c.v == True or c.v == None:
                            c.v = self.vct_cycle(k)
                        if c.v == False:
                            break

                # k가 없는 경우
                else:
                    return True

                # k가 전부 True인 경우
                if c.v == True:
                    return True

            # c가 다 False인 경우
            return False

        # c가 없는 경우
        else:
            return False



    @staticmethod
    def action(self, state):
        win_action = []
        depend_action = []
        attack_action = []

        if state.check_turn():
            me = state.black
            enemy = state.white
        else:
            me = state.white
            enemy = state.black

        for i in range(15):
            for j in range(15):
                # 5 찾기
                if state.black[i][j] == 0 and state.white[i][j] == 0 and state.check_5(i, j):
                    win_action.append(15 * i + j)

        for i in range(15):
            for j in range(15):
                # 백의 경우 6이상도 찾기
                if not state.check_turn():
                    if state.black[i][j] == 0 and state.white[i][j] == 0 and state.check_6(i, j):
                        win_action.append(15 * i + j)

        for i in range(15):
            for j in range(15):
                # 상대 4 찾기
                if not win_action and enemy[i][j] == 1:
                    for k in state.check_defend(i, j):
                        if k not in depend_action and state.check_legal(k // 15, k % 15)[0]:
                            depend_action.append(k)

        for i in range(15):
            for j in range(15):
                # 열린 3 찾기
                if not win_action and not depend_action and me[i][j] == 1:
                    for k in state.check_attack(i, j):
                        if k not in attack_action and state.check_legal(k // 15, k % 15)[0]:
                            attack_action.append(k)

        for i in range(15):
            for j in range(15):
                # finish 찾기
                if me[i][j] == 0 and enemy[i][j] == 0 and state.check_finish(i, j):
                    if state.check_legal(i, j)[0]:
                        attack_action.append(15*i + j)

        # vcf 탐색
        if not win_action and not depend_action and not attack_action:
            vcf_root = Tree(state, None)
            if self.vcf_cycle(vcf_root):
                for c in vcf_root.child_node:
                    if c.v == True:
                        attack_action.append(c.previous_action)

        # 상대 3 찾기
        if not win_action and not depend_action and not attack_action:
            for i in range(15):
                for j in range(15):
                    if enemy[i][j] == 1:
                        for k in state.check_defend2(i, j):
                            if k not in depend_action and state.check_legal(k // 15, k % 15)[0]:
                                depend_action.append(k)

        # finish2 찾기
        if not win_action and not depend_action and not attack_action:
            for i in range(15):
                for j in range(15):
                    if me[i][j] == 0 and enemy[i][j] == 0 and state.check_finish2(i, j):
                        if state.check_legal(i, j)[0]:
                            attack_action.append(15 * i + j)

        # vct 탐색
        if not win_action and not depend_action and not attack_action:
            vct_root = Tree(state, None)
            if self.vct_cycle(vct_root):
                for c in vct_root.child_node:
                    if c.v == True:
                        attack_action.append(c.previous_action)


    def find_opened_3(self, state, color):
        pass


    def find_closed_3(self):
        pass