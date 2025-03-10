import sys
from threading import Thread
import os
from os.path import join
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader

import ui_send
import ui_receiver
import ui_information
#ui参数说明
#button1 : 发送    ； button2 :接受   ; button3 : 其他信息


# 在QApplication之前先实例化
uiLoader = QUiLoader()
#扫描接受图像


class Stats:

    def __init__(self):
        # 再加载界面
        self.ui = uiLoader.load(os.path.join('.', 'ui', 'StartUp.ui'))
        #槽函数定义

        self.ui.button1.clicked.connect(self.send_open) #打开发送界面
        self.ui.button2.clicked.connect(self.receiver_open)  # 打开发送界面
        self.ui.button3.clicked.connect(self.information_open)  # 打开发送界面
    #打开新窗口
    #实例化另外一个窗口，显示新窗口，关闭老窗口
    def send_open(self):
        self.send_Window = ui_send.send_Window()
        self.send_Window.ui.show()
        self.ui.hide()
    def receiver_open(self):
        self.receiver_Window = ui_receiver.receiver_Window()
        self.receiver_Window.ui.show()
        self.ui.hide()


    def information_open(self):
        self.information_Window = ui_information.information_Window()
        self.information_Window.ui.show()
        self.ui.hide()


if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec()