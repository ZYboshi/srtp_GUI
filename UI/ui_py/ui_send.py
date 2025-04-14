from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap,QImage
from PySide6.QtCore import QObject, Signal, QThread ,QSize
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QApplication,QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
import ui_camera
import os
import APIinfo
import cv2
import shutil
import time
uiLoader = QUiLoader()






#参数:
#获取图片按钮:button1_1 ; 发送按钮:button1_2
#Label: 原图：labelvedio ; 边缘图片放置:label11 ; 当前连接设备；label_3
#显示连接line : lineEdit
#label:显示状态
class send_Window(QObject):
    image_updated = Signal(QPixmap)
    trans_signal = Signal()
    trans1_signal = Signal()
    trans2_signal = Signal()

    def __init__(self):
        # 再加载界面
        super().__init__()
        self.ui = uiLoader.load(os.path.join('.', 'ui', 'send.ui'))
        self.movie1 = QMovie(os.path.join('.', 'resources', 'icon_ok.gif'))
        self.movie2 = QMovie(os.path.join('.', 'resources', 'icon_warning.gif'))
        self.movie1.setScaledSize(QSize(80, 80))
        self.movie2.setScaledSize(QSize(80, 80))
        """       
        self.camera_thread = ui_camera.CameraApp()
        self.camera_thread.frame_ready.connect(self.display_frame)
        self.camera_thread.start()
        """
        #槽函数
        #self.ui.button1_1.clicked.connect(self.task_begin)  # 获取图片
        #self.ui.button1_3.clicked.connect(self.camera_open)
        self.ui.button1_3.clicked.connect(self.vedio_on)
        """
        self.camera_thread.error_occurred.connect(self.show_error_message)
        """
        self.ui.transbutton.clicked.connect(self.open_main)
        self.ui.transbutton1.clicked.connect(self.open_send)
        self.ui.transbutton2.clicked.connect(self.open_receive)
    def open_main(self):
        self.trans_signal.emit()
    def open_send(self):
        self.trans1_signal.emit()
    def open_receive(self):
        self.trans2_signal.emit()

    #直接播放图片
    def vedio_on(self):
        self.target_dir = os.path.join('.', 'resources', 'send')
        self.image_list = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png","8.png", "9.png"]
        self.current_image_index = 0  # 当前处理的图片索引

        # 创建定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.copy_next_image)
        self.timer.start(1000)  # 1秒触发一次


    def copy_next_image(self):
        if self.current_image_index < len(self.image_list):
            img = self.image_list[self.current_image_index]
            src_path = os.path.join(self.target_dir, img)
            dst_path = os.path.join(self.target_dir, "yuantu.png")

            if os.path.exists(src_path):
                # 1. 复制原图并显示到labelvideo
                shutil.copy(src_path, dst_path)

                pixmap = QPixmap(dst_path)
                target_size = QSize(500, 500)
                pixmap = pixmap.scaled(
                    target_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                if not pixmap.isNull():
                    self.ui.labelvideo.setPixmap(pixmap)

                # 2. 生成轮廓图并显示到label11
                img_cv = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)
                edges = cv2.Canny(img_cv, 50, 150)  # Canny边缘检测

                # 将OpenCV图像转为QPixmap
                height, width = edges.shape
                q_img = QImage(edges.data, width, height, width, QImage.Format_Grayscale8)
                edge_pixmap = QPixmap.fromImage(q_img).scaled(
                    QSize(200, 200),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_updated.emit(edge_pixmap)
                if not edge_pixmap.isNull():
                    self.ui.label11.setPixmap(edge_pixmap)
                    self.movie_start(2)
                print(f"已处理 {src_path} (原图+轮廓图)")
            else:
                print(f"警告: 文件 {src_path} 不存在")

            self.current_image_index += 1
        else:
            print("所有图片处理完成")
            self.timer.stop()

    def camera_open(self):
        self.camera_thread = ui_camera.CameraApp()
        self.camera_thread.frame_ready.connect(self.display_frame)
        self.camera_thread.start()
        self.camera_thread.error_occurred.connect(self.show_error_message)
        self.ui.button1_2.clicked.connect(self.camera_thread.stop)  # 关闭摄像头 ，清除图片文件
    def show_error_message(self, title, message):
        QMessageBox.critical(self.ui, title, message)

    def display_frame(self, q_img):
        """将帧显示在 QLabel 上"""
        # 将 QImage 转换为 QPixmap 并显示到 QLabel 上
        target_size = QSize(512, 512)  # 宽度 512，高度 512
        pixmap = QPixmap.fromImage(q_img).scaled(target_size)
        self.ui.labelvideo.setPixmap(pixmap)


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
        if status == 1:
            pic_name = os.path.join('.', 'resources', 'send', 'yuantu.png')
            image = cv2.imread(pic_name, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(image, threshold1 = 50, threshold2 = 150, apertureSize=3, L2gradient=False)
            height, width = edges.shape
            q_img = QImage(edges.data, width, height, width, QImage.Format_Grayscale8)
            output_path = os.path.join('.', 'resources', 'send', 'gujia.png')
            q_img.save(output_path)
            pixmap = QPixmap.fromImage(q_img)
            pixmap = pixmap.scaled(
                self.ui.label11.size(),  # 直接使用 QLabel 的当前尺寸
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation  # 平滑缩放
            )
            self.ui.label11.setPixmap(pixmap)
            self.movie_start(2)
        elif status == 0:
            self.movie_start(1)
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

