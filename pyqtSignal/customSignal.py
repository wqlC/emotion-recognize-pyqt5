'''
Objects created from QObject can emit signals.
In this program, we show how to emit a custom signal.
'''

import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import *

class Communicate(QObject):
    closeApp = pyqtSignal()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.c = Communicate()
        self.c.closeApp.connect(self.showMessage)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('pyqtSignal emit signal')
        self.show()

    def mousePressEvent(self, QMouseEvent):
        self.c.closeApp.emit()

    def showMessage(self):
        print('press the mouse')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())