#!/usr/bin/env python3
import wx
from CellularWindow import CellularWindow


class GolWxPy(wx.Frame):
    # TODO add Constants for sliders and sizing

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

        self.Bind(wx.EVT_MENU, self.OnAbout, file_about)
        self.Bind(wx.EVT_MENU, self.OnExit, file_exit)

        self.box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_play = wx.Button(self, -1, "Play")
        button_pause = wx.Button(self, -1, "Pause")
        button_reset = wx.Button(self, -1, "Reset")
        self.buttons = [button_play, button_pause, button_reset]
        for i in self.buttons:
            self.box_sizer.Add(i, 1, wx.EXPAND)

        # Timer rate slider
        self.slider_rate = wx.Slider(
            self,
            value=750,
            minValue=20,
            maxValue=1000,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS,
        )
        self.box_sizer.Add(self.slider_rate, 1, wx.EXPAND)

        # Grid size slider
        self.slider_grid_size = wx.Slider(
            self,
            value=8,
            minValue=8,
            maxValue=128,
            style=wx.SL_HORIZONTAL | wx.SL_LABELS,
        )
        self.box_sizer.Add(self.slider_grid_size, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.OnPlay, button_play)
        self.Bind(wx.EVT_BUTTON, self.OnPause, button_pause)
        self.Bind(wx.EVT_BUTTON, self.OnReset, button_reset)
        # TODO add labels and units to sliders
        self.slider_rate.Bind(wx.EVT_SLIDER, self.OnRate)
        self.slider_grid_size.Bind(wx.EVT_SLIDER, self.OnGridSize)

        self.cellular_window = CellularWindow(self)

        self.vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        # self.vertical_sizer.AddSpacer(5)
        self.vertical_sizer.Add(self.box_sizer, 0, wx.EXPAND)
        self.vertical_sizer.Add(self.cellular_window, 1, wx.EXPAND, 0)

        # Update Cellular window with slider value for grid size
        self.cellular_window.AdjustGridSize(self.slider_grid_size.GetValue())

        self.SetSizer(self.vertical_sizer)
        self.SetAutoLayout(True)
        self.vertical_sizer.Fit(self)
        self.SetSize(800, 600)
        self.Show(True)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.TimerCallback, self.timer)
        self.rate = self.slider_rate.GetValue()
        self.timer.Start(self.rate)

    def TimerCallback(self, event):
        self.cellular_window.IncrementTimeStep()
        print("Timer callback at interval (ms): ", event.GetTimer().GetInterval())

    def OnPlay(self, event):
        self.timer.Start(self.rate)

    def OnPause(self, event):
        self.timer.Stop()

    def OnReset(self, event):
        self.timer.Stop()
        self.cellular_window.RandomlyPopulateGrid()
        self.cellular_window.BuildSquares()

    def OnRate(self, event):
        val = event.GetEventObject().GetValue()
        # TODO invert with constants
        self.rate = val
        self.timer.Start(self.rate)

    def OnGridSize(self, event):
        val = event.GetEventObject().GetValue()
        self.cellular_window.AdjustGridSize(val)

    def OnAbout(self, event):
        dlg = wx.MessageDialog(
            self,
            "Learning experience - Conway's Game of Life implemented in python3 with a wxPython GUI",
            "About gol-wx-py",
            wx.OK,
        )
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)


if __name__ == "__main__":
    app = wx.App(False)
    frame = GolWxPy(None, "Conway's Game of Life using wxPython")
    app.MainLoop()