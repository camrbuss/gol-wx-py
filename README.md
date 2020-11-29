# gol-wx-py
Learning experience - Conway's Game of Life implemented in python3 with a wxPython GUI

The algorithm implementation is in the static method `CellularWindow.Cellupdate_grid(np.ndarray) -> np.ndarray`

## Features
- Play
- Pause
- Reset
- Single Step
- Stagnant animation detection
- Auto Restart upon stagnant animation
- Image saving (in current directory)
- Speed Adjustment
- Grid Size Adjustment

![](demo.gif)

## Python 3 Dependencies
- wxPython (wx)
- Numpy (numpy)
- Scipy (scipy)
