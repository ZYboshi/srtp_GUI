from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal, QThread ,QSize
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
import os
import APIinfo
import sys
import time
from PySide6.QtCore import Qt
#数据
#开始转换按钮：button   原图获取:button1
#原图：label1 , 结果图：label2   512*512
uiLoader = QUiLoader()

class ceshi_window(QObject):
    trans_signal = Signal()
    trans1_signal = Signal()
    trans2_signal = Signal()

    def __init__(self):
        # 再加载界面
        super(ceshi_window, self).__init__()
        self.ui = uiLoader.load(os.path.join('.', 'ui', 'try.ui'))
        self.current_play_index = 0
        self.src_path = os.path.join('.', 'resources', 'receive')
        #槽函数
        self.ui.button1.clicked.connect(self.start_receive)  # 获取图片
       # self.ui.button.clicked.connect(self.trans_start)  # 开始转换
        self.ui.transbutton.clicked.connect(self.open_main)
        self.ui.transbutton1.clicked.connect(self.open_send)
        self.ui.transbutton2.clicked.connect(self.open_receive)
    def open_main(self):
        self.trans_signal.emit()
    def open_send(self):
        self.trans1_signal.emit()
    def open_receive(self):
        self.trans2_signal.emit()

    def start_receive(self):
        print("接收端已启动，等待同步...")
    def update_image(self, edge_pixmap):
        """处理从主窗口传来的图片更新"""
        target_size = QSize(200, 200)  # 设置目标尺寸
        scaled_pix = edge_pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        # 假设ceshi_window也有一个QLabel用于显示
        self.ui.label1.setPixmap(scaled_pix)

        self.current_play_index  = self.current_play_index +1
        self.dst_path = os.path.join(self.src_path, f"{self.current_play_index}.png")
        QTimer.singleShot(50, lambda: print("延时操作完成"))
        pixmap = QPixmap(self.dst_path)
        target_size = QSize(500, 500)
        pixmap = pixmap.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        if not pixmap.isNull():
            self.ui.label2.setPixmap(pixmap)



    def trans_start(self):
        api = APIinfo.ImageProcessor()
        index = api.get_info()
        if index == 1:
            self.pic_open2()


    def pic_open2(self):
            pixmap = QPixmap(os.path.join('.', 'resources', 'receive','output.png'))
            if not pixmap.isNull():
                # 将图片设置到 QLabel 上
                self.ui.label2.setPixmap(pixmap)
            else:
                self.ui.label2.setText("Failed to load image!")


class ImageUpdateThread(QThread):
    # 定义一个信号，用于传递QPixmap到主线程
    image_updated = Signal(QPixmap)
    update_failed = Signal(str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.running = True

    def run(self):
        while self.running:
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                self.image_updated.emit(pixmap)  # 发送图像信号
            else:
                self.update_failed.emit(f"Failed to load image: {self.image_path}")
            time.sleep(1)  # 每秒检查一次（在子线程中sleep不影响UI）

    def stop(self):
        self.running = False
        self.wait()  # 等待线程安全退出



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ceshi_window()
    window.ui.show()
    sys.exit(app.exec())
