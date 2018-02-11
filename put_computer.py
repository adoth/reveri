import itertools
from random import randint
from time import time, sleep

white = 'white'
black = 'black'
green = 'green'
eight_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
N = 100
sumi = {(0, 0), (0, 9), (9, 0), (9, 9)}
danger = {(1, 1), (1, 8), (8, 1), (8, 8)}


class Monte:
    def __init__(self, bord, color):
        self.square_array = [[bord[i][j] for i in range(10)] for j in range(10)]
        self.now_color = color

    def play_one(self, n):
        for i in range(100 - n):
            self.put_computer()
            self.now_color = [white, black][self.now_color == white]
        return self.square_array

    def get_rev_block(self, pos) -> list:
        enemy_color = [white, black][self.now_color == white]
        rev_block = []
        for direction in eight_directions:
            square = self.get_square_color(pos, direction=direction)
            if square == enemy_color:
                rev_block.append(self.sandwich((pos[0] + direction[0], pos[1] + direction[1]), direction))

        rev_block = [i for j in rev_block for i in j]
        return rev_block

    def sandwich(self, pos, direction) -> list:
        enemy_block = [pos]
        for i in range(1, 10):
            square = (pos[0] + direction[0] * i, pos[1] + direction[1] * i)
            square_color = self.get_square_color(square)
            if square_color == green or square_color == 'none':
                break
            elif square_color == self.now_color:
                return enemy_block
            else:
                enemy_block.append(square)
        return []

    def can_put_list(self) -> (list, dict):
        can_put_list = []
        can_put_dic = dict()
        for i, j in itertools.product(range(10), repeat=2):
            rev_block = self.get_rev_block((i, j))
            if rev_block and self.get_square_color((i, j)) == green:
                rev_block.append((i, j))
                can_put_dic[(i, j)] = rev_block
                can_put_list.append((i, j))
        return can_put_list, can_put_dic

    def put_computer(self, pos=None):
        can_put_list, can_put_dic = self.can_put_list()
        if pos:
            rev_block = can_put_dic[pos]
            self.set_square_color((pos[0], pos[1]), self.now_color)
            for rev in rev_block:
                self.set_square_color((rev[0], rev[1]), self.now_color)

        elif can_put_list:
            put_pos = can_put_list[randint(0, len(can_put_list) - 1)]
            self.set_square_color((put_pos[0], put_pos[1]), self.now_color)
            pos = can_put_dic[put_pos]
            for rev in pos:
                self.set_square_color((rev[0], rev[1]), self.now_color)
        return self.square_array

    def set_square_color(self, pos, color, *, direction=(0, 0)):
        self.square_array[pos[0] + direction[0]][pos[1] + direction[1]] = color

    def get_square_color(self, pos, *, direction=(0, 0)) -> str:
        if 0 <= pos[0] + direction[0] < 10 and 0 <= pos[1] + direction[1] < 10:
            color = self.square_array[pos[0] + direction[0]][pos[1] + direction[1]]
        else:
            color = "none"
        return color


def monte(bord, color, n, can_put):
    print(can_put)
    start = time()
    start_color = color
    enemy_color = [black, white][start_color == black]
    ans = []
    even = N // len(can_put)
    for pos in can_put:
        win = 0
        put_bord = Monte(bord, start_color).put_computer(pos=pos)
        now_color = [black, white][start_color == black]
        tmp_bord = Monte(put_bord, now_color)
        for i in range(even):
            result = tmp_bord.play_one(n)
            result = [i for j in result for i in j]
            win += [0, 1][result.count(start_color) > result.count(enemy_color)]
            tmp_bord = Monte(put_bord, now_color)
        ans.append(win / even)

    print(ans)
    print(time() - start)
    return can_put[ans.index(max(ans))]


def main(bord, color, n):
    can_put, can_dic = Monte(bord, color).can_put_list()
    danger_minus = list(set(can_put) - danger)
    if not can_put:
        return []
    elif sumi & set(can_put):
        change_list = list(sumi & set(can_put))
        pos = change_list[randint(0, len(change_list) - 1)]
    elif len(can_put) == 1:
        pos = can_put[0]
    elif not danger_minus:
        pos = monte(bord, color, n, can_put)
    elif len(danger_minus) == 1:
        pos = danger_minus[0]
    else:
        pos = monte(bord, color, n, list(danger_minus))
    print(pos)
    return can_dic[pos]
