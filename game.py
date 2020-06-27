from state import State

width = 15
height = 15
board_size = width * height

class Game:
    def __init__(self):
        self.state = State()
        self.legal_actions = []
        self.illegal = []
        self.history = []
        self.end = None
        self.legal_actions, self.illegal, self.end = self.state.referee()
        self.game_count = 0
        self.game_length = 0
        self.w1, self.w2, self.w3 = 0, 0, 0
        self.last = None


    def next(self, action):
        if action in self.legal_actions:
            self.last = action
            self.state = self.state.next(action)
            self.legal_actions, self.illegal, self.end = self.state.referee()
            self.history.append(action)
            self.game_length += 1

            # 패배 혹은 무승부
            if self.end >= 1:
                count = self.game_count + 1
                length = self.game_length
                if self.end == 1:
                    if self.state.check_turn():
                        winner = '백'
                        self.w2 += 1
                    else:
                        winner = '흑'
                        self.w1 += 1
                    print(str(length) + '수', winner, '승')
                else:
                    self.w3 += 1
                    print(str(length) + '수', '무승부')

                #self.__init__()