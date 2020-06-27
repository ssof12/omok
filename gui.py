import pygame as pg
import ctypes
import game
from tensorflow.keras.models import load_model

from predict import get_policy, get_value, predict_p
from mcts import mcts_action


ctypes.windll.user32.SetProcessDPIAware()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
size = [800, 800]
diameter = 45
button_size = 120
dot_size = 12

board = pg.image.load('images/오목판.png')
stone_black = pg.image.load('images/stone_black2.png')
stone_white = pg.image.load('images/stone_white.png')
mark_33 = pg.image.load('images/33.png')
mark_44 = pg.image.load('images/44.png')
mark_6 = pg.image.load('images/6.png')
button_1 = pg.image.load('images/button_1.png')
button_2 = pg.image.load('images/button_2.png')
button_3 = pg.image.load('images/button_3.png')
button_4 = pg.image.load('images/button_4.png')
button_5 = pg.image.load('images/button_5.png')
button_6 = pg.image.load('images/button_6.png')
button_7 = pg.image.load('images/button_7.png')
#icon = pg.image.load('images/icon5.png')
s = pg.Surface((12,12))
s.fill((255,0,0))
last = pg.Surface((20,20))

clock = pg.time.Clock()
#pg.display.set_icon(pg.transform.smoothscale(icon, (32, 32)))
pg.display.set_caption("오목")


