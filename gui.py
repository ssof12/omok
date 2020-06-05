import pygame as pg
import ctypes
import game
import random
import mcts
from time import time
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
import numpy as np
from test import model_action
from ai import Ai
from test_model import predict
from feature import get_features


ctypes.windll.user32.SetProcessDPIAware()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
size = [800, 800]
diameter = 45

board = pg.image.load('images/오목판.png')
stone_black = pg.image.load('images/stone_black2.png')
stone_white = pg.image.load('images/stone_white.png')
mark_33 = pg.image.load('images/33.png')
#icon = pg.image.load('images/icon5.png')

clock = pg.time.Clock()
#pg.display.set_icon(pg.transform.smoothscale(icon, (32, 32)))
pg.display.set_caption("오목")


class Gui:
    def __init__(self):
        self.game = game.Game()
        self.width, self.height = 800, 800
        self.diameter = diameter
        self.board = board
        self.stone_black = stone_black
        self.stone_white = stone_white
        self.mark_33 = mark_33
        self.update_game_view()


    def run(self):
        #model = load_model('./model/latest.h5')
        #model2 = load_model('./model/best.h5')
        model = load_model('./model/aa.h5')
        model2 = load_model('train2.h5')

        ai = Ai()
        i = 0
        win1 = 0
        win2 = 0
        draw = 0
        done = False

        flag = True
        bm, wm = 1,2
        num = 0
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.VIDEORESIZE:
                    self.width, self.height = event.dict['size']
                    self.diameter = int(self.width / 800 * diameter)

                    self.board = pg.transform.smoothscale(board, (self.width, self.height))
                    self.stone_black = pg.transform.smoothscale(stone_black, (self.diameter, self.diameter))
                    self.stone_white = pg.transform.smoothscale(stone_white, (self.diameter, self.diameter))
                    self.mark_33 = pg.transform.smoothscale(mark_33, (self.diameter, self.diameter))

                    self.update_game_view()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x,y = event.pos
                    row = round((y - 43) / 51)
                    col = round((x - 43) / 51)

                    if self.game.state.check_turn():
                        pass
                        #self.game.next(predict(model, self.game.state))
                        self.game.next(row * game.width + col)
                        get_features(self.game.state)


                    else:
                        pass
                        #self.game.next(predict(model, self.game.state))
                        self.game.next(row * game.width + col)
                        get_features(self.game.state)

                    self.update_game_view()

            '''
            if self.game.state.check_turn():
                #action = model_action(model, self.game.state)
                #self.game.next(action)
                #self.game.next(self.game.legal_actions[random.randint(0, len(self.game.legal_actions) - 1)])
                action = model_action(model, self.game.state)
                self.game.next(action)
                self.update_game_view()
                self.game.game_length += 1
            else:
                #self.game.next(row * game.width + col)
                #self.game.next(self.game.legal_actions[random.randint(0, len(self.game.legal_actions) - 1)])
                #action = self.game.state.bot_action()
                #self.game.next(action)
                action = model_action(model, self.game.state)
                self.game.next(action)
                self.update_game_view()
                self.game.game_length += 1
        print("random, model, draw", win1, win2, draw)
        '''
        pg.quit()

    def random_play(self):
        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.VIDEORESIZE:
                    self.width, self.height = event.dict['size']
                    self.diameter = int(self.width / 800 * diameter)

                    self.board = pg.transform.smoothscale(board, (self.width, self.height))
                    self.stone_black = pg.transform.smoothscale(stone_black, (self.diameter, self.diameter))
                    self.stone_white = pg.transform.smoothscale(stone_white, (self.diameter, self.diameter))
                    self.mark_33 = pg.transform.smoothscale(mark_33, (self.diameter, self.diameter))

                    self.update_game_view()

            self.game.next(self.game.legal_actions[random.randint(0,len(self.game.legal_actions)-1)])
            self.game.game_length += 1
            self.update_game_view()
        pg.quit()


    def play_out(self):
        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.VIDEORESIZE:
                    self.width, self.height = event.dict['size']
                    self.diameter = int(self.width / 800 * diameter)

                    self.board = pg.transform.smoothscale(board, (self.width, self.height))
                    self.stone_black = pg.transform.smoothscale(stone_black, (self.diameter, self.diameter))
                    self.stone_white = pg.transform.smoothscale(stone_white, (self.diameter, self.diameter))
                    self.mark_33 = pg.transform.smoothscale(mark_33, (self.diameter, self.diameter))

                    self.update_game_view()

            mcts.playout(self.game.state)
            self.game.game_length += 1
            self.update_game_view()
            self.game.__init__()
        pg.quit()


    def mcts_play(self):
        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.VIDEORESIZE:
                    self.width, self.height = event.dict['size']
                    self.diameter = int(self.width / 800 * diameter)

                    self.board = pg.transform.smoothscale(board, (self.width, self.height))
                    self.stone_black = pg.transform.smoothscale(stone_black, (self.diameter, self.diameter))
                    self.stone_white = pg.transform.smoothscale(stone_white, (self.diameter, self.diameter))
                    self.mark_33 = pg.transform.smoothscale(mark_33, (self.diameter, self.diameter))

                    self.update_game_view()
                '''
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.game.state.turn:
                        x,y = event.pos
                        row = round((y - 43) / 51)
                        col = round((x - 43) / 51)
                        self.game.next(row * game.width + col)
                        self.update_game_view()
                        print(self.game.state.turn)
                '''


            if not self.game.state.turn:
                self.game.next(mcts.policy_action(self.game.state))
                #self.game.next(mcts.mcts_action(self.game.state))
                self.update_game_view()
            else:
                print('mcts')
                self.game.next(mcts.mcts_action(self.game.state))
                #self.game.next(self.game.legal_actions[random.randint(0,len(self.game.legal_actions)-1)])
                self.update_game_view()
            '''
            self.game.next(mcts.mcts_action(self.game.state))
            '''
            self.game.game_length += 1
            self.update_game_view()
        pg.quit()



    def update_game_view(self):
        screen = pg.display.set_mode((self.width, self.height), pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
        screen.blit(self.board, (0, 0))
        for row in range(15):
            for col in range(15):
                if self.game.state.black[row][col] == 1:
                    screen.blit(self.stone_black,
                                (round(self.width / 2 - (7 - col) * 51 * self.width / 800 - diameter / 2),
                                 round(self.height / 2 - (7 - row) * 51 * self.height / 800 - diameter / 2)))

        for row in range(15):
            for col in range(15):
                if self.game.state.white[row][col] == 1:
                    screen.blit(self.stone_white,
                                (round(self.width / 2 - (7 - col) * 51 * self.width / 800 - diameter / 2),
                                 round(self.height / 2 - (7 - row) * 51 * self.height / 800 - diameter / 2)))

        for i in self.game.illegal:
            row = i[0] // game.width
            col = i[0] % game.width
            screen.blit(self.mark_33,
                        (round(self.width / 2 - (7 - col) * 51 * self.width / 800 - diameter / 2),
                         round(self.height / 2 - (7 - row) * 51 * self.height / 800 - diameter / 2)))
        pg.display.flip()


if __name__ == '__main__':
    gui = Gui()
    gui.run()
