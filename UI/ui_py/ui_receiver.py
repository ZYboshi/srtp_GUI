import os
import time
from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap

uiLoader = QUiLoader()


#参数:
#Label: 图片放置：label1
#显示连接line : lineEdit   ； 图片获取：lineEdit1
class receiver_Window():
    def __init__(self):
        # 再加载界面
        self.ui = uiLoader.load(r'..\ui\receiver.ui')
        #槽函数


    #定时扫描
    def check_file_existence(self):
        folder_path = r'..\ui_py\resources'  # 这里表示当前文件夹，可换成目标文件夹路径
        file_name = "pic.png"
        while True:
            file_path = os.path.join(folder_path, file_name)
            if os.path.exists(file_path):
                self.ui.lineEdit1.setText("成功获取图片")
            else:
                self.ui.lineEdit1.setText("图片尚未传达到")
            time.sleep(5)  # 间隔5秒扫描一次，可按需修改