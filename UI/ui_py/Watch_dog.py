import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PySide6.QtCore import QObject

class FolderMonitor(QObject):
    def __init__(self, folder_path=".", target_file="pic1.png",callback=None):
        super().__init__()
        self.folder_path = folder_path
        self.target_file = target_file
        self.callback = callback  # 新增回调函数参数
        self.observer = None

    def start(self):
        class Handler(FileSystemEventHandler):
            def __init__(self, target,callback):
                super().__init__()
                self.target = target
                self.callback = callback

            def on_created(self, event):
                if not event.is_directory and event.src_path.endswith(self.target):
                    print(f"检测到 {self.target}，触发操作")

                    if self.callback:
                        self.callback()  # 触发回调函数
        event_handler = Handler(self.target_file, self.callback)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.folder_path, recursive=False)
        self.observer.start()

        try:
            while True:  # 保持主线程运行
                time.sleep(1)
                print("监控运行中...")
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("监控已停止")


if __name__ == "__main__":
    # 使用示例
    monitor = FolderMonitor(folder_path= r'..\ui_py\resources', target_file="pic1.png")
    monitor.start()