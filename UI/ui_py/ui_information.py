
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtWidgets import QApplication

import sys
import Watch_dog





uiLoader = QUiLoader()


#参数:
#获取图片按钮:button3
#Label: 骨架图：label3_0  ;
#prompt:textBrowser;



class information_Window(QObject):
    pic_triggered = Signal()
    def __init__(self):
        # 再加载界面
        super().__init__()
        self.ui = uiLoader.load(r'.\ui\information.ui')
        #槽函数
        self.ui.button3.clicked.connect(self.monitor_open)  # 获取图片
        self.pic_triggered.connect(self.pic_open)

        self.monitor_thread = None
        self.monitor = None

    def monitor_open(self):
        # 创建监控实例并传入回调(通过lambda捕获self)
        self.monitor = Watch_dog.FolderMonitor(
            folder_path=r'.\resources',
            target_file="pic1.png",
            callback=lambda: self.pic_triggered.emit()  # 触发信号
        )



        # 使用QThread管理监控线程
        self.monitor_thread = QThread()
        self.monitor.moveToThread(self.monitor_thread)
        self.monitor_thread.started.connect(self.monitor.start)
        self.monitor_thread.start()

    def pic_open(self):
        print("正在加载图片...")
        pixmap = QPixmap(r'..\ui_py\resources\pic1.png')
        if not pixmap.isNull():
            self.ui.label3_0.setPixmap(pixmap)
        else:
            self.ui.label3_0.setText("图片加载失败!")

        try:
            # 读取文件（注意文件路径！）
            with open(r'..\ui_py\resources\prompt.txt', "r", encoding="utf-8") as f:
                content = f.read()
            self.ui.textBrowser.setPlainText(content)
        except FileNotFoundError:
            self.ui.textBrowser.setPlainText("错误：未找到 str1.txt 文件")
        except Exception as e:
            self.ui.textBrowser.setPlainText(f"读取错误：{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = information_Window()
    window.ui.show()
    sys.exit(app.exec())