class Gui:
    def __init__(self):
        self.game = game.Game()
        self.width, self.height = 800, 800
        self.diameter = diameter
        self.button_size = button_size
        self.dot_size = dot_size
        self.board = board
        self.stone_black = stone_black
        self.stone_white = stone_white
        self.button_1 = button_1
        self.button_2 = button_2
        self.button_3 = button_3
        self.button_4 = button_4
        self.button_5 = button_5
        self.button_6 = button_6
        self.button_7 = button_7
        self.mark_33 = mark_33
        self.mark_44 = mark_44
        self.mark_6 = mark_6
        self.hint = False
        self.new_game = False
        self.bs = 0
        self.ws = 0
        self.model = load_model('./model/policy_black.h5', compile=False)
        self.model2 = load_model('./model/policy_white.h5', compile=False)
        self.model3 = load_model('./model/value_black_t3.h5', compile=False)
        self.model4 = load_model('./model/value_white_t3.h5', compile=False)
        self.update_game_view()


    def run(self):
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.VIDEORESIZE:
                    self.width, self.height = event.dict['size']
                    self.diameter = int(self.width / 800 * diameter)
                    self.button_size = int(self.width / 800 * button_size)
                    self.dot_size = int(self.width / 800 * dot_size)

                    self.board = pg.transform.smoothscale(board, (self.width, self.height))
                    self.stone_black = pg.transform.smoothscale(stone_black, (self.diameter, self.diameter))
                    self.stone_white = pg.transform.smoothscale(stone_white, (self.diameter, self.diameter))
                    self.mark_33 = pg.transform.smoothscale(mark_33, (self.diameter, self.diameter))
                    self.mark_44 = pg.transform.smoothscale(mark_44, (self.diameter, self.diameter))
                    self.mark_6 = pg.transform.smoothscale(mark_6, (self.diameter, self.diameter))
                    self.button_1 = pg.transform.smoothscale(button_1, (self.button_size, self.button_size))
                    self.button_2 = pg.transform.smoothscale(button_2, (self.button_size, self.button_size))
                    self.button_3 = pg.transform.smoothscale(button_3, (self.button_size, self.button_size))
                    self.button_4 = pg.transform.smoothscale(button_4, (self.button_size, self.button_size))
                    self.button_5 = pg.transform.smoothscale(button_5, (self.button_size, self.button_size))
                    self.button_6 = pg.transform.smoothscale(button_6, (self.button_size, self.button_size))
                    self.button_7 = pg.transform.smoothscale(button_7, (self.button_size, self.button_size))


                    self.update_game_view()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x,y = event.pos
                    row = round((y - 43 * self.width / 800) / (51 * self.width / 800))
                    col = round((x - 43 * self.width / 800) / (51 * self.width / 800))

                    if 700 * self.width / 800 < x < 780 * self.width / 800 and y < 45 * self.width / 800:
                        if self.hint:
                            self.hint = False
                        else:
                            self.hint = True
                        self.update_game_view()
                        pg.event.clear()
                        break
                    elif 50 * self.width / 800 < x < 130 * self.width / 800 and y < 45 * self.width / 800:
                        if not self.new_game:
                            self.game.__init__()
                            self.bs = 0
                            self.ws = 0
                            self.new_game = True
                        else:
                            if self.bs == 0:
                                self.bs = 1
                            else:
                                self.ws = 1
                                self.new_game = False
                        self.update_game_view()
                        pg.event.clear()
                        break
                    elif 140 * self.width / 800 < x < 220 * self.width / 800 and y < 45 * self.width / 800:
                        if self.new_game:
                            if self.bs == 0:
                                self.bs = 2
                            else:
                                self.ws = 2
                                self.new_game = False
                        self.update_game_view()
                        pg.event.clear()
                        break

                    if self.bs != 0 and self.ws != 0:
                        if self.bs == 1 and self.game.state.check_turn():
                            self.game.next(row * game.width + col)
                            if self.game.end >= 1:
                                self.new_game = False
                                self.bs = 0
                                self.ws = 0
                            self.update_game_view()
                            pg.event.clear()
                            break

                        elif self.ws == 1 and not self.game.state.check_turn():
                            self.game.next(row * game.width + col)
                            if self.game.end >= 1:
                                self.new_game = False
                                self.bs = 0
                                self.ws = 0
                            self.update_game_view()
                            pg.event.clear()
                            break

            if self.bs != 0 and self.ws != 0:
                if self.bs == 2 and self.game.state.check_turn():
                    #self.game.next(predict_p(self.model, self.game.state))
                    self.game.next(mcts_action(self.model, self.model2, self.model3, self.model4, self.game.state))
                    if self.game.end >= 1:
                        self.new_game = False
                        self.bs = 0
                        self.ws = 0
                    self.update_game_view()
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            done = True
                        elif event.type == pg.VIDEORESIZE:
                            self.width, self.height = event.dict['size']
                            self.diameter = int(self.width / 800 * diameter)
                            self.button_size = int(self.width / 800 * button_size)
                            self.dot_size = int(self.width / 800 * dot_size)

                            self.board = pg.transform.smoothscale(board, (self.width, self.height))
                            self.stone_black = pg.transform.smoothscale(stone_black, (self.diameter, self.diameter))
                            self.stone_white = pg.transform.smoothscale(stone_white, (self.diameter, self.diameter))
                            self.mark_33 = pg.transform.smoothscale(mark_33, (self.diameter, self.diameter))
                            self.mark_44 = pg.transform.smoothscale(mark_44, (self.diameter, self.diameter))
                            self.mark_6 = pg.transform.smoothscale(mark_6, (self.diameter, self.diameter))
                            self.button_1 = pg.transform.smoothscale(button_1, (self.button_size, self.button_size))
                            self.button_2 = pg.transform.smoothscale(button_2, (self.button_size, self.button_size))
                            self.button_3 = pg.transform.smoothscale(button_3, (self.button_size, self.button_size))
                            self.button_4 = pg.transform.smoothscale(button_4, (self.button_size, self.button_size))
                            self.button_5 = pg.transform.smoothscale(button_5, (self.button_size, self.button_size))
                            self.button_6 = pg.transform.smoothscale(button_6, (self.button_size, self.button_size))
                            self.button_7 = pg.transform.smoothscale(button_7, (self.button_size, self.button_size))

                            self.update_game_view()
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            x, y = event.pos
                            row = round((y - 43 * self.width / 800) / (51 * self.width / 800))
                            col = round((x - 43 * self.width / 800) / (51 * self.width / 800))

                            if 700 * self.width / 800 < x < 780 * self.width / 800 and y < 45 * self.width / 800:
                                if self.hint:
                                    self.hint = False
                                else:
                                    self.hint = True
                            elif 50 * self.width / 800 < x < 130 * self.width / 800 and y < 45 * self.width / 800:
                                if not self.new_game:
                                    self.game.__init__()
                                    self.bs = 0
                                    self.ws = 0
                                    self.new_game = True
                                else:
                                    if self.bs == 0:
                                        self.bs = 1
                                    else:
                                        self.ws = 1
                                        self.new_game = False
                            elif 140 * self.width / 800 < x < 220 * self.width / 800 and y < 45 * self.width / 800:
                                if self.new_game:
                                    if self.bs == 0:
                                        self.bs = 2
                                    else:
                                        self.ws = 2
                                        self.new_game = False

                            self.update_game_view()

                elif self.ws == 2 and not self.game.state.check_turn():
                    #self.game.next(predict_p(self.model, self.model2, self.game.state))
                    self.game.next(mcts_action(self.model, self.model2, self.model3, self.model4, self.game.state))
                    if self.game.end >= 1:
                        self.new_game = False
                        self.bs = 0
                        self.ws = 0
                    self.update_game_view()
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            done = True
                        elif event.type == pg.VIDEORESIZE:
                            self.width, self.height = event.dict['size']
                            self.diameter = int(self.width / 800 * diameter)
                            self.button_size = int(self.width / 800 * button_size)
                            self.dot_size = int(self.width / 800 * dot_size)

                            self.board = pg.transform.smoothscale(board, (self.width, self.height))
                            self.stone_black = pg.transform.smoothscale(stone_black, (self.diameter, self.diameter))
                            self.stone_white = pg.transform.smoothscale(stone_white, (self.diameter, self.diameter))
                            self.mark_33 = pg.transform.smoothscale(mark_33, (self.diameter, self.diameter))
                            self.mark_44 = pg.transform.smoothscale(mark_44, (self.diameter, self.diameter))
                            self.mark_6 = pg.transform.smoothscale(mark_6, (self.diameter, self.diameter))
                            self.button_1 = pg.transform.smoothscale(button_1, (self.button_size, self.button_size))
                            self.button_2 = pg.transform.smoothscale(button_2, (self.button_size, self.button_size))
                            self.button_3 = pg.transform.smoothscale(button_3, (self.button_size, self.button_size))
                            self.button_4 = pg.transform.smoothscale(button_4, (self.button_size, self.button_size))
                            self.button_5 = pg.transform.smoothscale(button_5, (self.button_size, self.button_size))
                            self.button_6 = pg.transform.smoothscale(button_6, (self.button_size, self.button_size))
                            self.button_7 = pg.transform.smoothscale(button_7, (self.button_size, self.button_size))

                            self.update_game_view()
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            x, y = event.pos
                            row = round((y - 43 * self.width / 800) / (51 * self.width / 800))
                            col = round((x - 43 * self.width / 800) / (51 * self.width / 800))

                            if 700 * self.width / 800 < x < 780 * self.width / 800 and y < 45 * self.width / 800:
                                if self.hint:
                                    self.hint = False
                                else:
                                    self.hint = True
                            elif 50 * self.width / 800 < x < 130 * self.width / 800 and y < 45 * self.width / 800:
                                if not self.new_game:
                                    self.game.__init__()
                                    self.bs = 0
                                    self.ws = 0
                                    self.new_game = True
                                else:
                                    if self.bs == 0:
                                        self.bs = 1
                                    else:
                                        self.ws = 1
                                        self.new_game = False
                            elif 140 * self.width / 800 < x < 220 * self.width / 800 and y < 45 * self.width / 800:
                                if self.new_game:
                                    if self.bs == 0:
                                        self.bs = 2
                                    else:
                                        self.ws = 2
                                        self.new_game = False

                            self.update_game_view()

        pg.quit()


    def update_game_view(self):
        screen = pg.display.set_mode((self.width, self.height), pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
        screen.blit(self.board, (0, 0))

        for row in range(15):
            for col in range(15):
                if self.game.state.black[row][col] == 1:
                    screen.blit(self.stone_black,
                                (round(self.width / 2 - (7 - col) * 51 * self.width / 800 - self.diameter / 2),
                                 round(self.height / 2 - (7 - row) * 51 * self.height / 800 - self.diameter / 2)))

        for row in range(15):
            for col in range(15):
                if self.game.state.white[row][col] == 1:
                    screen.blit(self.stone_white,
                                (round(self.width / 2 - (7 - col) * 51 * self.width / 800 - self.diameter / 2),
                                 round(self.height / 2 - (7 - row) * 51 * self.height / 800 - self.diameter / 2)))

        for i in self.game.illegal:
            row = i[0] // game.width
            col = i[0] % game.width
            if i[1] == 3:
                screen.blit(self.mark_33,
                            (round(self.width / 2 - (7 - col) * 51 * self.width / 800 - self.diameter / 2),
                             round(self.height / 2 - (7 - row) * 51 * self.height / 800 - self.diameter / 2)))
            elif i[1] == 4:
                screen.blit(self.mark_44,
                            (round(self.width / 2 - (7 - col) * 51 * self.width / 800 - self.diameter / 2),
                             round(self.height / 2 - (7 - row) * 51 * self.height / 800 - self.diameter / 2)))
            elif i[1] == 6:
                screen.blit(self.mark_6,
                            (round(self.width / 2 - (7 - col) * 51 * self.width / 800 - self.diameter / 2),
                             round(self.height / 2 - (7 - row) * 51 * self.height / 800 - self.diameter / 2)))

        if self.game.last != None:
            row = self.game.last // 15
            col = self.game.last % 15
            if self.game.state.check_turn():
                color = (0,0,0)
            else:
                color = (255,255,255)
            pg.draw.rect(screen, color, [round(self.width / 2 - (7 - col) * 51 * self.width / 800 - 20 / 2),
                                                       round(self.height / 2 - (7 - row) * 51 * self.height / 800 - 21 / 2),
                                                       21,
                                                       21], 2)

        if self.hint and self.game.end == 0:
            if self.game.state.check_turn():
                print('현재 흑이 이길 확률 :', round((float(get_value(self.model3, self.model4, self.game.state)) * 100 + 100) / 2, 2), '%')
            else:
                print('현재 백이 이길 확률 :', round((float(get_value(self.model3, self.model4, self.game.state)) * 100 + 100) / 2, 2), '%')
            screen.blit(self.button_2, (680 * self.width / 800, -37 * self.width / 800))
            p, m = get_policy(self.model, self.model2, self.game.state)
            m = 1 / m
            n = 0
            for i in self.game.legal_actions:
                row = i // game.width
                col = i % game.width
                s.set_alpha(256 * p[n] * m)
                n += 1
                screen.blit(s,
                            (round(self.width / 2 - (7 - col) * 51 * self.width / 800 - self.dot_size / 2),
                             round(self.height / 2 - (7 - row) * 51 * self.height / 800 - self.dot_size / 2)))

        else:
            screen.blit(self.button_1, (680 * self.width / 800, -37 * self.width / 800))

        if not self.new_game:
            screen.blit(self.button_3, (30 * self.width / 800, -37 * self.width / 800))
        else:
            if self.bs == 0:
                screen.blit(self.button_4, (30 * self.width / 800, -37 * self.width / 800))
                screen.blit(self.button_5, (120 * self.width / 800, -37 * self.width / 800))
            elif self.ws == 0:
                screen.blit(self.button_6, (30 * self.width / 800, -37 * self.width / 800))
                screen.blit(self.button_7, (120 * self.width / 800, -37 * self.width / 800))

        pg.display.flip()


if __name__ == '__main__':
    gui = Gui()
    gui.run()
