from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal, QThread
import os
import APIinfo
uiLoader = QUiLoader()


#参数:
#获取图片按钮:button1_1 ; 发送按钮:button1_2
#Label: 原图：label_2  ; 图片放置:label11 ; 当前连接设备；label_3
#显示连接line : lineEdit
class send_Window(QObject):
    def __init__(self):
        # 再加载界面
        super().__init__()
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



#
class ClassifyProcessorThread(QThread):

    result_signal = Signal(int, str)  # (状态码, 消息)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = os.path.join('.', 'resources', 'send.png')
        self.running = False
        self.processor = APIinfo.ClassifyProcessor(
            input_path=self.image_path,
        )

    def run(self):
        self.running = True
        while self.running:
            try:
                result = self.processor.get_info()
                if result == 0:
                    self.result_signal.emit(0, "处理成功")
                if result == 1:  # success
                    self.result_signal.emit(1, "处理成功")
                elif result == 2:  # error
                    self.result_signal.emit(2, "服务错误")
                else:
                    self.result_signal.emit(3, "未知状态")
                self.msleep(1000)
            except Exception as e:
                self.result_signal.emit(4, f"异常错误: {str(e)}")



