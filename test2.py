import sys

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import *


class Communicate(QObject):
    closeApp = pyqtSignal()
    pass

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('pyqtSignal')

        self.c = Communicate()
        self.c.closeApp.connect(self.showmessage)
        self.show()

    def mousePressEvent(self, QMouseEvent):
        self.c.closeApp.emit()

    def showmessage(self):
        print('mouse pressed - to close window')
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())
