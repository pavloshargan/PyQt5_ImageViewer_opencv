import os
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2
from matplotlib import pyplot as plt
import numpy as np
import qdarkstyle
import scipy.misc
import colorsys
from PIL import Image

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.bg = QFrame(self)
        self.bg.setGeometry(0, 0, 800, 600)
        self.pic = QLabel(self.bg)
        self.pic.setBackgroundRole(QPalette.Base)
        self.pic.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.pic.setScaledContents(True)

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(okButton)
        vbox.addWidget(cancelButton)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.bg)
        hbox.addLayout(vbox)
        self.setLayout(hbox)
        self.setGeometry(0, 0, 800, 600)

        # self.pic.setGeometry(10, 10,800,600)
        # use full ABSOLUTE path to the image, not relative
        self.current_image_path = os.getcwd() +"/1.bmp"
        self.image = QtGui.QImage()
        self.cv2Image = cv2.imread(self.current_image_path, 0)
        self.selectedImage = None #The image, selected via rubberband
        self.image = self.convertCv2ToQimage(self.cv2Image)
        self.pic.setPixmap(QtGui.QPixmap.fromImage(self.image))


        # If you pass a parent to PySide.QtGui.QRubberBand ¡®s constructor,
        # the rubber band will display only inside its parent, but stays on top of other child widgets.
        # If no parent is passed, PySide.QtGui.QRubberBand will act as a top-level widget.
        # self.rubberband = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,)
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self.pic)
        self.setMouseTracking(True)



        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open document')
        openAction.triggered.connect(self.openCall)
        # Create new action
        saveAction = QAction(QIcon('open.png'), '&Save', self)
        saveAction.setShortcut('Ctrl+O')
        saveAction.setStatusTip('Save document')
        saveAction.triggered.connect(self.saveCall)
        # Show the histogram
        showHistogram = QAction(QIcon('open.png'), '&Show histogram', self)
        showHistogram.setStatusTip('Shows the histogram')
        showHistogram.triggered.connect(self.show_histogram)
        # Image Processing
        Action = QAction(QIcon('open.png'), '&Example image processing', self)
        Action.setShortcut('Ctrl+P')
        Action.setStatusTip('Changes the image')
        Action.triggered.connect(self.example_image_processing_method)
        # Create new action
        showDefaultImage = QAction(QIcon('open.png'), '&Show Default Image', self)  # показує дефолтне(відкрите) зображення
        showDefaultImage.setShortcut('Ctrl+D')
        showDefaultImage.setStatusTip('Shows default image')
        showDefaultImage.triggered.connect(self.ShowDefaultImage)
        # Create new action
        self.ShowSelectedImage = QAction(QIcon('open.png'), '&Show', self)
        self.ShowSelectedImage.setShortcut('Ctrl+S')
        self.ShowSelectedImage.setStatusTip('Shows the selected area')
        self.ShowSelectedImage.triggered.connect(self.showSelectedImage)
        # Create new action
        self.SaveSelectedImage = QAction(QIcon('open.png'), '&SaveSelected', self)
        self.SaveSelectedImage.setStatusTip('Saves selected image')
        self.SaveSelectedImage.triggered.connect(self.saveSelectedImage)
        # Create new action
        self.ContrastSelectedImage = QAction(QIcon('open.png'), '&Raise Contract', self)
        self.ContrastSelectedImage.setShortcut('Ctrl+C')
        self.ContrastSelectedImage.setStatusTip('Raises the contrast')
        self.ContrastSelectedImage.triggered.connect(self.raiseContrastSelectedImage)
        # Create new action
        self.HslSelectedImage = QAction(QIcon('open.png'), '&Colorize', self)
        self.HslSelectedImage.setShortcut('Ctrl+H')
        self.HslSelectedImage.setStatusTip('Converting to HSL')
        self.HslSelectedImage.triggered.connect(self.selectedToHsl)

        self.SaveSelectedImage.setEnabled(False)
        self.ContrastSelectedImage.setEnabled(False)
        self.HslSelectedImage.setEnabled(False)
        self.ShowSelectedImage.setEnabled(False)




        # Create menu bar and add action
        menuBar = self.menuBar()
        MenuFile = menuBar.addMenu('&File')
        MenuFile.addAction(openAction)
        MenuFile.addAction(saveAction)




        MenuImage = menuBar.addMenu('&Image')
        MenuImage.addAction(Action)
        MenuImage.addAction(showHistogram)
        MenuImage.addAction(showDefaultImage)

        MenuSelected = menuBar.addMenu('&Selected Image')
        MenuSelected.addAction(self.ShowSelectedImage)
        MenuSelected.addAction(self.SaveSelectedImage)
        MenuSelected.addAction(self.ContrastSelectedImage)
        MenuSelected.addAction(self.HslSelectedImage)





    # def contextMenuEvent(self, event):
    #     x = event.pos().x()
    #     y = event.pos().y()
    #     rect = self.rubberband.geometry()
    #     if x>=rect.x() and x<= (rect.x()+rect.width()) and y>=rect.y() and y<=(rect.y() + rect.height())
    #     menu = QMenu(self)
    #     quitAction = menu.addAction("Quit")
    #     action = menu.exec_(self.mapToGlobal(event.pos()))
    #     if action == quitAction:
    #         qApp.quit()

    def raiseContrastSelectedImage(self):
        self.selectedImage = self.HighContrast(self.selectedImage.copy())

    def selectedToHsl(self):
        self.selectedImage = self.grayScale2BGR(self.selectedImage.copy())

    def saveSelectedImage(self):
        rgb = Image.fromarray(self.selectedImage, mode=None)
        path = QFileDialog.getSaveFileName(self, 'Save File')
        if path:
            print(path)
            rgb.save(path[0])

    def showSelectedImage(self):
        cv2.imshow('Selected Image', self.selectedImage)

    def show_histogram(self):
        plt.hist(self.selectedImage.ravel(), 256, [1, 255])
        plt.show()

    def mousePressEvent(self, event):
        self.rubberband.hide()
        self.ShowSelectedImage.setEnabled(False)
        self.SaveSelectedImage.setEnabled(False)
        self.ContrastSelectedImage.setEnabled(False)
        self.HslSelectedImage.setEnabled(False)
        self.origin = self.pic.mapFromParent(event .pos())
        self.rubberband.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
        self.rubberband.show()
        # QtGui.QWidget.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        rect = self.rubberband.geometry()
        if rect.width() > 10 and rect.height() > 10:
            self.selectedImage = self.cropImage(rect)
            print(type(self.selectedImage))
            self.ShowSelectedImage.setEnabled(True)
            self.SaveSelectedImage.setEnabled(True)
            self.ContrastSelectedImage.setEnabled(True)
            self.HslSelectedImage.setEnabled(True)

    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible():
            # Control the Rubber within the imageViewer!!!
            self.rubberband.setGeometry(QtCore.QRect(self.origin, event .pos()) & self.image.rect())
        # QtGui.QWidget.mouseMoveEvent(self, event)

    def convertQImageToMat(self, incomingImage):
        '''  Converts a QImage into an opencv MAT format  '''

        incomingImage = incomingImage.convertToFormat(4)
        width = incomingImage.width()
        height = incomingImage.height()
        ptr = incomingImage.bits()
        ptr.setsize(incomingImage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
        return cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)

    def convertCv2ToQimage(self, im):
        qim = QImage()
        if im is None:
            return qim
        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                qim.setColorTable([qRgb(i, i, i) for i in range(256)])
            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                elif im.shape[2] == 4:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
        return qim

    def cropImage(self, rect):
        croppedImage = self.image.copy(rect)
        return self.convertQImageToMat(croppedImage)



    def changeLabelPic(self,cv2Image):
        self.image = self.convertCv2ToQimage(cv2Image)
        self.pic.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def saveCall(self):
        rgb = Image.fromarray(self.cv2Image, mode=None)
        path = QFileDialog.getSaveFileName(self, 'Save File')
        if path:
            print(path)
            rgb.save(path[0])

    def openCall(self):
        dlg = QFileDialog()
        # dlg.setFileMode(QFileDialog.AnyFile)
        if dlg.exec_():
            self.current_image_path = dlg.selectedFiles()[0]
            self.setWindowTitle(self.current_image_path)
            self.cv2Image = cv2.imread(self.current_image_path, 0)
            self.changeLabelPic(self.cv2Image)


    def cannyEdges(self):
        edges = cv2.Canny(self.cv2Image, 1, 1)
        self.cv2Image = edges
        cv2.imshow('kek', self.cv2Image)
        # self.cv2Image = cv2.Sobel(self.cv2Image, cv2.CV_8U, 1, 0, ksize=3)

        self.changeLabelPic(self.cv2Image)
        numpyArray = self.cv2Image
        print(numpyArray)

    def grayScale2BGR(self, grayScaleImage):
        hslImage = np.zeros((grayScaleImage.shape[0], grayScaleImage.shape[1], 3), np.uint8)

        for i in range(1, grayScaleImage.shape[0]):
            for j in range(1, grayScaleImage.shape[1] - 2):
                # hslColor = ((int(self.cv2Image[i][j] + abs(int(self.cv2Image[i][j]) - int(self.cv2Image[i][j + 1]))) * 361 / 256), 100, 100)
                hslColor = (int(grayScaleImage[i][j]) * 361 / 256, 100, 100)

                hslImage[i][j] = hslColor
        print(hslColor)
        return cv2.cvtColor(hslImage, cv2.COLOR_HLS2BGR)

    def HighContrast(self, grayImage):
        min = grayImage.min()
        max= grayImage.max()
        Range = max - min
        for i in range(int(grayImage.shape[0])):
            for j in range(int(grayImage.shape[1])):
                grayImage[i][j] = (grayImage[i][j] - min) * (255/Range)
        return grayImage



    def example_image_processing_method(self):  #обробка зображення
        colorized = self.grayScale2BGR(self.cv2Image)
        self.cv2Image = colorized
        # self.cv2Image = self.grayScale2BGR(self.cv2Image.copy())
        # self.cv2Image = cv2.Sobel(self.cv2Image, cv2.CV_8U, 1, 0, ksize=3)

        self.changeLabelPic(self.cv2Image)
        numpyArray = self.cv2Image
        print(numpyArray)



    def ShowDefaultImage(self):
        self.cv2Image = cv2.imread(self.current_image_path,0)
        self.changeLabelPic(self.cv2Image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
sys.exit(app.exec_())
