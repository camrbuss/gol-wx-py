import math
import wx
import numpy as np
from scipy import signal
from collections import deque

# TODO Reduce side effects and make methods more pure


class CellularWindow(wx.Window):

    _grid_size = None
    _grid_line_list = []
    _square_list = []
    _current_state = None
    _state_hashes = deque([], maxlen=3)

    def __init__(self, parent, grid_size, *args, **kwargs):
        wx.Window.__init__(self, parent, *args, **kwargs)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.build_grid_lines)
        self.adjust_grid_size(grid_size)
        self.randomly_populate_grid()

    @staticmethod
    def update_grid(current_grid: np.ndarray) -> np.ndarray:
        if not isinstance(current_grid.flat[0], np.bool_):
            raise RuntimeError("Numpy Array is not of boolean datatype")

        rows = current_grid.shape[0]
        cols = current_grid.shape[1]

        # Copy input array and pad the outter edge with zeros
        curr = np.copy(current_grid)
        blank_col = np.zeros((rows, 1), dtype=bool)
        curr = np.concatenate((blank_col, curr, blank_col), axis=1)
        blank_row = np.zeros((1, cols + 2), dtype=bool)
        curr = np.concatenate((blank_row, curr, blank_row), axis=0)

        x_conv = signal.convolve2d(
            curr, np.array([[1, 0, 1], [0, 0, 0], [1, 0, 1]]), mode="same"
        )
        plus_conv = signal.convolve2d(
            curr, np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]), mode="same"
        )
        curr_sum = x_conv + plus_conv

        next_sum = curr_sum[1 : rows + 1, 1 : cols + 1]
        next_grid = np.copy(current_grid)

        for index, val in np.ndenumerate(next_sum):
            i = index[0]
            j = index[1]
            if (val == 2 or val == 3) and current_grid[i][j]:
                next_grid[i, j] = True
            elif val == 3 and not current_grid[i][j]:
                next_grid[i, j] = True
            else:
                next_grid[i, j] = False

        return next_grid

    def increment_time_step(self):
        self._current_state = CellularWindow.update_grid(self._current_state)
        self._state_hashes.append(hash(self._current_state.tobytes()))
        self.build_squares(self._current_state)
        if self._state_hashes.__len__() == self._state_hashes.maxlen:
            if (
                self._state_hashes[0] == self._state_hashes[2]
                or self._state_hashes[0] == self._state_hashes[1]
            ):
                self.GetParent().button_status.SetLabel("Iterations Stagnant")
                if self.GetParent().is_auto_repeat:
                    self.randomly_populate_grid()
                else:
                    self.GetParent().timer.Stop()

        else:
            self.GetParent().button_status.SetLabel("Iterations Progressing")

    def randomly_populate_grid(self):
        self._current_state = np.random.randint(
            0, high=2, size=(self._grid_size, self._grid_size), dtype=bool
        )
        self.build_squares(self._current_state)
        self._state_hashes.clear()

    def adjust_grid_size(self, length):
        self._grid_size = length
        self.randomly_populate_grid()
        self.SendSizeEvent()

    def build_squares(self, arr):
        self._square_list.clear()
        grid_spacing = self.get_grid_spacing()
        for i in range(0, arr.shape[0]):
            for j in range(0, arr.shape[1]):
                if arr[i, j]:
                    x_loc = i * grid_spacing
                    y_loc = j * grid_spacing
                    width = grid_spacing
                    height = grid_spacing
                    self._square_list.append((x_loc, y_loc, width, height))
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

        self.build_squares(self._current_state)

    def get_grid_spacing(self):
        self.GetSize()
        min_pixels = min(self.GetSize())
        grid_spacing = math.floor(min_pixels / self._grid_size)
        return grid_spacing

    def on_paint(self, event):
        device_context = wx.PaintDC(self)
        device_context.Clear()
        # Draw grid
        device_context.DrawLineList(self._grid_line_list, wx.Pen(wx.BLACK, 1))
        # Draw Rectangles
        device_context.DrawRectangleList(self._square_list, wx.Pen(wx.RED, 1))

        event.Skip()
