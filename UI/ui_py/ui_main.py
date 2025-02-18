import sys
from threading import Thread
import time
from time import sleep
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader

import ui_send
import ui_receiver

#ui参数说明
#button1 : 发送    ； button2 :接受   ; button3 : 其他信息


# 在QApplication之前先实例化
uiLoader = QUiLoader()
#扫描接受图像


class Stats:

    def __init__(self):
        # 再加载界面
        self.ui = uiLoader.load(r'..\ui\StartUp.ui')
        #槽函数定义

        self.ui.button1.clicked.connect(self.send_open) #打开发送界面
        self.ui.button2.clicked.connect(self.receiver_open)  # 打开发送界面
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
        thread1 = Thread(target=self.receiver_Window.check_file_existence, args=())
        thread1.start()  # 线程1开始




app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec()