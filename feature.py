from time import time

def get_features(state):
    t = time()
    legal_features = get_legal_feature(state)
    my_feature_4 = make_list(0)
    my_feature_3 = make_list(0)
    my_feature_2 = make_list(0)
    enemy_feature_4 = make_list(0)
    enemy_feature_3 = make_list(0)
    enemy_feature_2 = make_list(0)

    if state.check_turn():
        me = state.black
        enemy = state.white
    else:
        me = state.white
        enemy = state.black

    for i in range(15):
        for j in range(15):
            if me[i][j] == 0 and enemy[i][j] == 0:
                if state.check_legal(i, j)[0]:
                    feature_4, feature_3, feature_2 = convert_me(state, i, j)
                    if feature_4:
                        my_feature_4[i][j] = 1
                    if feature_3:
                        my_feature_3[i][j] = 1
                    if feature_2:
                        my_feature_2[i][j] = 1

                    if feature_4:
                        enemy_feature_4[i][j] = 1
                    if feature_3:
                        enemy_feature_3[i][j] = 1
                    if feature_2:
                        enemy_feature_2[i][j] = 1
    return legal_features, my_feature_4, my_feature_3, my_feature_2, enemy_feature_4, enemy_feature_3, enemy_feature_2


def convert_me(state, i, j):
    feature_4 = False
    feature_3 = False
    feature_2 = False

    if state.check_turn():
        me = state.black
        enemy = state.white
    else:
        me = state.white
        enemy = state.black

    for c in range(4):
        a, b, left, lm, rm, right, l1, l2, r1, r2 = state.get_10set(i, j, c)
        mid = lm + rm + 1

        # 4를 체크 (놓으면 5)
        if mid == 5:
            feature_4 = True
        elif not state.check_turn() and mid > 5:
            feature_4 = True

        # 3을 체크 (놓으면 4)
        if mid == 4:
            l_half, r_half = False, False
            if state.check_turn():
                if left >= 1:
                    l_half = True
                if right >= 1:
                    r_half = True

            if l1 == 0 or enemy[i - a * l1][j - b * l1] == 1:
                l_half = True
            if r1 == 0 or enemy[i + a * r1][j + b * r1] == 1:
                r_half = True

            if not (l_half and r_half):
                feature_3 = True

        else:
            if mid + left == 4:
                if enemy[i - a * l1][j - b * l1] == 0:
                    feature_3 = True
            if mid + right == 4:
                if enemy[i + a * r1][j + b * r1] == 0:
                    feature_3 = True
            if not state.check_turn():
                if mid + left > 4:
                    if enemy[i - a * l1][j - b * l1] == 0:
                        feature_3 = True
                if mid + right > 4:
                    if enemy[i + a * r1][j + b * r1] == 0:
                        feature_3 = True

        # 2를 체크 (놓으면 3)
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
                    elif state.check_turn() and me[i - a * l2 - a][j - b * l2 - b] == 1:
                        continue
                except IndexError:
                    pass

                if state.check_legal(i - a * l1, j - b * l1)[0]:
                    feature_2 = True
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
                    elif state.check_turn() and me[i + a * r2 + a][j + b * r2 + b] == 1:
                        continue
                except IndexError:
                    pass

                if state.check_legal(i + a * r1, j + b * r1)[0]:
                    feature_2 = True
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
                    elif state.check_turn() and me[i - a * l2 - a][j - b * l2 - b] == 1:
                        left_half = True
                except IndexError:
                    pass

            if r2 == 0 or enemy[i + a * r2][j + b * r2] == 1:
                right_half = True
            else:
                try:
                    if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                        pass
                    elif state.check_turn() and me[i + a * r2 + a][j + b * r2 + b] == 1:
                        right_half = True
                except IndexError:
                    pass

            if left_half == right_half == True:
                continue
            elif left_half == right_half == False:
                if state.check_legal(i - a * l1, j - b * l1)[0] or state.check_legal(i + a * r1, j + b * r1)[0]:
                    feature_2 = True
                else:
                    continue
            elif left_half:
                if state.check_legal(i + a * r1, j + b * r1)[0]:
                    feature_2 = True
                else:
                    continue
            elif right_half:
                if state.check_legal(i - a * l1, j - b * l1)[0]:
                    feature_2 = True
                else:
                    continue
    return feature_4, feature_3, feature_2


