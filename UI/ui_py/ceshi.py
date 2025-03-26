from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtWidgets import QApplication
import os
import APIinfo
import sys
#数据
#开始转换按钮：button   原图获取:button1
#原图：label1 , 结果图：label2   512*512
uiLoader = QUiLoader()

class ceshi_window(QObject):
    trans_signal = Signal()
    trans1_signal = Signal()
    trans2_signal = Signal()

    def __init__(self):
        # 再加载界面
        super(ceshi_window, self).__init__()
        self.ui = uiLoader.load(os.path.join('.', 'ui', 'try.ui'))
        #槽函数
        self.ui.button1.clicked.connect(self.pic_open)  # 获取图片
        self.ui.button.clicked.connect(self.trans_start)  # 开始转换
        self.ui.transbutton.clicked.connect(self.open_main)
        self.ui.transbutton1.clicked.connect(self.open_send)
        self.ui.transbutton2.clicked.connect(self.open_receive)
    def open_main(self):
        self.trans_signal.emit()
    def open_send(self):
        self.trans1_signal.emit()
    def open_receive(self):
        self.trans2_signal.emit()

    def pic_open(self):
            pixmap = QPixmap(os.path.join('.', 'resources','receive','input.png'))
            if not pixmap.isNull():
                # 将图片设置到 QLabel 上
                self.ui.label1.setPixmap(pixmap)
            else:
                self.ui.label1.setText("Failed to load image!")


    def trans_start(self):
        api = APIinfo.ImageProcessor()
        index = api.get_info()
        if index == 1:
            self.pic_open2()


    def pic_open2(self):
            pixmap = QPixmap(os.path.join('.', 'resources', 'receive','output.png'))
            if not pixmap.isNull():
                # 将图片设置到 QLabel 上
                self.ui.label2.setPixmap(pixmap)
            else:
                self.ui.label2.setText("Failed to load image!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ceshi_window()
    window.ui.show()
    sys.exit(app.exec())
