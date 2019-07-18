# -*- coding: utf-8 -*-

'''
In this example, we connect a signal of a QSlider to a slot of QLCDNumber
'''

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lcd = QLCDNumber()
        sld = QSlider(Qt.Horizontal, self)
        sld.setMaximum(1000)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)
        self.setLayout(vbox)

        sld.valueChanged.connect(lcd.display)

        self.setWindowTitle('Signal and Slot')
        print('hello world')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())
