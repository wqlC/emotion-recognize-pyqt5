#-*- coding:utf-8 -*-
'''
defined Signal
'''

import sys
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QCheckBox, QSpinBox, QHBoxLayout, QComboBox, QGridLayout


class SignalEmit(QWidget):
    helpSignal = pyqtSignal(str)
    printSignal = pyqtSignal(list)

    # 声明一个多重载版本的信号，包括了一个带int和str类型参数的信号，以及带str参数的信号
    previewSignal = pyqtSignal([int,str],[str])

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.creatContorls("打印控制：")
        self.creatResult("操作结果：")

        layout = QHBoxLayout()
        layout.addWidget(self.controlsGroup)
        layout.addWidget(self.resultGroup)
        self.setLayout(layout)

        self.helpSignal.connect(self.showHelpMessage)
        self.printSignal.connect(self.printPaper)
        self.previewSignal[str].connect(self.previewPaper)
        self.previewSignal[int,str].connect(self.previewPaperWithArgs)
        self.printButton.clicked.connect(self.emitPrintSignal)
        self.previewButton.clicked.connect(self.emitPreviewSignal)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('defined signal')
        self.show()

    def creatContorls(self, title):
        self.controlsGroup = QGroupBox(title)
        self.printButton = QPushButton("打印")
        self.previewButton  = QPushButton("预览")
        numberLabel = QLabel("打印份数：")
        pageLabel = QLabel("纸张类型：")
        self.previewStatus = QCheckBox("全屏预览")
        self.numberSpinBox = QSpinBox()
        self.numberSpinBox.setRange(1, 100)
        self.styleCombo = QComboBox(self)
        self.styleCombo.addItem("A4")
        self.styleCombo.addItem("A5")

        controlsLayout = QGridLayout()
        controlsLayout.addWidget(numberLabel, 0, 0)
        controlsLayout.addWidget(self.numberSpinBox, 0, 1)
        controlsLayout.addWidget(pageLabel, 0, 2)
        controlsLayout.addWidget(self.styleCombo, 0, 3)
        controlsLayout.addWidget(self.printButton, 0, 4)
        controlsLayout.addWidget(self.previewStatus, 3, 0)
        controlsLayout.addWidget(self.previewButton, 3, 1)
        self.controlsGroup.setLayout(controlsLayout)

    def creatResult(self,title):
        self.resultGroup = QGroupBox(title)
        self.resultLabel = QLabel("")
        layout = QHBoxLayout()
        layout.addWidget(self.resultLabel)
        self.resultGroup.setLayout(layout)

    def emitPreviewSignal(self):
        if self.previewStatus.isChecked() == True:
            self.previewSignal[int, str].emit(1080, " Full Screen")
        elif self.previewStatus.isChecked() == False:
            self.previewSignal[str].emit("Preview")

    def emitPrintSignal(self):
        pList = []
        pList.append(self.numberSpinBox.value ())
        pList.append(self.styleCombo.currentText())
        self.printSignal.emit(pList)

    def printPaper(self,list):
        self.resultLabel.setText("Print: "+"份数："+ str(list[0]) +"  纸张："+str(list[1]))

    def previewPaperWithArgs(self,style,text):
        self.resultLabel.setText(str(style)+text)

    def previewPaper(self,text):
        self.resultLabel.setText(text)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_F1:
            self.helpSignal.emit("help message")

    def showHelpMessage(self, message):
        self.resultLabel.setText(message)
        #self.statusBar().showMessage(message)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    dispatch = SignalEmit()
    sys.exit(app.exec_())
