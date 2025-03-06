import os
import time
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtWidgets import QApplication

import sys
import Watch_dog
uiLoader = QUiLoader()


#参数:
#Label: 图片放置：label1
#显示连接line : lineEdit   ； 图片获取：lineEdit1
#接收图片：button
class receiver_Window(QObject):

    pic_triggered = Signal() #信号

    def __init__(self):
        super().__init__()
        # 再加载界面
        self.ui = uiLoader.load(r'.\ui\receiver.ui')
        #槽函数
        self.ui.button.clicked.connect(self.monitor_open)  # 获取图片
        self.pic_triggered.connect(self.pic_open)

        self.monitor_thread = None
        self.monitor = None



    def monitor_open(self):
        # 创建监控实例并传入回调(通过lambda捕获self)
        self.monitor = Watch_dog.FolderMonitor(
            folder_path=r'.\resources',
            target_file="pic1.png",  #想要得到的图片名称
            callback=lambda: self.pic_triggered.emit()  # 触发信号
        )
        # 使用QThread管理监控线程
        self.monitor_thread = QThread()
        self.monitor.moveToThread(self.monitor_thread)
        self.monitor_thread.started.connect(self.monitor.start)
        self.monitor_thread.start()



    def pic_open(self):
        print("正在加载图片...")
        pixmap = QPixmap(r'.\resources\pic1.png')
        if not pixmap.isNull():
            self.ui.label1.setPixmap(pixmap)

        else:
            self.ui.label1.setText("图片加载失败!")




    """
    #定时扫描
    def check_file_existence(self):
        folder_path = r'..\ ui_py \ resources'  # 这里表示当前文件夹，可换成目标文件夹路径
        file_name = "pic1.png"
        while True:
            file_path = os.path.join(folder_path, file_name)
            if os.path.exists(file_path):
                self.ui.lineEdit1.setText("成功获取图片")
            else:
                self.ui.lineEdit1.setText("图片尚未传达到")
            time.sleep(5)  # 间隔5秒扫描一次，可按需修改
    """


