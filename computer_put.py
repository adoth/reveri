import itertools
from random import randint


white = 'white'
black = 'black'
green = 'green'
eight_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
N = 300


class Monte:
    def __init__(self, bord, color):
        self.square_array = [[bord[i][j] for i in range(10)] for j in range(10)]
        self.now_color = color

    def play_one(self, n):
        for i in range(100 - n):
            self.on_computer()
            self.now_color = [white, black][self.now_color == white]
        return self.square_array

    def put_stone(self, pos) -> list:
        rev_block = self.get_rev_block((pos[0], pos[1]))
        if rev_block:
            self.set_square_color((pos[0], pos[1]), self.now_color)
            for rev in rev_block:
                self.set_square_color((rev[0], rev[1]), self.now_color)
            return self.square_array

        else:
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
            if square_color == green or not (0 <= square[0] < 10) or not (0 <= square[1] < 10):
                break
            elif square_color == self.now_color:
                return enemy_block
            else:
                enemy_block.append(square)
        return []

    def can_put_list(self) -> list:
        can_put_list = []
        for i, j in itertools.product(range(10), repeat=2):
            if self.get_rev_block((i, j)) and self.get_square_color((i, j)) == green:
                can_put_list.append((i, j))
        return can_put_list

    def on_computer(self, pos=None):
        can_put_list = self.can_put_list()
        if pos:
            put_pos = pos
            self.put_stone(put_pos)

        elif can_put_list:
            put_pos = can_put_list[randint(0, len(can_put_list) - 1)]
            self.put_stone(put_pos)
        return self.square_array

    def set_square_color(self, pos, color, *, direction=(0, 0)):
        self.square_array[pos[0] + direction[0]][pos[1] + direction[1]] = color

    def get_square_color(self, pos, *, direction=(0, 0)) -> str:
        if 0 <= pos[0] + direction[0] < 10 and 0 <= pos[1] + direction[1] < 10:
            color = self.square_array[pos[0] + direction[0]][pos[1] + direction[1]]
        else:
            color = "none"
        return color

    def reset_bord(self, re_bord, color):
        for i, j in itertools.product(range(10), repeat=2):
            self.square_array[i][j] = re_bord[i][j]
        self.now_color = color


def random_put(bord, color):
    can_put = Monte(bord, color).can_put_list()
    if can_put:
        return can_put[randint(0, len(can_put) - 1)]


def monte(bord, color, n):
    start_color = color
    now_color = color
    can_put = Monte(bord, color).can_put_list()
    if not can_put:
        return []
    elif len(can_put) == 1:
        return can_put[0]
    else:
        ans = []
        even = N // len(can_put)
        for pos in can_put:
            win = 0
            for i in range(even):
                put_bord = Monte(bord, now_color).on_computer(pos=pos)
                tmp_bord = Monte(put_bord, now_color)
                result = [i for j in tmp_bord.play_one(n) for i in j]
                win += [0, 1][result.count(start_color) > 50]
            ans.append(win/even)
    return can_put[ans.index(max(ans))]
