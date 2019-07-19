import sys

import cv2
from PyQt5.QtCore import QBasicTimer, pyqtSignal
from PyQt5.QtWidgets import *

class T(QWidget):

    def __init__(self):
        super().__init__()
        self.camera = cv2.VideoCapture(0)

        self.timer = QBasicTimer()
        self.timer.start(1000, self)

    def timerEvent(self, QTimeEvent):
        print('hello')
        self.camera.read()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.t = T()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    # window.show()

    sys.exit(app.exec_())