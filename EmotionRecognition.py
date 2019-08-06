from sklearn.externals import joblib
import numpy as np
from skimage.feature import local_binary_pattern
from skimage import feature as ft
import cv2
from PIL import Image


class EmotionRecognition():
    def __init__(self):
        self.emotion_list = ['angry', 'happy', 'n', 'sad']
        self.model_path = "./svm_model.m"     #加载的模型的路径
        self.model = joblib.load(self.model_path)

    def clf_emotion(self, image):
        face_pic = self.saveFaces(image)
        if face_pic:
            lbp_feature = self.get_lbp_feature(np.array(face_pic))
            hog_feature = self.get_hog_feature(np.array(face_pic))
            feature = np.concatenate([hog_feature, lbp_feature])
            predict = self.model.predict(feature.reshape((1, -1)))
        else:
            predict = -1;
        print('%s:  %s' % ("the emotion of image is: ", self.emotion_list[np.int(predict)]))
        return self.emotion_list[np.int(predict)]

    def get_hog_feature(self, image):
        features = ft.hog(image,  # input image
                          orientations=9,  # number of bins
                          pixels_per_cell=(8, 8),  # pixel per cell
                          cells_per_block=(2, 2),  # cells per blcok
                          block_norm='L1',  # block norm : str {‘L1’, ‘L1-sqrt’, ‘L2’, ‘L2-Hys’}
                          transform_sqrt=True,  # power law compression (also known as gamma correction)
                          feature_vector=True,  # flatten the final vectors
                          visualize=False)  # return HOG map
        return features

    def get_lbp_feature(self, image):
        # 参数设置
        # settings for LBP
        radius = 1  # LBP算法中范围半径的取值
        n_points = 8 * radius  # 领域像素
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # LBP处理
        lbp = local_binary_pattern(image, n_points, radius)
        lbp_list = self.split_matrix(lbp, 8, 8)

        hist_normal_all = np.arange(0)
        for lpb_matrix in lbp_list:
            width, height = lpb_matrix.shape
            hist, bin_edges = np.histogram(lpb_matrix, bins=256)
            hist_normal = hist / (width * height)
            hist_normal_all = np.hstack((hist_normal_all, hist_normal))
        return hist_normal_all

    def split_matrix(self, matrix, h_num, v_num):
        """
        h_num:横向分割数量
        v_num：纵向分割数量
        """
        h_list = np.hsplit(matrix, h_num)
        matrix_list = []
        for h_matrix in h_list:
            v_list = np.vsplit(h_matrix, v_num)
            for v_matrix in v_list:
                matrix_list.append(v_matrix)
        return matrix_list

    def saveFaces(self, image_path):
        faces = self.detectFaces(image_path)
        if faces:
            # 将人脸保存在save_dir目录下。
            # Image模块：Image.open获取图像句柄，crop剪切图像(剪切的区域就是detectFaces返回的坐标)，save保存。
            for (x1, y1, x2, y2) in faces:
                image = Image.fromarray(image_path).crop((x1, y1, x2, y2)).convert('RGB').resize((64, 64))
                return image
        else:
            return faces

    def detectFaces(self, image_name):
        # img = cv2.imread(image_name)
        img = image_name
        face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml")
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img  # if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

        faces = face_cascade.detectMultiScale(gray, 1.2, 2)  # 1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
        result = []
        for (x, y, width, height) in faces:
            result.append((x, y, x + width, y + height))
        return result


if __name__ == '__main__':
    pic_path = './sad.jpg'  # 最后测试的图像路径
    img = cv2.imread(pic_path)
    emotionRecognition = EmotionRecognition()
    emotionRecognition.clf_emotion(img)
