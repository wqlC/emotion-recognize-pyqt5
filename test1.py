import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QToolTip
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont, QIcon


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('wweiruanyahei', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        qbtn = QPushButton('Quit', self)
        qbtn.setToolTip('This is a <b>QPushButton</b> widget')
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())

        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle('hello world')
        self.setWindowIcon(QIcon('web.gif'))
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())