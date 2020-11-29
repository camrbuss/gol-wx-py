#!/usr/bin/env python3
import wx
from CellularWindow import CellularWindow


class GolWxPy(wx.Frame):

    DEFAULT_WINDOW_HEIGHT = 800
    DEFAULT_WINDOW_WIDTH = 1200

    BUTTON_HEIGHT = 50
    BUTTON_WIDTH = 100
    BUTTON_SIZE = wx.Size(BUTTON_WIDTH, BUTTON_HEIGHT)

    SLIDER_RATE_LABEL = "Tick Period (ms)"
    SLIDER_RATE_VALUE = 750
    SLIDER_RATE_MINVALUE = 20
    SLIDER_RATE_MAXVALUE = 1000

    SLIDER_GRID_LABEL = "Grid Size (ul)"
    SLIDER_GRID_VALUE = 8
    SLIDER_GRID_MINVALUE = 8
    SLIDER_GRID_MAXVALUE = 128

    is_auto_repeat = False

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        self.CreateStatusBar()
        file_menu = wx.Menu()

        file_about = file_menu.Append(wx.ID_ABOUT, "&About", " About this thing")
        file_menu.AppendSeparator()
        file_exit = file_menu.Append(wx.ID_EXIT, "&Exit", "Exit")

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_about, file_about)
        self.Bind(wx.EVT_MENU, self.on_exit, file_exit)

        self.option_bar_box_sizer = wx.BoxSizer(wx.VERTICAL)
        button_play = wx.Button(self, -1, "Play", size=self.BUTTON_SIZE)
        button_pause = wx.Button(self, -1, "Pause", size=self.BUTTON_SIZE)
        button_next = wx.Button(self, -1, "Next", size=self.BUTTON_SIZE)
        button_reset = wx.Button(self, -1, "Reset", size=self.BUTTON_SIZE)
        self.button_grid_sizer = wx.GridSizer(2, 0, 0)
        self.button_grid_sizer.AddMany(
            [button_play, button_pause, button_next, button_reset]
        )
        self.option_bar_box_sizer.Add(self.button_grid_sizer)

        self.checkbox_auto_repeat = wx.CheckBox(self, label="Auto Reset")
        self.option_bar_box_sizer.Add(self.checkbox_auto_repeat, 1, wx.EXPAND)

        # Timer rate slider
        slider_rate_box = wx.StaticBox(self, label=self.SLIDER_RATE_LABEL)
        slider_rate_box_sizer = wx.StaticBoxSizer(slider_rate_box, wx.VERTICAL)
        self.slider_rate = wx.Slider(
            self,
            value=self.SLIDER_RATE_VALUE,
            minValue=self.SLIDER_RATE_MINVALUE,
            maxValue=self.SLIDER_RATE_MAXVALUE,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS,
        )
        slider_rate_box_sizer.Add(self.slider_rate, 1, wx.EXPAND)
        self.option_bar_box_sizer.AddSpacer(5)
        self.option_bar_box_sizer.Add(slider_rate_box_sizer, 1, wx.EXPAND)
        self.option_bar_box_sizer.AddSpacer(5)

        # Grid size slider
        slider_grid_box = wx.StaticBox(self, label=self.SLIDER_GRID_LABEL)
        slider_grid_box_sizer = wx.StaticBoxSizer(slider_grid_box, wx.VERTICAL)
        self.slider_grid_size = wx.Slider(
            self,
            value=self.SLIDER_GRID_VALUE,
            minValue=self.SLIDER_GRID_MINVALUE,
            maxValue=self.SLIDER_GRID_MAXVALUE,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS,
        )
        slider_grid_box_sizer.Add(self.slider_grid_size, 1, wx.EXPAND)
        self.option_bar_box_sizer.AddSpacer(5)
        self.option_bar_box_sizer.Add(slider_grid_box_sizer, 1, wx.EXPAND)
        self.option_bar_box_sizer.AddSpacer(5)

        self.button_status = wx.Button(self, -1, label="Status: None")
        self.button_status.Disable()
        self.option_bar_box_sizer.Add(self.button_status, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.on_play, button_play)
        self.Bind(wx.EVT_BUTTON, self.on_pause, button_pause)
        self.Bind(wx.EVT_BUTTON, self.on_next, button_next)
        self.Bind(wx.EVT_BUTTON, self.on_reset, button_reset)
        self.Bind(wx.EVT_CHECKBOX, self.on_auto_repeat, self.checkbox_auto_repeat)
        self.slider_rate.Bind(wx.EVT_SLIDER, self.on_rate)
        self.slider_grid_size.Bind(wx.EVT_SLIDER, self.on_grid_size)

        self.cellular_window = CellularWindow(self, self.slider_grid_size.GetValue())

        self.drawing_option_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.drawing_option_sizer.AddSpacer(10)
        self.drawing_option_sizer.Add(self.option_bar_box_sizer, 0, wx.EXPAND)
        self.drawing_option_sizer.AddSpacer(10)
        self.drawing_option_sizer.Add(self.cellular_window, 1, wx.EXPAND, 0)

        self.SetSizer(self.drawing_option_sizer)
        self.SetAutoLayout(True)
        self.drawing_option_sizer.Fit(self)
        self.SetSize(self.DEFAULT_WINDOW_WIDTH, self.DEFAULT_WINDOW_HEIGHT)
        self.Show(True)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_callback, self.timer)
        self.rate = self.slider_rate.GetValue()

    def timer_callback(self, event):
        # pylint: disable=unused-argument
        self.cellular_window.increment_time_step()

    def on_play(self, event):
        # pylint: disable=unused-argument
        self.timer.Start(self.rate)

    def on_pause(self, event):
        # pylint: disable=unused-argument
        self.timer.Stop()

    def on_next(self, event):
        # pylint: disable=unused-argument
        self.timer.Stop()
        self.timer.StartOnce(milliseconds=0)

    def on_reset(self, event):
        # pylint: disable=unused-argument
        self.timer.Stop()
        self.cellular_window.randomly_populate_grid()

    def on_auto_repeat(self, event):
        self.is_auto_repeat = event.GetEventObject().GetValue()

    def on_rate(self, event):
        val = event.GetEventObject().GetValue()
        self.rate = val
        if self.timer.IsRunning():
            self.timer.Start(self.rate)

    def on_grid_size(self, event):
        val = event.GetEventObject().GetValue()
        self.cellular_window.adjust_grid_size(val)

    def on_about(self, event):
        # pylint: disable=unused-argument
        dlg = wx.MessageDialog(
            self,
            "Learning experience - Conway's Game of Life implemented in python3 with a wxPython GUI",
            "About gol-wx-py",
            wx.OK,
        )
        dlg.ShowModal()
        dlg.Destroy()

    def on_exit(self, event):
        # pylint: disable=unused-argument
        self.Close(True)


if __name__ == "__main__":
    app = wx.App(False)
    frame = GolWxPy(None, "Conway's Game of Life using wxPython")
    app.MainLoop()