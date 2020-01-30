# Main

import gsr, gsp
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyautogui
import keyboard

class Window(QWidget):

    def __init__(self, ftv, mtv, sv):
        super().__init__()

        self.running = True
        self.learning = False
        self.ftv = ftv
        self.mtv = mtv
        self.sv = sv

        self.SelfLearningButton = QPushButton("Let 2B0T48 Learn", self)
        self.SelfLearningButton.setToolTip("Allow the bot to learn from user input.")
        self.SelfLearningButton.clicked.connect(self._performLearning)

        self.FreeTilesLabel = QLabel()
        self.FreeTilesLabel.setAlignment(Qt.AlignCenter)
        self.FreeTilesLabel.setText(f"Free Tile Value : {self.ftv}")

        self.FreeTilesSlider = QSlider(Qt.Horizontal, self)
        self.FreeTilesSlider.setMinimum(0)
        self.FreeTilesSlider.setMaximum(100)
        self.FreeTilesSlider.valueChanged.connect(self._changeFTValue)

        self.MonotricityLabel = QLabel()
        self.MonotricityLabel.setAlignment(Qt.AlignCenter)
        self.MonotricityLabel.setText(f"Monotricity Value : {self.mtv}")

        self.MonotricitySlider = QSlider(Qt.Horizontal, self)
        self.MonotricitySlider.setMinimum(0)
        self.MonotricitySlider.setMaximum(100)
        self.MonotricitySlider.valueChanged.connect(self._changeMTValue)

        self.SmoothnessLabel = QLabel()
        self.SmoothnessLabel.setAlignment(Qt.AlignCenter)
        self.SmoothnessLabel.setText(f"Smoothness Value : {self.sv}")

        self.SmoothnessSlider = QSlider(Qt.Horizontal, self)
        self.SmoothnessSlider.setMinimum(0)
        self.SmoothnessSlider.setMaximum(100)
        self.SmoothnessSlider.valueChanged.connect(self._changeSValue)

        self.StartButton = QPushButton("Start 2B0T48!", self)
        self.StartButton.setToolTip("Start the bot using the heuristics set above.")
        self.StartButton.clicked.connect(self._startButtonClicked)

        self.FreeTilesSlider.setValue(self.ftv * 100)
        self.MonotricitySlider.setValue(self.mtv * 100)
        self.SmoothnessSlider.setValue(self.sv * 100)

        layout = QGridLayout()
        layout.setSpacing(30)
        layout.addWidget(self.SelfLearningButton, 0, 0)
        layout.addWidget(self.FreeTilesLabel, 1, 0)
        layout.addWidget(self.FreeTilesSlider, 2, 0)
        layout.addWidget(self.MonotricityLabel, 3, 0)
        layout.addWidget(self.MonotricitySlider, 4, 0)
        layout.addWidget(self.SmoothnessLabel, 5, 0)
        layout.addWidget(self.SmoothnessSlider, 6, 0)
        layout.addWidget(self.StartButton, 7, 0)
        layout.setAlignment(Qt.AlignCenter)

        self.setGeometry(50, 50, 200, 350)
        self.setWindowTitle("2B0T48")
        self.setLayout(layout)
        self.show()

    def _changeFTValue(self, value):
        self.ftv = value / 100
        self.FreeTilesLabel.setText(f"Free Tile Value : {self.ftv}")

    def _changeMTValue(self, value):
        self.mtv = value / 100
        self.MonotricityLabel.setText(f"Monotricity Value : {self.mtv}")

    def _changeSValue(self, value):
        self.sv = value / 100
        self.SmoothnessLabel.setText(f"Smoothness Value : {self.sv}")

    def _startButtonClicked(self):
        self.running = False
        self.close()

    def _performLearning(self):
        self.running = False
        self.learning = True
        self.close()

    def getFTValue(self):
        return (self.ftv, self.mtv, self.sv)

    def getRunning(self):
        return self.running

    def closeEvent(self, event):
        if self.running == False:
            self.running = True
        else:
            self.running = False
        self.close()

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    window = QApplication(sys.argv)
    ftv = mtv = sv = 0.5

    while True:
        ex = Window(ftv, mtv, sv)
        window.exec_()
        if ex.learning:
            ftv = mtv = sv = count = 0
            board = gsr.refresh()
            while board is not None:
                board = gsr.getBoardState(board)
                count += 1
                ftv = gsp._free(board)
                mtv = gsp._mono(board)
                sv = gsp._smth(board)
                while True:
                    time.sleep(0.2)
                    boardcheck = gsr.refresh()
                    if boardcheck is not None:
                        if (board == gsr.getBoardState(boardcheck)).all():
                            time.sleep(0.2)
                            break
                    else:
                        break
                board = gsr.refresh()
            if count != 0:
                ftv = round(ftv / count, 2)
                mtv = round(mtv / count, 2)
                sv = round(sv / count, 2)
        else:
            ftv = ex.ftv
            mtv = ex.mtv
            sv = ex.sv

            while True:
                board = gsr.refresh()
                if board is not None:
                    bestmove = gsp.findBestDir(gsr.getBoardState(board), ftv, mtv, sv)

                    if bestmove == 0:
                        pyautogui.press('right')
                    elif bestmove == 1:
                        pyautogui.press('down')
                    elif bestmove == 2:
                        pyautogui.press('left')
                    else:
                        pyautogui.press('up')
                else:
                    break
        if ex.running == False:
            break