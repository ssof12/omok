from copy import deepcopy
from random import randint


class State:
    def __init__(self, black = [], white = [], turn = True):
        if not black:
            self.black = []
            for _ in range(15):
                self.black.append([0] * 15)
        else:
            self.black = deepcopy(black)

        if not white:
            self.white = []
            for _ in range(15):
                self.white.append([0] * 15)
        else:
            self.white = deepcopy(white)

        if turn:
            self.turn = [[1]]
        else:
            self.turn = [[0]]


    def next(self, action):
        if self.turn[0][0] == 1:
            black = deepcopy(self.black)
            black[action // 15][action % 15] = 1
            return State(black, self.white, False)
        else:
            white = deepcopy(self.white)
            white[action // 15][action % 15] = 1
            return State(self.black, white, True)


    def check_turn(self):
        if self.turn[0][0] == 1:
            return True
        else:
            return False


    # return legal, illegal, result(0: not end, 1: lose, 2: draw)
    def referee(self):
        legal = []
        illegal = []
        end = 0

        if self.check_lose():
            end = 1
            return legal, illegal, end

        empty = []
        for i in range(15):
            for j in range(15):
                if self.black[i][j] == 0 and self.white[i][j] == 0:
                    empty.append(15 * i + j)

        if len(empty) == 0:
            end = 2
            return legal, illegal, end

        if not self.check_turn():
            return empty, illegal, end

        for k in empty:
            i, j = k // 15, k % 15
            check_result = self.check_legal(i, j)
            if check_result[0]:
                legal.append(15 * i + j)
            else:
                illegal.append([15 * i + j, check_result[1]])

        if len(legal) == 0:
            end = 2

        return legal, illegal, end


    def check_lose(self):

        # left -> right
        for i in range(15):
            black_length = 0
            white_length = 0
            for j in range(15):
                if self.black[i][j] == 1:
                    black_length += 1
                    if black_length == 5:
                        return True
                else:
                    black_length = 0

                if self.white[i][j] == 1:
                    white_length += 1
                    if white_length == 5:
                        return True
                else:
                    white_length = 0

        # up -> down
        for i in range(15):
            black_length = 0
            white_length = 0
            for j in range(15):
                if self.black[j][i] == 1:
                    black_length += 1
                    if black_length == 5:
                        return True
                else:
                    black_length = 0

                if self.white[j][i] == 1:
                    white_length += 1
                    if white_length == 5:
                        return True
                else:
                    white_length = 0

        # lu -> rd
        for i in range(15):
            black_length = 0
            white_length = 0
            try:
                for j in range(15):
                    if self.black[i+j][j] == 1:
                        black_length += 1
                        if black_length == 5:
                            return True
                    else:
                        black_length = 0

                    if self.white[i + j][j] == 1:
                        white_length += 1
                        if white_length == 5:
                            return True
                    else:
                        white_length = 0
            except IndexError:
                pass

        for j in range(1,15):
            black_length = 0
            white_length = 0
            try:
                for i in range(15):
                    if self.black[i][j+i] == 1:
                        black_length += 1
                        if black_length == 5:
                            return True
                    else:
                        black_length = 0

                    if self.white[i][j+i] == 1:
                        white_length += 1
                        if white_length == 5:
                            return True
                    else:
                        white_length = 0
            except IndexError:
                pass

        # ld -> ru
        for i in range(15):
            black_length = 0
            white_length = 0
            try:
                for j in range(15):
                    if i-j < 0:
                        break
                    if self.black[i-j][j] == 1:
                        black_length += 1
                        if black_length == 5:
                            return True
                    else:
                        black_length = 0

                    if self.white[i-j][j] == 1:
                        white_length += 1
                        if white_length == 5:
                            return True
                    else:
                        white_length = 0
            except IndexError:
                pass

        for j in range(1, 15):
            black_length = 0
            white_length = 0
            try:
                for i in range(15):
                    if self.black[14-i][j + i] == 1:
                        black_length += 1
                        if black_length == 5:
                            return True
                    else:
                        black_length = 0

                    if self.white[14-i][j + i] == 1:
                        white_length += 1
                        if white_length == 5:
                            return True
                    else:
                        white_length = 0
            except IndexError:
                pass

        return False


    # return True/False, flag (0,3,4,6)
    def check_legal(self, i, j):
        if not self.check_turn():
            return True, 0

        if self.check_5(i, j):
            return True, 0
        elif self.check_6(i, j):
            return False, 6
        elif self.check_44(i, j):
            return False, 4
        elif self.check_33(i, j):
            return False, 3
        else:
            return True, 0


    def get_9set(self, i, j, c):
        if self.check_turn():
            me = self.black
        else:
            me = self.white

        if c == 0:
            a, b = 0, 1
        elif c == 1:
            a, b = 1, 0
        elif c == 2:
            a, b = 1, 1
        else:
            a, b = -1, 1

        left, mid, right = 0, 1, 0
        l1, l2, r1, r2 = 0, 0, 0, 0

        try:
            for k in range(1, 6):
                if i + a * k < 0 or j + b * k < 0:
                    break
                if me[i + a * k][j + b * k] == 1:
                    if r1 == 0:
                        mid += 1
                    else:
                        right += 1
                elif r1 == 0:
                    r1 = k
                else:
                    r2 = k
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 6):
                if i - a * k < 0 or j - b * k < 0:
                    break
                if me[i - a * k][j - b * k] == 1:
                    if l1 == 0:
                        mid += 1
                    else:
                        left += 1
                elif l1 == 0:
                    l1 = k
                else:
                    l2 = k
                    break
        except IndexError:
            pass

        return a, b, left, mid, right, l1, l2, r1, r2


    def check_5(self, i, j):
        if self.check_turn():
            me = self.black
        else:
            me = self.white

        me[i][j] = 1

        # left -> right
        length = 1
        try:
            for k in range(1,5):
                if me[i][j + k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 5):
                if j-k < 0:
                    break
                if me[i][j - k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        if length == 5:
            me[i][j] = 0
            return True

        # up -> down
        length = 1

        try:
            for k in range(1, 5):
                if me[i + k][j] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 5):
                if i-k < 0:
                    break
                if me[i - k][j] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        if length == 5:
            me[i][j] = 0
            return True

        # lu -> rd
        length = 1
        try:
            for k in range(1, 5):
                if me[i + k][j + k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 5):
                if i-k < 0 or j-k < 0:
                    break
                if me[i - k][j - k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        if length == 5:
            me[i][j] = 0
            return True

        # ld -> ru
        length = 1

        try:
            for k in range(1, 5):
                if i-k < 0:
                    break
                if me[i - k][j + k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 5):
                if j-k < 0:
                    break
                if me[i + k][j - k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        me[i][j] = 0

        if length == 5:
            return True

        return False


    def check_6(self, i, j):
        if self.check_turn():
            me = self.black
        else:
            me = self.white

        me[i][j] = 1

        # left -> right
        length = 1
        try:
            for k in range(1, 5):
                if me[i][j + k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 5):
                if j - k < 0:
                    break
                if me[i][j - k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        if length >= 6:
            me[i][j] = 0
            return True

        # up -> down
        length = 1

        try:
            for k in range(1, 5):
                if me[i + k][j] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 5):
                if i - k < 0:
                    break
                if me[i - k][j] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        if length >= 6:
            me[i][j] = 0
            return True

        # lu -> rd
        length = 1
        try:
            for k in range(1, 5):
                if me[i + k][j + k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 5):
                if i - k < 0 or j - k < 0:
                    break
                if me[i - k][j - k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        if length >= 6:
            me[i][j] = 0
            return True

        # ld -> ru
        length = 1

        try:
            for k in range(1, 5):
                if i - k < 0:
                    break
                if me[i - k][j + k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 5):
                if j - k < 0:
                    break
                if me[i + k][j - k] == 1:
                    length += 1
                else:
                    break
        except IndexError:
            pass

        if length >= 6:
            me[i][j] = 0
            return True

        me[i][j] = 0
        return False


    def get_10set(self, i, j, c):
        if self.check_turn():
            me = self.black
        else:
            me = self.white

        if c == 0:
            a, b = 0, 1
        elif c == 1:
            a, b = 1, 0
        elif c == 2:
            a, b = 1, 1
        else:
            a, b = -1, 1

        left, lm, rm, right = 0, 0, 0, 0
        l1, l2, r1, r2 = 0, 0, 0, 0

        try:
            for k in range(1, 6):
                if i + a * k < 0 or j + b * k < 0:
                    break
                if me[i + a * k][j + b * k] == 1:
                    if r1 == 0:
                        rm += 1
                    else:
                        right += 1
                elif r1 == 0:
                    r1 = k
                else:
                    r2 = k
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 6):
                if i - a * k < 0 or j - b * k < 0:
                    break
                if me[i - a * k][j - b * k] == 1:
                    if l1 == 0:
                        lm += 1
                    else:
                        left += 1
                elif l1 == 0:
                    l1 = k
                else:
                    l2 = k
                    break
        except IndexError:
            pass

        return a, b, left, lm, rm, right, l1, l2, r1, r2


    def get_e10set(self, i, j, c):
        if self.check_turn():
            enemy = self.white
        else:
            enemy = self.black

        if c == 0:
            a, b = 0, 1
        elif c == 1:
            a, b = 1, 0
        elif c == 2:
            a, b = 1, 1
        else:
            a, b = -1, 1

        left, lm, rm, right = 0, 0, 0, 0
        l1, l2, r1, r2 = 0, 0, 0, 0

        try:
            for k in range(1, 6):
                if i + a * k < 0 or j + b * k < 0:
                    break
                if enemy[i + a * k][j + b * k] == 1:
                    if r1 == 0:
                        rm += 1
                    else:
                        right += 1
                elif r1 == 0:
                    r1 = k
                else:
                    r2 = k
                    break
        except IndexError:
            pass

        try:
            for k in range(1, 6):
                if i - a * k < 0 or j - b * k < 0:
                    break
                if enemy[i - a * k][j - b * k] == 1:
                    if l1 == 0:
                        lm += 1
                    else:
                        left += 1
                elif l1 == 0:
                    l1 = k
                else:
                    l2 = k
                    break
        except IndexError:
            pass

        return a, b, left, lm, rm, right, l1, l2, r1, r2


    def count_4(self, i, j):
        if self.check_turn():
            me = self.black
            enemy = self.white
        else:
            me = self.white
            enemy = self.black

        me[i][j] = 1
        count = 0

        for c in range(4):
            a, b, left, mid, right, l1, l2, r1, r2 = self.get_9set(i, j, c)

            if mid == 4:
                l_half, r_half = False, False
                if me == self.black:
                    if  left >= 1:
                        l_half = True
                    if  right >= 1:
                        r_half = True

                if l1 == 0 or enemy[i - a * l1][j - b * l1] == 1:
                    l_half = True
                if r1 == 0 or enemy[i + a * r1][j + b * r1] == 1:
                    r_half = True

                if not (l_half and r_half):
                    count += 1

            else:
                if mid + left == 4:
                    if enemy[i - a * l1][j - b * l1] == 0:
                        count += 1
                if mid + right == 4:
                    if enemy[i + a * r1][j + b * r1] == 0:
                        count += 1
                if me == self.white:
                    if mid + left > 4:
                        if enemy[i - a * l1][j - b * l1] == 0:
                            count += 1
                    if mid + right > 4:
                        if enemy[i + a * r1][j + b * r1] == 0:
                            count += 1

        me[i][j] = 0
        return count


    def count_3(self,i, j):
        if self.check_turn():
            me = self.black
            enemy = self.white
        else:
            me = self.white
            enemy = self.black

        me[i][j] = 1
        count = 0

        for c in range(4):
            a, b, left, mid, right, l1, l2, r1, r2 = self.get_9set(i, j, c)

            if left >= 1 and right >= 1:
                continue
            elif l1 == 0 or r1 == 0:
                continue
            elif left >= 1 and left + mid == 3:
                if enemy[i - a * l1][j - b * l1] == 1 or l2 == 0:
                    continue
                elif enemy[i - a * l2][j - b * l2] == 1 or enemy[i + a * r1][j + b * r1] == 1:
                    continue
                else:
                    try:
                        if i - a * l2 - a < 0 or j - b * l2 - b < 0:
                            pass
                        elif me == self.black and me[i - a * l2 - a][j - b * l2 - b] == 1:
                            continue
                    except IndexError:
                        pass

                    if self.check_legal(i - a * l1, j - b * l1)[0]:
                        count += 1
                    else:
                        continue

            elif right >= 1 and right + mid == 3:
                if enemy[i + a * r1][j + b * r1] == 1 or r2 == 0:
                    continue
                elif enemy[i + a * r2][j + b * r2] == 1 or enemy[i - a * l1][j - b * l1] == 1:
                    continue
                else:
                    try:
                        if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                            pass
                        elif me == self.black and me[i + a * r2 + a][j + b * r2 + b] == 1:
                            continue
                    except IndexError:
                        pass

                    if self.check_legal(i + a * r1, j + b * r1)[0]:
                        count += 1
                    else:
                        continue

            elif mid == 3 and left == right == 0:
                if enemy[i - a * l1][j - b * l1] == 1 or enemy[i + a * r1][j + b * r1] == 1:
                    continue

                left_half, right_half = False, False

                if l2 == 0 or enemy[i - a * l2][j - b * l2] == 1:
                    left_half = True
                else:
                    try:
                        if i - a * l2 - a < 0 or j - b * l2 - b < 0:
                            pass
                        elif me == self.black and me[i - a * l2 - a][j - b * l2 - b] == 1:
                            left_half = True
                    except IndexError:
                        pass

                if r2 == 0 or enemy[i + a * r2][j + b * r2] == 1:
                    right_half = True
                else:
                    try:
                        if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                            pass
                        elif me == self.black and me[i + a * r2 + a][j + b * r2 + b] == 1:
                            right_half = True
                    except IndexError:
                        pass

                if left_half == right_half == True:
                    continue
                elif left_half == right_half == False:
                    if self.check_legal(i - a * l1, j - b * l1)[0] or self.check_legal(i + a * r1, j + b * r1)[0]:
                        count += 1
                    else:
                        continue
                elif left_half:
                    if self.check_legal(i + a * r1, j + b * r1)[0]:
                        count += 1
                    else:
                        continue
                elif right_half:
                    if self.check_legal(i - a * l1, j - b * l1)[0]:
                        count += 1
                    else:
                        continue

        me[i][j] = 0

        return count


    def check_44(self, i, j):
        if self.check_turn():
            me = self.black
        else:
            me = self.white

        me[i][j] = 1
        count = 0

        for c in range(4):
            a, b, left, mid, right, l1, l2, r1, r2 = self.get_9set(i, j, c)

            l_half, r_half = False, False
            if mid == 4:
                if left >= 1:
                    l_half = True
                elif l1 == 0:
                    l_half = True
                elif self.white[i - a * l1][j - b * l1] == 1:
                    l_half = True

                if right >= 1:
                    r_half = True
                elif r1 == 0:
                    r_half = True
                elif self.white[i + a * r1][j + b * r1] == 1:
                    r_half = True

                if not(l_half == True and r_half == True):
                    count += 1

            else:
                if mid + left == 4:
                    if self.white[i - a * l1][j - b * l1] == 0:
                        count += 1
                if mid + right == 4:
                    if self.white[i + a * r1][j + b * r1] == 0:
                        count += 1

        me[i][j] = 0
        if count >= 2:
            return True
        return False


    def check_33(self, i, j):
        self.black[i][j] = 1
        count = 0

        for c in range(4):
            a, b, left, mid, right, l1, l2, r1, r2 = self.get_9set(i, j, c)

            if left >= 1 and right >= 1:
                continue
            elif l1 == 0 or r1 == 0:
                continue
            elif left >= 1 and left + mid == 3:
                if self.white[i - a * l1][j - b * l1] == 1 or l2 == 0:
                    continue
                elif self.white[i - a * l2][j - b * l2] == 1 or self.white[i + a * r1][j + b * r1] == 1:
                    continue
                else:
                    try:
                        if i-a*l2-a < 0 or j-b*l2-b < 0:
                            pass
                        elif self.black[i - a * l2 - a][j - b * l2 - b] == 1:
                            continue
                    except IndexError:
                        pass

                    if self.check_legal(i - a * l1, j - b * l1)[0]:
                        count += 1
                    else:
                        continue

            elif right >= 1 and right + mid == 3:
                if self.white[i + a * r1][j + b * r1] == 1 or r2 == 0:
                    continue
                elif self.white[i + a * r2][j + b * r2] == 1 or self.white[i - a * l1][j - b * l1] == 1:
                    continue
                else:
                    try:
                        if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                            pass
                        elif self.black[i + a * r2 + a][j + b * r2 + b] == 1:
                            continue
                    except IndexError:
                        pass

                    if self.check_legal(i + a * r1, j + b * r1)[0]:
                        count += 1
                    else:
                        continue

            elif mid == 3 and left == right == 0:
                if self.white[i - a * l1][j - b * l1] == 1 or  self.white[i + a * r1][j + b * r1] == 1:
                    continue

                left_half, right_half = False, False

                if l2 == 0 or self.white[i - a * l2][j - b * l2] == 1:
                    left_half = True
                else:
                    try:
                        if i - a * l2 - a < 0 or j - b * l2 - b < 0:
                            pass
                        elif self.black[i - a * l2 - a][j - b * l2 - b] == 1:
                            left_half = True
                    except IndexError:
                        pass

                if r2 == 0 or self.white[i + a * r2][j + b * r2] == 1:
                    right_half = True
                else:
                    try:
                        if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                            pass
                        elif self.black[i + a * r2 + a][j + b * r2 + b] == 1:
                            right_half = True
                    except IndexError:
                        pass

                if left_half == right_half == True:
                    continue
                elif left_half == right_half == False:
                    if self.check_legal(i - a * l1,j - b * l1)[0] or self.check_legal(i + a * r1,j + b * r1)[0]:
                        count += 1
                    else:
                        continue
                elif left_half:
                    if self.check_legal(i + a * r1,j + b * r1)[0]:
                        count += 1
                    else:
                        continue
                elif right_half:
                    if self.check_legal(i - a * l1,j - b * l1)[0]:
                        count += 1
                    else:
                        continue

        self.black[i][j] = 0
        if count >= 2:
            return True
        return False


    def check_finish(self, i, j):
        # 4, 3 갯수 세기
        count_4 = self.count_4(i, j)
        count_3 = self.count_3(i, j)

        # 흑의 경우 43
        if self.check_turn():
            if count_4 == 1 and count_3 == 1:
                return True
            else:
                return False
        # 백의 경우 43, 44
        else:
            if count_4 + count_3 >= 2 and count_4 >= 1:
                return True
            else:
                return False


    def check_finish2(self, i, j):
        # 3 갯수 세기
        count_3 = self.count_3(i, j)

        # 백의 33 체크
        if not self.check_turn():
            if count_3 >= 2:
                return True
            else:
                return False
        return False


    def check_defend(self, i, j):
        depend_4 = []

        if self.check_turn():
            enemy = self.white
            me = self.black
        else:
            enemy = self.black
            me = self.white

        for c in range(4):
            if c == 0:
                a, b = 0, 1
            elif c == 1:
                a, b = 1, 0
            elif c == 2:
                a, b = 1, 1
            else:
                a, b = -1, 1

            left, mid, right = 0, 1, 0
            l1, l2, r1, r2 = 0, 0, 0, 0

            try:
                for k in range(1, 6):
                    if i + a * k < 0 or j + b * k < 0:
                        break
                    if enemy[i + a * k][j + b * k] == 1:
                        if r1 == 0:
                            mid += 1
                        else:
                            right += 1
                    elif r1 == 0:
                        r1 = k
                    else:
                        r2 = k
                        break
            except IndexError:
                pass

            try:
                for k in range(1, 6):
                    if i - a * k < 0 or j - b * k < 0:
                        break
                    if enemy[i - a * k][j - b * k] == 1:
                        if l1 == 0:
                            mid += 1
                        else:
                            left += 1
                    elif l1 == 0:
                        l1 = k
                    else:
                        l2 = k
                        break
            except IndexError:
                pass

            if mid == 4:
                l_half, r_half = False, False

                if left >= 1 and not self.check_turn():
                    l_half = True
                elif l1 == 0:
                    l_half = True
                elif me[i - a * l1][j - b * l1] == 1:
                    l_half =  True

                if right >= 1 and not self.check_turn():
                    r_half = True
                elif r1 == 0:
                    r_half = True
                elif me[i + a * r1][j + b * r1] == 1:
                    r_half = True

                if not l_half:
                    depend_4.append((i - a * l1)*15 + j - b * l1)
                if not r_half:
                    depend_4.append((i + a * r1)*15 + j + b * r1)

            else:
                if mid + left == 4:
                    if me[i - a * l1][j - b * l1] == 0:
                        depend_4.append((i - a * l1)*15 + j - b * l1)
                if mid + right == 4:
                    if me[i + a * r1][j + b * r1] == 0:
                        depend_4.append((i + a * r1)*15 + j + b * r1)

        return depend_4


    def check_defend2(self, i, j):
        depend_3 = []

        if self.check_turn():
            enemy = self.white
            me = self.black
        else:
            enemy = self.black
            me = self.white

        for c in range(4):
            if c == 0:
                a, b = 0, 1
            elif c == 1:
                a, b = 1, 0
            elif c == 2:
                a, b = 1, 1
            else:
                a, b = -1, 1

            left, mid, right = 0, 1, 0
            l1, l2, r1, r2 = 0, 0, 0, 0

            try:
                for k in range(1, 5):
                    if i + a * k < 0 or j + b * k < 0:
                        break
                    if enemy[i + a * k][j + b * k] == 1:
                        if r1 == 0:
                            mid += 1
                        else:
                            right += 1
                    elif r1 == 0:
                        r1 = k
                    else:
                        r2 = k
                        break
            except IndexError:
                pass

            try:
                for k in range(1, 5):
                    if i - a * k < 0 or j - b * k < 0:
                        break
                    if enemy[i - a * k][j - b * k] == 1:
                        if l1 == 0:
                            mid += 1
                        else:
                            left += 1
                    elif l1 == 0:
                        l1 = k
                    else:
                        l2 = k
                        break
            except IndexError:
                pass


            if left >= 1 and right >= 1:
                continue
            elif l1 == 0 or r1 == 0:
                continue
            elif left >= 1 and left + mid == 3:
                if me[i - a * l1][j - b * l1] == 1 or l2 == 0:
                    continue
                elif me[i - a * l2][j - b * l2] == 1 or me[i + a * r1][j + b * r1] == 1:
                    continue
                else:
                    try:
                        if i - a * l2 - a < 0 or j - b * l2 - b < 0:
                            pass
                        elif enemy[i - a * l2 - a][j - b * l2 - b] == 1 and self.check_turn() == False:
                            continue
                    except IndexError:
                        pass

                    if self.check_legal(i - a * l1, j - b * l1)[0]:
                        depend_3.append(15*(i-a*l1) + j-b*l1)
                    if self.check_legal(i - a * l2, j - b * l2)[0]:
                        depend_3.append(15 * (i - a * l2) + j - b * l2)
                    if self.check_legal(i + a * r1, j + b * r1)[0]:
                        depend_3.append(15 * (i + a * r1) + j + b * r1)

            elif right >= 1 and right + mid == 3:
                if me[i + a * r1][j + b * r1] == 1 or r2 == 0:
                    continue
                elif me[i + a * r2][j + b * r2] == 1 or me[i - a * l1][j - b * l1] == 1:
                    continue
                else:
                    try:
                        if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                            pass
                        elif enemy[i + a * r2 + a][j + b * r2 + b] == 1 and self.check_turn() == False:
                            continue
                    except IndexError:
                        pass

                    if self.check_legal(i + a * r1, j + b * r1)[0]:
                        depend_3.append(15 * (i + a * r1) + j + b * r1)
                    if self.check_legal(i + a * r2, j + b * r2)[0]:
                        depend_3.append(15 * (i + a * r2) + j + b * r2)
                    if self.check_legal(i - a * l1, j - b * l1)[0]:
                        depend_3.append(15 * (i - a * l1) + j - b * l1)


            elif mid == 3 and left == right == 0:
                if me[i - a * l1][j - b * l1] == 1 or me[i + a * r1][j + b * r1] == 1:
                    continue

                left_half, right_half = False, False

                if l2 == 0 or me[i - a * l2][j - b * l2] == 1:
                    left_half = True
                else:
                    try:
                        if i - a * l2 - a < 0 or j - b * l2 - b < 0:
                            pass
                        elif enemy[i - a * l2 - a][j - b * l2 - b] == 1 and self.check_turn() == False:
                            left_half = True
                    except IndexError:
                        pass

                if r2 == 0 or me[i + a * r2][j + b * r2] == 1:
                    right_half = True
                else:
                    try:
                        if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                            pass
                        elif enemy[i + a * r2 + a][j + b * r2 + b] == 1 and self.check_turn() == False:
                            right_half = True
                    except IndexError:
                        pass

                if left_half == right_half == True:
                    continue
                elif left_half == right_half == False:
                    if self.check_legal(i - a * l1, j - b * l1)[0]:
                        depend_3.append(15 * (i - a * l1) + j - b * l1)
                    if self.check_legal(i + a * r1, j + b * r1)[0]:
                        depend_3.append(15 * (i + a * r1) + j + b * r1)
                elif left_half:
                    if self.check_legal(i + a * r1, j + b * r1)[0]:
                        depend_3.append(15 * (i + a * r1) + j + b * r1)
                elif right_half:
                    if self.check_legal(i - a * l1, j - b * l1)[0]:
                        depend_3.append(15 * (i - a * l1) + j - b * l1)

        return depend_3


    def defend_list(self):
        defend_action = []

        if self.check_turn():
            me = self.black
            enemy = self.white
        else:
            me = self.white
            enemy = self.black

        for i in range(15):
            for j in range(15):
                if enemy[i][j] == 1:
                    for k in self.check_defend(i, j):
                        if k not in defend_action and self.check_legal(k // 15, k % 15)[0]:
                            defend_action.append(k)

        return defend_action


    def defend_list2(self):
        defend_action = []

        if self.check_turn():
            me = self.black
            enemy = self.white
        else:
            me = self.white
            enemy = self.black

        for i in range(15):
            for j in range(15):
                if enemy[i][j] == 1:
                    for k in self.check_defend2(i, j):
                        if k not in defend_action and self.check_legal(k // 15, k % 15)[0]:
                            defend_action.append(k)

        return defend_action


    def check_attack(self, i, j):
        attack = []

        if self.check_turn():
            enemy = self.white
            me = self.black
        else:
            enemy = self.black
            me = self.white

        for c in range(4):
            if c == 0:
                a, b = 0, 1
            elif c == 1:
                a, b = 1, 0
            elif c == 2:
                a, b = 1, 1
            else:
                a, b = -1, 1

            left, mid, right = 0, 1, 0
            l1, l2, r1, r2 = 0, 0, 0, 0

            try:
                for k in range(1, 5):
                    if i + a * k < 0 or j + b * k < 0:
                        break
                    if me[i + a * k][j + b * k] == 1:
                        if r1 == 0:
                            mid += 1
                        else:
                            right += 1
                    elif r1 == 0:
                        r1 = k
                    else:
                        r2 = k
                        break
            except IndexError:
                pass

            try:
                for k in range(1, 5):
                    if i - a * k < 0 or j - b * k < 0:
                        break
                    if me[i - a * k][j - b * k] == 1:
                        if l1 == 0:
                            mid += 1
                        else:
                            left += 1
                    elif l1 == 0:
                        l1 = k
                    else:
                        l2 = k
                        break
            except IndexError:
                pass

            if left >= 1 and right >= 1:
                continue
            elif l1 == 0 or r1 == 0:
                continue
            elif left >= 1 and left + mid == 3:
                if enemy[i - a * l1][j - b * l1] == 1 or l2 == 0:
                    continue
                elif enemy[i - a * l2][j - b * l2] == 1 or enemy[i + a * r1][j + b * r1] == 1:
                    continue
                else:
                    try:
                        if i - a * l2 - a < 0 or j - b * l2 - b < 0:
                            pass
                        elif me[i - a * l2 - a][j - b * l2 - b] == 1:
                            continue
                    except IndexError:
                        pass

                    if self.check_legal(i - a * l1, j - b * l1)[0]:
                        attack.append((i - a * l1)*15 + j - b * l1)
                    else:
                        continue

            elif right >= 1 and right + mid == 3:
                if enemy[i + a * r1][j + b * r1] == 1 or r2 == 0:
                    continue
                elif enemy[i + a * r2][j + b * r2] == 1 or enemy[i - a * l1][j - b * l1] == 1:
                    continue
                else:
                    try:
                        if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                            pass
                        elif me[i + a * r2 + a][j + b * r2 + b] == 1:
                            continue
                    except IndexError:
                        pass

                    if self.check_legal(i + a * r1, j + b * r1)[0]:
                        attack.append((i + a * r1)*15 + j + b * r1)
                    else:
                        continue

            elif mid == 3 and left == right == 0:
                if enemy[i - a * l1][j - b * l1] == 1 or enemy[i + a * r1][j + b * r1] == 1:
                    continue

                left_half, right_half = False, False

                if l2 == 0 or enemy[i - a * l2][j - b * l2] == 1:
                    left_half = True
                else:
                    try:
                        if i - a * l2 - a < 0 or j - b * l2 - b < 0:
                            pass
                        elif me[i - a * l2 - a][j - b * l2 - b] == 1:
                            left_half = True
                    except IndexError:
                        pass

                if r2 == 0 or enemy[i + a * r2][j + b * r2] == 1:
                    right_half = True
                else:
                    try:
                        if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                            pass
                        elif me[i + a * r2 + a][j + b * r2 + b] == 1:
                            right_half = True
                    except IndexError:
                        pass

                if left_half == right_half == True:
                    continue
                elif left_half == right_half == False:
                    if self.check_legal(i - a * l1,j - b * l1)[0]:
                        attack.append((i - a * l1)*15 + j - b * l1)
                    if self.check_legal(i + a * r1, j + b * r1)[0]:
                        attack.append((i + a * r1) * 15 + j + b * r1)
                elif left_half:
                    if self.check_legal(i + a * r1,j + b * r1)[0]:
                        attack.append((i + a * r1)*15 + j + b * r1)
                    else:
                        continue
                elif right_half:
                    if self.check_legal(i - a * l1,j - b * l1)[0]:
                        attack.append((i - a * l1)*15 + j - b * l1)
                    else:
                        continue

        return attack