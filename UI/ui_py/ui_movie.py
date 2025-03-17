from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal, QThread ,QSize
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication
import os
import time
import APIinfo
uiLoader = QUiLoader()


#参数:
#获取图片按钮:button1_1 ; 发送按钮:button1_2
#Label: 原图：label_2  ; 图片放置:label11 ; 当前连接设备；label_3
#显示连接line : lineEdit
#label:显示状态
class send_Window(QObject):
    def __init__(self):
        # 再加载界面
        super().__init__()
        self.ui = uiLoader.load(os.path.join('.', 'ui', 'send.ui'))
        self.movie1 = QMovie(os.path.join('.', 'resources', 'icon_ok.gif'))
        self.movie2 = QMovie(os.path.join('.', 'resources', 'icon_warning.gif'))
        self.movie1.setScaledSize(QSize(80, 80))
        self.movie2.setScaledSize(QSize(80, 80))
        #槽函数

    def movie_start(self,status):
        if status == 1:
            self.ui.label.setMovie(self.movie1)
            self.movie1.start()
        if status == 2:
            self.ui.label.setMovie(self.movie2)
            self.movie2.start()

if __name__ == "__main__":
    app = QApplication([])
    window = send_Window()
    window.ui.show()
    window.movie_start(1)

    window.movie_start(2)
    app.exec()

