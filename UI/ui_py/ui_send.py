from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal, QThread ,QSize
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication
import os
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
        self.ui.button1_1.clicked.connect(self.task_begin)  # 获取图片

    def pic_open(self,pic_name):
        pixmap = QPixmap(os.path.join('.', 'resources', 'send',pic_name))
        if not pixmap.isNull():
            # 将图片设置到 QLabel 上
            self.ui.label11.setPixmap(pixmap)
        else:
            self.ui.label11.setText("Failed to load image!")

    def task_begin(self):
        print("开启线程")
        self.processor_thread = ClassifyProcessorThread()
        self.processor_thread.result_signal.connect(self.task_work)
        self.processor_thread.start()

    #accident:1  other:0
    def task_work(self,status,message):
        print(status,message)
        if status == 0:
            pic_name = 'yuantu.png'
            self.pic_open(pic_name)
            self.movie_start(1)
        if status == 1:
            pic_name = 'yuantu.png'
            self.pic_open(pic_name)
            self.movie_start(2)
        else:
            self.ui.label.setText("出现问题，请检查")


    def movie_start(self,status):
        if status == 1:
            self.ui.label.setMovie(self.movie1)
            self.movie1.start()
        if status == 2:
            self.ui.label.setMovie(self.movie2)
            self.movie2.start()


#QThread使用：重写run函数即可
#
class ClassifyProcessorThread(QThread):
    result_signal = Signal(int, str)  # (状态码, 消息)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = os.path.join('.', 'resources','send','yuantu.png')
        self.running = False
        self.processor = APIinfo.ClassifyProcessor(
            input_path=self.image_path,
        )

    def run(self):
        print("正在运行中")
        self.running = True
        while self.running:
            try:
                print("进入try")
                result = self.processor.get_info()
                if result == 0:
                    self.result_signal.emit(0, "处理成功")
                if result == 1:  # success
                    self.result_signal.emit(1, "处理成功")
                elif result == 2:  # error
                    self.result_signal.emit(2, "服务错误")
                else:
                    self.result_signal.emit(3, "未知状态")
                self.msleep(5000)
            except Exception as e:
                print("进入except")
                self.result_signal.emit(4, f"异常错误: {str(e)}")
                self.msleep(5000)


if __name__ == "__main__":
    app = QApplication([])
    window = send_Window()
    window.ui.show()
    app.exec()

