import cv2
import sys
import logging
import os
from PySide6.QtCore import QObject,Signal, QThread,QSize,QTimer

from PySide6.QtGui import QPixmap,QImage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#摄像头获取
class CameraApp(QThread):
    frame_ready = Signal(QImage)
    error_occurred = Signal(str, str)
    def __init__(self):
        # 初始化摄像头
        super().__init__()
        self.save_dir = os.path.join('.', 'resources','video')

        self.cap = cv2.VideoCapture(21)  # 摄像头设备号
        self.running = False

        if not self.cap.isOpened():
            logger.error("无法打开摄像头")
            self.error_occurred.emit("错误", "无法打开摄像头")
            #sys.exit(1)

        # 计数器，用于生成唯一的文件名
        self.frame_count = 0
    def run(self):
        self.running = True
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # 显示帧（可选）
                # 将 OpenCV 图像转换为 QImage
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换为 RGB 格式
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.frame_ready.emit(q_img)

                # 保存帧到本地
                self.save_frame(frame)
            else:
                logger.error("摄像头读取失败")
                self.error_occurred.emit("错误", "无法读取帧")
                self.cap.release()
                cv2.destroyAllWindows()
                break
            self.msleep(30)  # 控制帧率

    def clear_images(self):
        """清空图片文件夹"""
        if self.save_dir and os.path.exists(self.save_dir):
            for file in os.listdir(self.save_dir):
                file_path = os.path.join(self.save_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            logger.info(f"已清空文件夹: {self.save_dir}")
    def save_frame(self, frame):
        # 生成文件名
        yuantu_path = os.path.join(self.save_dir, "yuantu.png")
        yuantu_1_path = os.path.join(self.save_dir, "yuantu_1.png")

        # 如果 yuantu_1.png 存在，则将其重命名为 yuantu.png
        if os.path.exists(yuantu_1_path):
            os.replace(yuantu_1_path, yuantu_path)

        # 保存当前帧为 yuantu_1.png
        cv2.imwrite(yuantu_1_path, frame)
        logger.info(f"已保存图像: {yuantu_1_path}")


    def stop(self):
        # 释放摄像头资源
        self.running = False
        self.wait()  # 等待线程结束
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.clear_images()