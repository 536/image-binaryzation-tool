import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from PIL import Image
from PIL.ImageQt import ImageQt

from lib import binaryzation


class Picture(QLabel):
    def __init__(self, parent=None):
        super(Picture, self).__init__(parent)
        self.setStyleSheet('background: #AAA;')
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.pix = None
        self.img = None
        self.processed_img = None
        self.img_width = 0
        self.img_height = 0

    def load_img(self, pix=None):
        if pix:
            self.processed_img = pix
            p = pix
        else:
            p = self.pix
        if p:
            self.setPixmap(p.scaled(*self.get_appropriate_size()))

    def get_appropriate_size(self, size=None):
        s = size if size else self
        width, height = s.width(), s.height()

        if (width / height) > (self.img_width / self.img_height):
            return height * (self.img_width / self.img_height), height
        else:
            return width, width / (self.img_width / self.img_height)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        mime = event.mimeData()
        if mime.hasUrls():
            file = mime.urls()[0].toLocalFile()
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.pix = QPixmap(mime.urls()[0].toLocalFile())
                self.img = Image.open(mime.urls()[0].toLocalFile())
                self.img_width, self.img_height = self.img.size
                self.load_img()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.load_img()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.load_img(self.processed_img)

    def resizeEvent(self, event):
        self.load_img(self.processed_img)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__(flags=QtCore.Qt.WindowStaysOnTopHint)

        self.pix = Picture(self)
        self.slider = QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 255)
        self.slider.valueChanged.connect(self.process_pix)
        action_save = QAction('Save', self)
        action_save.setShortcut('Ctrl+S')
        action_save.triggered.connect(self.save)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.pix)
        layout.addWidget(self.slider)
        self.addAction(action_save)
        self.setLayout(layout)

    def process_pix(self, value):
        img = binaryzation(self.pix.img, threshold=value, alpha=FLAG)
        self.pix.load_img(QPixmap.fromImage(ImageQt(img)))

    def save(self):
        if self.pix.processed_img:
            save_path, _ = QFileDialog.getSaveFileName(self, filter='*.png')
            if save_path:
                self.pix.processed_img.save(save_path)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        FLAG = bool(sys.argv[1] == 'alpha')
    else:
        FLAG = False

    QApplication.setStyle('fusion')
    app = QApplication(sys.argv)
    win = MainWindow()
    win.setMinimumSize(500, 350)
    win.show()
    sys.exit(app.exec_())
