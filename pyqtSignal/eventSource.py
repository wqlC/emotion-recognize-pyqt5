'''
Sometime it is convenient to know which widget is the sender of the signal.
Use sender() method to get the sender of the signal.
In this program, we determine the event sender object
'''

import sys
from PyQt5.QtWidgets import *


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('button1', self)
        btn1.move(30, 50)
        btn2 = QPushButton('button2', self)
        btn2.move(150, 50)

        self.statusBar()
        self.setGeometry(300, 300, 400, 300)
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        sender = self.sender()
        print(sender.text()+' was pressed')
        self.statusBar().showMessage(sender.text()+' was pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
