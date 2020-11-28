import wx
import math
import numpy as np

# TODO Reduce side effects and make methods more pure


class CellularWindow(wx.Window):

    _grid_size = None
    _grid_line_list = []
    _square_list = []
    _current_state = None
    _next_state = None

    def __init__(self, parent, grid_size, *args, **kwargs):
        wx.Window.__init__(self, parent, *args, **kwargs)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.build_grid_lines)
        self.adjust_grid_size(grid_size)
        self.randomly_populate_grid()

    def increment_time_step(self):
        self.build_squares()

    def randomly_populate_grid(self):
        self._current_state = np.random.randint(
            0, high=2, size=(self._grid_size, self._grid_size), dtype=bool
        )

    def adjust_grid_size(self, length):
        self._grid_size = length
        self.randomly_populate_grid()
        self.SendSizeEvent()

    def build_squares(self):
        self._square_list.clear()
        grid_spacing = self.get_grid_spacing()
        for i in range(0, self._grid_size):
            for j in range(0, self._grid_size):
                if self._current_state[i, j]:
                    x = i * grid_spacing
                    y = j * grid_spacing
                    w = grid_spacing
                    h = grid_spacing
                    self._square_list.append((x, y, w, h))
        self.Refresh()

    def build_grid_lines(self, event):
        # pylint: disable=unused-argument
        self._grid_line_list.clear()
        grid_spacing = self.get_grid_spacing()
        for i in range(0, self._grid_size + 1):
            # Vertical lines
            x_1 = i * grid_spacing
            y_1 = 0
            x_2 = x_1
            y_2 = self._grid_size * grid_spacing
            self._grid_line_list.append((x_1, y_1, x_2, y_2))

            # Horizontal lines
            x_1 = 0
            y_1 = i * grid_spacing
            x_2 = self._grid_size * grid_spacing
            y_2 = y_1
            self._grid_line_list.append((x_1, y_1, x_2, y_2))

        self.build_squares()

    def get_grid_spacing(self):
        self.GetSize()
        min_pixels = min(self.GetSize())
        grid_spacing = math.floor(min_pixels / self._grid_size)
        return grid_spacing

    def zero_grid(self):
        self._current_state = np.zeros((self._grid_size, self._grid_size), dtype=bool)
        self._next_state = np.zeros((self._grid_size, self._grid_size), dtype=bool)

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        # Draw grid
        dc.DrawLineList(self._grid_line_list, wx.Pen(wx.BLACK, 1))
        # Draw Rectangles
        dc.DrawRectangleList(self._square_list, wx.Pen(wx.RED, 1))

        event.Skip()
