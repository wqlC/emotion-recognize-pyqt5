import sys

from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import *

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.timer = QBasicTimer()
        self.setWindowTitle('timer')

        self.btn_timer = QPushButton('start timer')
        layout = QGridLayout()
        layout.addWidget(self.btn_timer, 0, 0, 1, 1)
        self.setLayout(layout)

        self.btn_timer.clicked.connect(self.timer_control)

    def timer_control(self):
        if self.btn_timer.text() == 'start timer':
            print('new timer')
            self.timer.start(1000, self)
            self.btn_timer.setText('end timer')
        else:
            self.btn_timer.setText('start timer')
            self.timer.stop()

    def timerEvent(self, QTimeEvent):
        print('time_id: {}--hello'.format(QTimeEvent.timerId()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())