'''
调用本机摄像头
'''

import sys
import numpy as np
from PyQt5.QtCore import QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
import cv2

class Camera(QWidget):
    image = pyqtSignal(np.ndarray)
    def __init__(self, camera_port=0):
        super().__init__()
        self.timer = QBasicTimer()
        self.timer.start(1000, self)

    def timerEvent(self, QTimerEvent):
        print('hello world')


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("camera")

        self.label_show_camera = QLabel()
        self.label_show_camera.setFixedSize(800, 600)
        self.label_show_camera.setAutoFillBackground(False)
        self.label_show_camera.setStyleSheet('background-color: #ff0')
        layout = QHBoxLayout()
        layout.addWidget(self.label_show_camera)
        self.setLayout(layout)
        self.camera = Camera()

    def show_image(self, image_data):
        height, width, colors = image_data.shape
        bytesPerLine = colors * width
        # 变换彩色空间
        cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB, image_data)

        #转换为Qimage
        image = QImage(
            image_data.data,
            width,
            height,
            bytesPerLine,
            QImage.Format_RGB888
        )

        self.label_show_camera.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())