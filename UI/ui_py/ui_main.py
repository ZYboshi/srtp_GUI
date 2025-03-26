import sys
from threading import Thread
import os
from os.path import join
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader

import ui_send
import ui_receiver
import ui_information
import ceshi
#ui参数说明
#button1 : 发送    ； button2 :接受   ; button3 : 其他信息


# 在QApplication之前先实例化
uiLoader = QUiLoader()
#扫描接受图像


class Stats:

    def __init__(self):
        # 再加载界面
        self.send_window = None
        self.receiver_window = None
        self.information_Window = None
        self.ui = uiLoader.load(os.path.join('.', 'ui', 'StartUp.ui'))
        #槽函数定义

        self.ui.button1.clicked.connect(self.send_open) #打开发送界面
        self.ui.button2.clicked.connect(self.receiver_open)  # 打开发送界面
        self.ui.button3.clicked.connect(self.information_open)  # 打开发送界面

    #打开新窗口
    #实例化另外一个窗口，显示新窗口，关闭老窗口
    def main_open(self):
        self.ui.show()
    def send_open(self):
        if self.send_window is None:
            self.send_window = ui_send.send_Window()
            # 重写关闭事件为隐藏
            self.send_window.ui.closeEvent = lambda event: self.send_window.ui.hide()
            self.send_window.trans_signal.connect(self.main_open)
            self.send_window.trans1_signal.connect(self.send_open)
            self.send_window.trans2_signal.connect(self.receiver_open)
        self.send_window.ui.show()
        self.ui.hide()
    def receiver_open(self):
        if self.receiver_window is None:
            self.receiver_window = ceshi.ceshi_window()
            self.receiver_window.ui.closeEvent = lambda event: self.receiver_window.ui.hide()
            self.receiver_window.trans_signal.connect(self.main_open)
            self.receiver_window.trans1_signal.connect(self.send_open)
            self.receiver_window.trans2_signal.connect(self.receiver_open)
        self.receiver_window.ui.show()
        self.ui.hide()


    def information_open(self):
        if self.information_Window is None:
            self.information_Window = ui_information.information_Window()
            self.information_Window.ui.closeEvent = lambda event: self.information_Window.ui.hide()
        self.information_Window.ui.show()
        self.ui.hide()


if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec()