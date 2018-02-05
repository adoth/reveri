import wx
import itertools
import computer_put
import bord

eight_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
black = 'black'
white = 'white'
green = 'green'


class Reversi(bord.MainFrame):
    def __init__(self):
        super().__init__()
        self.radio_box.Bind(wx.EVT_RADIOBOX, self.get_radio_box_selection)
        self.start_button.Bind(wx.EVT_BUTTON, self.reset_setting)
        self.redo_button.Bind(wx.EVT_BUTTON, self.redo)
        self.pass_button.Bind(wx.EVT_BUTTON, self.pass_turn)
        self.monte = self.redo_bord = [[self.get_square_color((i, j)) for i in range(10)] for j in range(10)]
        self.n = 4
        for i, j in itertools.product(range(10), repeat=2):
            self.square_array[i][j].Bind(wx.EVT_LEFT_UP, self.on_bord_click)

    def on_bord_click(self, event):
        self.redo_bord = [[self.get_square_color((i, j)) for i in range(10)] for j in range(10)]
        obj = event.GetEventObject()
        pos = obj.pos_index
        if self.put_stone(pos):
            if not self.end_dialog():
                self.change_color()
                self.monte = [[self.get_square_color((i, j)) for i in range(10)] for j in range(10)]
                self.put_computer()
                self.end_dialog()
                self.change_color()

    def put_computer(self):
        # if self.n < 50:
        #     put_pos = monte.random_put(self.monte, self.now_color)
        # else:
        put_pos = computer_put.monte(self.monte, self.now_color, self.n)
        if put_pos:
            # print('computer put on : {} {}'.format(put_pos[0]+1, put_pos[1]+1))
            self.put_stone(put_pos)
        elif not put_pos:
            box = wx.MessageDialog(None, 'computer pss', 'pass', wx.OK)
            box.ShowModal()

    def put_stone(self, pos):
        rev_block = self.get_rev_block((pos[0], pos[1]))
        if rev_block:
            self.set_square_color((pos[0], pos[1]), self.now_color, put=True)
            for rev in rev_block:
                self.set_square_color((rev[0], rev[1]), self.now_color, put=True)
            self.n += 1
            return True
        return False

    def get_rev_block(self, pos) -> list:
        enemy_color = [white, black][self.now_color == white]
        rev_block = []
        for direction in eight_directions:
            enemy_block = []
            square = self.get_square_color(pos, direction=direction)
            if square == enemy_color:
                enemy_block.append((pos[0]+direction[0], pos[1]+direction[1]))
                rev_block.append(self.sandwich((pos[0]+direction[0], pos[1]+direction[1]), direction, enemy_block))
            else:
                continue
        rev_block = [i for j in rev_block for i in j]
        return rev_block

    def sandwich(self, pos, direction, enemy_block) -> list:
        for i in range(1, 10):
            square = (pos[0] + direction[0]*i, pos[1] + direction[1]*i)
            square_color = self.get_square_color(square)
            if square_color == green or not (0 <= square[0] < 10) or not(0 <= square[1] < 10):
                break
            elif square_color == self.now_color:
                return enemy_block
            else:
                enemy_block.append(square)
        return []

    def get_radio_box_selection(self, _):
        radio_select = self.radio_box.GetSelection()
        if radio_select == 0:
            self.first_player = 'I'
            self.second_player = 'Computer'
        elif radio_select == 1:
            self.first_player = 'Computer'
            self.second_player = 'I'
        elif radio_select == 2:
            self.first_player = 'Computer'
            self.second_player = 'Computer'

    def reset_setting(self, _):
        for i, j in itertools.product(range(10), repeat=2):
            self.set_square_color((i, j), green, put=False)
        self.set_square_color((4, 4), white, put=True)
        self.set_square_color((4, 5), black, put=True)
        self.set_square_color((5, 4), black, put=True)
        self.set_square_color((5, 5), white, put=True)
        self.now_color = black

        if self.first_player == 'Computer' and self.second_player == 'Computer':
            while True:
                self.put_computer()
                self.change_color()
                if self.end_dialog():
                    break
        elif self.first_player == 'Computer':
            self.put_stone((6, 5))
            self.now_color = white

    def redo(self, _):
        for i, j in itertools.product(range(10), repeat=2):
            color = self.redo_bord[i][j]
            if color == green:
                self.set_square_color((j, i), color, put=False)
            else:
                self.set_square_color((j, i), color, put=True)

    def pass_turn(self, _):
        can_put_list = []
        for i, j in itertools.product(range(10), repeat=2):
            if self.get_rev_block((i, j)) and self.get_square_color((i, j)) == green:
                can_put_list.append((i, j))
        if can_put_list:
            print(can_put_list)

        else:
            self.change_color()
            self.put_computer()
            self.change_color()

    def change_color(self):
        self.now_color = [white, black][self.now_color == white]

    def end_dialog(self):
        bord_color = [self.get_square_color((i, j)) for i, j in itertools.product(range(10), repeat=2)]
        if len(set(bord_color)) <= 2:
            black_num = bord_color.count(black)
            white_num = bord_color.count(white)
            box = wx.MessageDialog(None, """終わり\n黒 {} \n白 {}""".format(black_num, white_num), 'end')
            box.ShowModal()
            return True
        return False


if __name__ == "__main__":
    app = wx.App()
    frame = Reversi().Show()
    app.MainLoop()
