import sys

from PyQt5.QtCore import QBasicTimer, pyqtSignal
from PyQt5.QtWidgets import *

class T(QWidget):
    data = pyqtSignal(int)
    index = 0
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):
        self.timer = QBasicTimer()
        self.timer.start(1000, self)

    def timerEvent(self, QTimerEvent):
        print('timer_id: \n\t{}'.format(self.timer.timerId()))
        self.index += 1
        self.data.emit(self.index)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.t = T()
        # self.t.data.connect(self.showdata)
    def showdata(self):
        print(self.sender().data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    # window.show()

    sys.exit(app.exec_())