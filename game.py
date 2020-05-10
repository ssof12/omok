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


    def next(self, action):
        if action in self.legal_actions:
            self.state = self.state.next(action)
            self.legal_actions, self.illegal, self.end = self.state.referee()
            self.history.append(action)

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
                    print('제', str(count) + '국,', str(length) + '수', winner, '승', str(self.w1)+'/'+str(self.w2)+'/'+str(self.w3))
                else:
                    print('제', str(count) + '국,', str(length) + '수', '무승부', str(self.w1)+'/'+str(self.w2)+'/'+str(self.w3))

                w1,w2,w3 = self.w1, self.w2, self.w3
                self.__init__()
                self.w1, self.w2, self.w3 = w1,w2,w3
                self.game_count = count


    def text_view(self):
        text_board = [0] * board_size

        for i in range(15):
            for j in range(15):
                if self.state.black[i][j] == 1:
                    text_board[15 * i + j] = 1
                elif self.state.white[i][j] == 1:
                    text_board[15 * i + j] = -1

        text = ''
        for i in range(225):
            if text_board[i] == 0:
                text += '-'
            elif text_board[i] == 1:
                text += 'O'
            elif text_board[i] == -1:
                text += 'X'
            if i%15 == 14:
                text += '\n'
        print(text)


    def text_run(self):
        while True:
            self.text_view()
            while True:
                a = int(input('행'))
                b = int(input('열'))
                if 15 * a + b in self.legal_actions:
                    self.next(15 * a + b)
                    break
            #self.next(mcts.mcts_action(self.state))


if __name__ == '__main__':
    g = Game()
    g.text_run()