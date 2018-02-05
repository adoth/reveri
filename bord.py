import wx
import itertools

black = 'black'
white = 'white'
green = 'green'


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, size=(900, 800))

        bord = wx.Panel(self, wx.ID_ANY, pos=(0, 0), size=(760, 800))
        self.bord = bord
        radio_panel = SubPanel(self, pos=(760, 400), size=(200, 100))
        self.radio_panel = radio_panel
        start_btm = SubPanel(self, pos=(760, 500), size=(200, 100))
        self.start_button = start_btm
        return_btm = SubPanel(self, pos=(760, 600), size=(200, 100))
        pass_btm = SubPanel(self, pos=(760, 700), size=(200, 100))

        square_array = [[None for _ in range(10)] for _ in range(10)]
        self.square_array = square_array
        square_layout = [[0 for _ in range(10)] for _ in range(10)]
        self.square_layout = square_layout

        radio_box = wx.RadioBox(radio_panel, wx.ID_ANY, '先行・後攻',
                                choices=('先行:黒', '後攻:白'), style=wx.RA_SPECIFY_ROWS)
        self.radio_box = radio_box
        start_button = wx.Button(start_btm, wx.ID_ANY, 'START')
        self.start_button = start_button
        redo_button = wx.Button(return_btm, wx.ID_ANY, 'RETURN')
        self.redo_button = redo_button
        pass_button = wx.Button(pass_btm, wx.ID_ANY, 'PASS')
        self.pass_button = pass_button

        now_color = black
        self.now_color = now_color

        self.first_player = 'I'
        self.second_player = 'Computer'

        # create bord
        for i, j in itertools.product(range(10), repeat=2):
                square_array[i][j] = VanillaBord(bord, (i, j), (76 * i, 76 * j))
                self.set_square_color((i, j), green, put=True)
        self.bord_color = None

    def set_square_color(self, pos,  color, *, direction=(0, 0), put):
        self.square_array[pos[0] + direction[0]][pos[1] + direction[1]].color = color

        self.square_array[pos[0] + direction[0]][pos[1] + direction[1]].SetBackgroundColour(color)
        if put:
            self.square_array[pos[0] + direction[0]][pos[1] + direction[1]].Disable()
        else:
            self.square_array[pos[0] + direction[0]][pos[1] + direction[1]].Enable()
        self.Refresh()

    def get_square_color(self, pos, *, direction=(0, 0)) -> str:
        if 0 <= pos[0] + direction[0] < 10 and 0 <= pos[1] + direction[1] < 10:
            color = self.square_array[pos[0] + direction[0]][pos[1] + direction[1]].color
        else:
            color = "none"
        return color


class SubPanel(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, pos=pos, size=size)


class VanillaBord(wx.Panel):
    def __init__(self, parent, index, pos):
        wx.Panel.__init__(self, parent, pos=pos, size=(74, 74))
        self.pos_index = index
        self.color = green