def convert_enemy(state, i, j):
    feature_4 = False
    feature_3 = False

    if state.check_turn():
        me = state.black
        enemy = state.white
    else:
        me = state.white
        enemy = state.black

    for c in range(4):
        a, b, left, lm, rm, right, l1, l2, r1, r2 = state.get_e10set(i, j, c)
        mid = lm + rm + 1

        # 4를 체크
        if mid == 4:
            l_half, r_half = False, False

            if left >= 1 and not state.check_turn():
                l_half = True
            elif l1 == 0:
                l_half = True
            elif me[i - a * l1][j - b * l1] == 1:
                l_half =  True

            if right >= 1 and not state.check_turn():
                r_half = True
            elif r1 == 0:
                r_half = True
            elif me[i + a * r1][j + b * r1] == 1:
                r_half = True

            if not l_half or not r_half:
                feature_4 = True
                continue

        else:
            if mid + left == 4:
                if me[i - a * l1][j - b * l1] == 0:
                    feature_4 = True
                    continue
            elif mid + left > 4 and state.check_turn():
                if me[i - a * l1][j - b * l1] == 0:
                    feature_4 = True
                    continue

            if mid + right == 4:
                if me[i + a * r1][j + b * r1] == 0:
                    feature_4 = True
                    continue
            elif mid + right > 4 and state.check_turn():
                if me[i + a * r1][j + b * r1] == 0:
                    feature_4 = True
                    continue

        # 3을 체크
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
                    elif enemy[i - a * l2 - a][j - b * l2 - b] == 1 and state.check_turn() == False:
                        continue
                except IndexError:
                    pass
                feature_3 = True

        elif right >= 1 and right + mid == 3:
            if me[i + a * r1][j + b * r1] == 1 or r2 == 0:
                continue
            elif me[i + a * r2][j + b * r2] == 1 or me[i - a * l1][j - b * l1] == 1:
                continue
            else:
                try:
                    if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                        pass
                    elif enemy[i + a * r2 + a][j + b * r2 + b] == 1 and state.check_turn() == False:
                        continue
                except IndexError:
                    pass
                feature_3 = True

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
                    elif enemy[i - a * l2 - a][j - b * l2 - b] == 1 and state.check_turn() == False:
                        left_half = True
                except IndexError:
                    pass

            if r2 == 0 or me[i + a * r2][j + b * r2] == 1:
                right_half = True
            else:
                try:
                    if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                        pass
                    elif enemy[i + a * r2 + a][j + b * r2 + b] == 1 and state.check_turn() == False:
                        right_half = True
                except IndexError:
                    pass

            if left_half == right_half == True:
                continue
            feature_3 = True

    return feature_4, feature_3


def convert_enemy2(state, i, j):
    feature_4 = False
    feature_3 = False
    feature_2 = False

    if state.check_turn():
        me = state.white
        enemy = state.black
    else:
        me = state.black
        enemy = state.white

    for c in range(4):
        a, b, left, lm, rm, right, l1, l2, r1, r2 = state.get_10set(i, j, c)
        mid = lm + rm + 1

        # 4를 체크 (놓으면 5)
        if mid == 5:
            feature_4 = True
        elif not state.check_turn() and mid > 5:
            feature_4 = True

        # 3을 체크 (놓으면 4)
        if mid == 4:
            l_half, r_half = False, False
            if state.check_turn():
                if left >= 1:
                    l_half = True
                if right >= 1:
                    r_half = True

            if l1 == 0 or enemy[i - a * l1][j - b * l1] == 1:
                l_half = True
            if r1 == 0 or enemy[i + a * r1][j + b * r1] == 1:
                r_half = True

            if not (l_half and r_half):
                feature_3 = True

        else:
            if mid + left == 4:
                if enemy[i - a * l1][j - b * l1] == 0:
                    feature_3 = True
            if mid + right == 4:
                if enemy[i + a * r1][j + b * r1] == 0:
                    feature_3 = True
            if not state.check_turn():
                if mid + left > 4:
                    if enemy[i - a * l1][j - b * l1] == 0:
                        feature_3 = True
                if mid + right > 4:
                    if enemy[i + a * r1][j + b * r1] == 0:
                        feature_3 = True

        # 2를 체크 (놓으면 3)
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
                    elif state.check_turn() and me[i - a * l2 - a][j - b * l2 - b] == 1:
                        continue
                except IndexError:
                    pass

                if state.check_legal(i - a * l1, j - b * l1)[0]:
                    feature_2 = True
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
                    elif state.check_turn() and me[i + a * r2 + a][j + b * r2 + b] == 1:
                        continue
                except IndexError:
                    pass

                if state.check_legal(i + a * r1, j + b * r1)[0]:
                    feature_2 = True
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
                    elif state.check_turn() and me[i - a * l2 - a][j - b * l2 - b] == 1:
                        left_half = True
                except IndexError:
                    pass

            if r2 == 0 or enemy[i + a * r2][j + b * r2] == 1:
                right_half = True
            else:
                try:
                    if i + a * r2 + a < 0 or j + b * r2 + b < 0:
                        pass
                    elif state.check_turn() and me[i + a * r2 + a][j + b * r2 + b] == 1:
                        right_half = True
                except IndexError:
                    pass

            if left_half == right_half == True:
                continue
            elif left_half == right_half == False:
                if state.check_legal(i - a * l1, j - b * l1)[0] or state.check_legal(i + a * r1, j + b * r1)[0]:
                    feature_2 = True
                else:
                    continue
            elif left_half:
                if state.check_legal(i + a * r1, j + b * r1)[0]:
                    feature_2 = True
                else:
                    continue
            elif right_half:
                if state.check_legal(i - a * l1, j - b * l1)[0]:
                    feature_2 = True
                else:
                    continue
    return feature_4, feature_3, feature_2


