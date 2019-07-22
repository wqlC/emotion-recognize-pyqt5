'''
emotion recognize

# TODO train a model and input the image data to recognize the emotion
'''
import sys
import time

import numpy as np
import cv2

from PyQt5.QtCore import pyqtSignal, QBasicTimer, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()

        #打开相机
        self.btn_open_cam()

    def set_ui(self):
        # 布局设置
        self.layout_main = QHBoxLayout()  # 整体框架是水平布局
        self.layout_button = QVBoxLayout()  # 按键布局是垂直布局

        # 按钮设置
        self.btn_photo = QPushButton(u'拍照识别')
        self.btn_video = QPushButton(u'实时识别')
        self.btn_quit = QPushButton(u'退出')

        # 显示视频
        self.label_show_camera = QLabel()

        # 显示捕获的图片
        self.label_capture = QLabel()
        self.label_capture.setFixedSize(100, 75)
        self.label_capture.setStyleSheet('background-color:#00f')

        # 显示文本框
        self.text = QTextEdit(self)

        self.label_show_camera.setFixedSize(800, 600)
        self.label_show_camera.setAutoFillBackground(False)
        self.label_show_camera.setStyleSheet('background-color: #ff0')

        # 布局
        self.layout_button.addWidget(self.btn_photo)
        self.layout_button.addWidget(self.btn_video)
        self.layout_button.addWidget(self.btn_quit)
        self.layout_button.addWidget(self.label_capture)
        self.layout_button.addWidget(self.text)

        self.layout_main.addWidget(self.label_show_camera)
        self.layout_main.addLayout(self.layout_button)

        self.setLayout(self.layout_main)
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("人脸识别软件")

        # 拍照识别
        self.btn_photo.clicked.connect(self.btn_photo_capture)
        # 实时识别
        self.btn_video.clicked.connect(self.btn_video_capture)
        self.video_timer = QBasicTimer()

        # 退出
        self.btn_quit.clicked.connect(self.closeApp)

    def btn_open_cam(self):
        self.camera_record = CameraRecord()
        self.camera_record.image_data.connect(self.show_main_image)

    def show_main_image(self, image_data):
        self.main_image = image_data
        image = self.image2Qimage(image_data)
        pixmap = QPixmap.fromImage(image)

        # pixmap.scaled(): resize the image
        self.label_show_camera.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio))
        pass

    def btn_photo_capture(self):
        self.show_capture_image(self.main_image)
        pass

    def image2Qimage(self, image_data):
        height, width, colors = image_data.shape
        bytesPerLine = colors * width
        # 变换彩色空间
        cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB, image_data)

        # 转换为Qimage
        image = QImage(
            image_data.data,
            width,
            height,
            bytesPerLine,
            QImage.Format_RGB888
        )
        return image

    def show_capture_image(self, image_data):

        image = self.image2Qimage(image_data)

        pixmap = QPixmap.fromImage(image)
        # pixmap.scaled(): resize the image
        self.label_capture.setPixmap(pixmap.scaled(100, 75, Qt.KeepAspectRatio))
        self.emotion_recognition(image_data)
        pass

    def btn_video_capture(self):
        # 设置一个计时器，用于定时捕获人脸，显示。
        if self.btn_video.text() == u'实时识别':
            self.btn_photo.setEnabled(False)
            self.btn_video.setText(u'停止识别')
            # print('开始自动捕获')
            self.video_timer.start(500, self)
        else:
            self.video_timer.stop()
            # print('结束自动捕获')
            self.btn_photo.setEnabled(True)
            self.btn_video.setText(u'实时识别')
        pass

    def emotion_recognition(self, picture):
        '''

        :param picture:
        :return:
        '''
        picture_name = str(int(time.time())) + '.jpg'
        cv2.imwrite(picture_name, picture)
        self.text.setText(picture_name)
        pass

    def timerEvent(self, QTimeEvent):
        if QTimeEvent.timerId() == self.video_timer.timerId():
            # print('video_timer_id: {}'.format(self.video_timer.timerId()))
            self.show_capture_image(self.main_image)

    def closeApp(self):
        if self.btn_video.text() == u'停止识别':
            self.video_timer.stop()
        self.camera_record.camera.release()
        cv2.destroyAllWindows()
        self.close()


class CameraRecord(QWidget):

    image_data = pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0):
        super().__init__()
        self.camera = cv2.VideoCapture(camera_port)
        self.timer = QBasicTimer()
        self.timer.start(0, self)

    def timerEvent(self, QTimerEvent):
        if QTimerEvent.timerId() != self.timer.timerId():
            return
        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())
