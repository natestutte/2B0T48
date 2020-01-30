# Game State Reader

from pyautogui import screenshot
from PIL import Image
import numpy as np

def refresh():
    # Returns a screenshot of the 2048 board
    # Requires Scrot for Linux
    return _getGameBoard(screenshot().convert("RGB"))

def _getGameBoard(screen):
    # Crops and returns game board based on color of board (#B7AF9F / R: 187 G: 176 B: 159)
    x, y = screen.size
    direction = np.zeros(4, dtype=np.int16)
    for a in range(x):
        for b in range(y):
            pixel = screen.getpixel((a, b))
            if pixel == (187, 173, 160):
                direction[0] = a
                break
        else:
            continue
        break
    else:
        return None
    for a in range(x-1, 0, -1):
        for b in range(y):
            pixel = screen.getpixel((a, b))
            if pixel == (187, 173, 160):
                direction[2] = a
                break
        else:
            continue
        break
    else:
        return None
    for a in range(y):
        for b in range(x):
            pixel = screen.getpixel((b, a))
            if pixel == (187, 173, 160):
                direction[1] = a
                break
        else:
            continue
        break
    else:
        return None
    for a in range(y-1, 0, -1):
        for b in range(x):
            pixel = screen.getpixel((b, a))
            if pixel == (187, 173, 160):
                direction[3] = a
                break
        else:
            continue
        break
    else:
        return None
    return screen.crop(direction)

def getBoardState(board):
    # Returns a numpy 2d array representing the gameboard
    colordict = {
        (205, 193, 180) : 0,
        (238, 228, 218) : 2,
        (237, 224, 200) : 4,
        (242, 177, 121) : 8,
        (245, 149, 99) : 16,
        (246, 124, 95) : 32,
        (246, 94, 59) : 64,
        (237, 207, 114) : 128,
        (237, 204, 97) : 256,
        (237, 200, 80) : 512,
        (237, 197, 63) : 1024,
        (237, 194, 46) : 2048
    }

    boardstate = np.zeros((4, 4), dtype=np.int16)
    x, y = board.size

    # New board -> boardstate Converter

    numtile = -1
    for a in colordict:
        numtile += 1
        coloredpixels = []
        for b in range(0, x, 10):
            for c in range(0, y, 10):
                if board.getpixel((b, c)) == a:
                    coloredpixels.append((b, c))

        for a in coloredpixels:
            for b in range(0, 4):
                for c in range(0, 4):
                    if ((x / 33.2666) + b * ((x / 4.7075) + (x / 33.2666))) < a[0] \
                            < ((x / 4.1583) + b * ((x / 4.7075) + (x / 33.2666))):
                        if ((x / 33.2666) + c * ((x / 4.7075) + (x / 33.2666))) < a[1] \
                                < ((x / 4.1583) + c * ((x / 4.7075) + (x / 33.2666))):
                            if 2**numtile == 1:
                                boardstate[c,b] = 0
                            else:
                                boardstate[c,b] = 2**numtile

    # Old board -> boardstate Converter

    # ax = ay = 0
    #
    # for a in range(0, 4):
    #     for b in range(0, 4):
    #         ax = int((x / 7.6769) + (a * (x / 4.0901)))
    #         ay = int((y / 7.6769) + (b * (y / 4.0901)))
    #         print(ax, ay)
    #         boardstate[b, a] = colordict[board.getpixel((ax, ay))]
    #         print(boardstate)

    return boardstate