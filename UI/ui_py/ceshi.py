from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal, QThread
import os
import APIinfo

#数据
#开始转换按钮：button   原图获取:button1
#原图：label1 , 结果图：label2   512*512
uiLoader = QUiLoader()

class ceshi_window(QObject):
    def __init__(self):
        # 再加载界面
        super(ceshi_window, self).__init__()
        self.ui = uiLoader.load(os.path.join('.', 'ui', 'try.ui'))
        #槽函数
        self.ui.button1.clicked.connect(self.pic_open)  # 获取图片
        self.ui.button.clicked.connect(self.trans_start)  # 开始转换

    def pic_open(self):
            pixmap = QPixmap(os.path.join('.', 'resources', 'input.png'))
            if not pixmap.isNull():
                # 将图片设置到 QLabel 上
                self.ui.label1.setPixmap(pixmap)
            else:
                self.ui.label1.setText("Failed to load image!")


    def trans_start(self):
        index = APIinfo.get_info()
        if index == 1:
            self.pic_open2()


    def pic_open2(self):
            pixmap = QPixmap(os.path.join('.', 'resources', 'output.png'))
            if not pixmap.isNull():
                # 将图片设置到 QLabel 上
                self.ui.label2.setPixmap(pixmap)
            else:
                self.ui.label2.setText("Failed to load image!")



