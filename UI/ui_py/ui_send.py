from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
import os
uiLoader = QUiLoader()


#参数:
#获取图片按钮:button1_1 ; 发送按钮:button1_2
#Label: 原图：label_2  ; 图片放置:label11 ; 当前连接设备；label_3
#显示连接line : lineEdit
class send_Window():
    def __init__(self):
        # 再加载界面
        self.ui = uiLoader.load(os.path.join('.', 'ui', 'send.ui'))
        #槽函数
        self.ui.button1_1.clicked.connect(self.pic_open)  # 获取图片


    def pic_open(self):
        pixmap = QPixmap(os.path.join('.', 'resources', 'pic.png'))
        if not pixmap.isNull():
            # 将图片设置到 QLabel 上
            self.ui.label11.setPixmap(pixmap)
        else:
            self.ui.label11.setText("Failed to load image!")