def make_list(n):
    m = []
    for i in range(15):
        m.append([n]*15)
    return m


def get_legal_feature(state):
    legal_map = make_list(1)

    for i in range(15):
        for j in range(15):
            if state.black[i][j] == 1 or state.white[i][j] == 1:
                legal_map[i][j] = 0

    if not state.check_turn():
        return legal_map

    illegal_list = state.referee()[1]
    for i in illegal_list:
        j = i[0]
        r, c = j//15, j%15
        legal_map[r][c] = 0

    return legal_map


def get_connect_feature(state):
    connect_map = make_list(0)

    if state.check_turn():
        me = state.black
        enemy = state.white
    else:
        me = state.white
        enemy = state.black

    for i in range(15):
        for j in range(15):
            if me[i][j] == 1 or enemy[i][j] == 1:
                continue

            # left
            if me[i][j-1] == 1 and j>0:
                connect_map[i][j] += 1
            elif me[i][j-2] == 1 and enemy[i][j-1] == 0 and j>1:
                connect_map[i][j] += 1
            elif me[i][j-3] == 1 and enemy[i][j-1] == 0 and enemy[i][j-2] == 0 and j>2:
                connect_map[i][j] += 1

            # right
            if j<14 and me[i][j+1] == 1:
                connect_map[i][j] += 1
            elif j<13 and me[i][j+2] == 1 and enemy[i][j+1] == 0:
                connect_map[i][j] += 1
            elif j<12 and me[i][j+3] == 1 and enemy[i][j+1] == 0 and enemy[i][j+2] == 0:
                connect_map[i][j] += 1

            # up
            if me[i-1][j] == 1 and i > 0:
                connect_map[i][j] += 1
            elif me[i-2][j] == 1 and enemy[i-1][j] == 0 and i > 1:
                connect_map[i][j] += 1
            elif me[i-3][j] == 1 and enemy[i-1][j] == 0 and enemy[i-2][j] == 0 and i > 2:
                connect_map[i][j] += 1

            # down
            if i < 14 and me[i+1][j] == 1:
                connect_map[i][j] += 1
            elif i < 13 and me[i+2][j] == 1 and enemy[i+1][j] == 0:
                connect_map[i][j] += 1
            elif i < 12 and me[i+3][j] == 1 and enemy[i+1][j] == 0 and enemy[i+2][j] == 0:
                connect_map[i][j] += 1

            # lu
            if me[i-1][j-1] == 1 and i > 0 and j > 0:
                connect_map[i][j] += 1
            elif me[i-2][j-2] == 1 and enemy[i-1][j-1] == 0 and i > 1 and j > 1:
                connect_map[i][j] += 1
            elif me[i-3][j-3] == 1 and enemy[i-1][j-1] == 0 and enemy[i-2][j-2] == 0 and i > 2 and j > 2:
                connect_map[i][j] += 1

            # ld
            if i < 14 and me[i + 1][j-1] == 1 and j > 0:
                connect_map[i][j] += 1
            elif i < 13 and me[i + 2][j-2] == 1 and enemy[i + 1][j-1] == 0 and j > 1:
                connect_map[i][j] += 1
            elif i < 12 and me[i + 3][j-3] == 1 and enemy[i + 1][j-1] == 0 and enemy[i + 2][j-2] == 0 and j > 2:
                connect_map[i][j] += 1

            # ru
            if j<14 and me[i-1][j+1] == 1 and i > 0:
                connect_map[i][j] += 1
            elif j<13 and me[i-2][j+2] == 1 and enemy[i-1][j+1] == 0 and i > 1:
                connect_map[i][j] += 1
            elif j<12 and me[i-3][j+3] == 1 and enemy[i-1][j+1] == 0 and enemy[i-2][j+2] == 0 and i > 2:
                connect_map[i][j] += 1

            # rd
            if i < 14 and j < 14 and me[i+1][j+1] == 1:
                connect_map[i][j] += 1
            elif i < 13 and j < 13 and me[i+2][j+2] == 1 and enemy[i+1][j+1] == 0:
                connect_map[i][j] += 1
            elif i < 12 and j < 12 and me[i+3][j+3] == 1 and enemy[i+1][j+1] == 0 and enemy[i+2][j+2] == 0:
                connect_map[i][j] += 1

    return connect_map
