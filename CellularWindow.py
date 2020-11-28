import wx
import math
import numpy as np

# TODO Reduce side effects and make methods more pure

class CellularWindow(wx.Window):

    __grid_size = 64
    __grid_line_list = []
    __square_list = []
    __current_state = None
    __next_state = None

    def __init__(self, parent, *args, **kwargs):
        wx.Window.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.BuildGridLines)
        self.AdjustGridSize(self.__grid_size)
        self.RandomlyPopulateGrid()

    def IncrementTimeStep(self):
        self.BuildSquares()

    def RandomlyPopulateGrid(self):
        self.__current_state = np.random.randint(
            0, high=2, size=(self.__grid_size, self.__grid_size), dtype=bool
        )

    def AdjustGridSize(self, length):
        self.__grid_size = length
        self.RandomlyPopulateGrid()
        self.SendSizeEvent()

    def BuildSquares(self):
        self.__square_list.clear()
        grid_spacing = self.GetGridSpacing()
        for i in range(0, self.__grid_size):
            for j in range(0, self.__grid_size):
                if self.__current_state[i, j]:
                    x = i * grid_spacing
                    y = j * grid_spacing
                    w = grid_spacing
                    h = grid_spacing
                    self.__square_list.append((x, y, w, h))
        self.Refresh()

    def BuildGridLines(self, event):
        self.__grid_line_list.clear()
        grid_spacing = self.GetGridSpacing()
        for i in range(0, self.__grid_size + 1):
            # Vertical lines
            x1 = i * grid_spacing
            y1 = 0
            x2 = x1
            y2 = self.__grid_size * grid_spacing
            self.__grid_line_list.append((x1, y1, x2, y2))

            # Horizontal lines
            x1 = 0
            y1 = i * grid_spacing
            x2 = self.__grid_size * grid_spacing
            y2 = y1
            self.__grid_line_list.append((x1, y1, x2, y2))

        self.BuildSquares()

    def GetGridSpacing(self):
        self.GetSize()
        min_pixels = min(self.GetSize())
        grid_spacing = math.floor(min_pixels / self.__grid_size)
        return grid_spacing

    def ZeroGrid(self):
        self.__current_state = np.zeros(
            (self.__grid_size, self.__grid_size), dtype=bool
        )
        self.__next_state = np.zeros((self.__grid_size, self.__grid_size), dtype=bool)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        # Draw grid
        dc.DrawLineList(self.__grid_line_list, wx.Pen(wx.BLACK, 1))
        # Draw Rectangles
        dc.DrawRectangleList(self.__square_list, wx.Pen(wx.RED, 1))

        event.Skip()
