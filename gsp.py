# Game State Player
# Heuristics based on 2048 AI written by Ovolve
# https://github.com/ovolve/2048-AI

import numpy as np

def _free(board):
    # amount of free tiles on a scale of 0-1 (1 being best, 0 being worst)
    # board - 2D Numpy Array
    freetiles = 0

    for a in board:
        for b in a:
            if b == 0:
                freetiles += 1

    return (freetiles / 16)

def _mono(board):
    # monotricity of the board on a scale of 0-1 (1 being best, 0 being worst)
    # board - 2D Numpy Array
    # may have to update it to use rot90

    scores = []

    for a in board:
        temptotala = 0
        for b in range(0, 3):
            if a[b] > a[b+1]:
                temptotala += 1
        temptotalb = 0
        for b in range(3, 0, -1):
            if a[b] > a[b-1]:
                temptotalb += 1
        scores.append(max(temptotala, temptotalb)/3)
    for a in range(0, 4):
        temptotala = 0
        for b in range(0, 3):
            if board[b, a] > board[b+1, a]:
                temptotala += 1
        temptotalb = 0
        for b in range(3, 0, -1):
            if board[b, a] > board[b-1, a]:
                temptotalb += 1
        scores.append(max(temptotala, temptotalb)/3)

    monotricity = 0
    for a in scores:
        monotricity += a

    return monotricity / len(scores)

def _smth(board):
    # smoothness of the board on a scale of 0-1 (1 being best, 0 being worst)
    # board - 2D Numpy Array
    # may have to update it to use rot90

    scores = []

    for a in board:
        temptotal = 0
        for b in range(0, 3):
            if a[b] == a[b + 1]:
                temptotal += 1
        scores.append(temptotal / 3)
    for a in range(0, 4):
        temptotal = 0
        for b in range(0, 3):
            if board[b, a] == board[b + 1, a]:
                temptotal += 1
        scores.append(temptotal / 3)

    smoothness = 0
    for a in scores:
        smoothness += a

    return smoothness / len(scores)

def _corner(board):
    highest = x = y = 0

    for a in range(0, 4):
        for b in range(0, 4):
            if board[b, a] > highest:
                highest = board[b, a]
                x = a
                y = b

    if x == 0 or x == 3:
        if y == 0 or y == 3:
            return 1.0
    return 0.0

def _simMove(board, dirinput):
    # simulates game movement and returns simulated board
    # given original board and direction inputted
    # does not simulate the adding of a new tile after movement

    # board - 2D Numpy Array
    # dirinput - int / char giving number of rots
    # r = 0 = right
    # d = 1 = down
    # l = 2 = left
    # u = 3 = up

    dircode = {
        'r' : 0,
        'd' : 1,
        'l' : 2,
        'u' : 3
    }

    dir = None

    if not isinstance(dirinput, int):
        try:
            dir = dircode[dirinput]
        except:
            print("Uh oh! Could not complete simulated move!")
            return board
    else:
        dir = dirinput

    finalboard = board.copy()

    for i in range(dir):
        finalboard = np.rot90(finalboard)

    mergecount = 0

    for a in finalboard:
        marked = []
        for i in range(2, -1, -1):
            if a[i] != 0:
                for j in range(i + 1, 4):
                    if a[j] == a[i] and i not in marked:
                        a[j] *= 2
                        a[i] = 0
                        mergecount += 1
                        marked.append(j)
                        break
                    elif a[j] != 0:
                        if j-1 != i:
                            a[j-1] = a[i]
                            a[i] = 0
                        break
                else:
                    a[3] = a[i]
                    a[i] = 0

    for i in range(dir, 4):
        finalboard = np.rot90(finalboard)

    if (finalboard == board).all():
        return None
    else:
        return (finalboard, mergecount / 16)

def _getPossibleBoards(board):
    # returns a 2D array of all possible boards, separated by input direction

    allBoards = [[], [], [], []]
    tempBoard = None

    for a in range(4):

        if _simMove(board, a) is not None:
            tempBoard, mergecount = _simMove(board, a)
            allBoards[a].append(mergecount)
            for y in range(4):
                for x in range(4):
                    if tempBoard[y, x] == 0:
                        tempBoard[y, x] = 2
                        allBoards[a].append(np.copy(tempBoard))
                        tempBoard[y, x] = 4
                        allBoards[a].append(np.copy(tempBoard))
                        tempBoard[y, x] = 0
        else:
            allBoards[a].append(None)

    return allBoards

def _getAvgValues(board):
    allBoards = _getPossibleBoards(board)
    dirValues = [[], [], [], []]

    for a in range(4):
        totalBoards = totalFree = totalMono = totalSmth = totalCorner = 0
        if allBoards[a][0] is not None:
            mergecount = allBoards[a][0]
            for b in allBoards[a]:
                if not isinstance(b, float):
                    totalBoards += 1
                    totalFree += _free(b)
                    totalMono += _mono(b)
                    totalSmth += _smth(b)
                    totalCorner += _corner(b)
            dirValues[a].append((totalFree / totalBoards, totalMono / totalBoards, totalSmth / totalBoards, mergecount, totalCorner / totalBoards))
        else:
            dirValues[a].append(None)

    return dirValues

def findBestDir(board, w0, w1, w2):
    directions = []
    avgValues = _getAvgValues(board)
    maximumDirection = -1
    tempMax = 0

    for a in range(4):
        if avgValues[a][0] is not None:
            weights = (avgValues[a][0][0] * w0) + (avgValues[a][0][1] * w1) + (avgValues[a][0][2] * w2) + (avgValues[a][0][3]) + (avgValues[a][0][4])
            if tempMax < weights:
                tempMax = weights
                maximumDirection = a

    return maximumDirection
