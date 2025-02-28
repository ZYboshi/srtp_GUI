# 尚未完成内容：
* 与模型的连接：以什么形式启动模型  ：即发送按钮（ui_send）
* 通信设备连接显示
* 相关数据显示
___
# GUI操作说明
## ui_send
* 获取发送图片:图片address：resources\pic.png
## ui_receiver
* 获取接收图片:图片address：resources\pic1.png

## ui_information
* 中间信息：骨架图+prompt
## 接收信息
* 已完成异步信息接收，主要通过：watchdog（进行文件系统监控，增强效率） 信号和槽函数（信号传递）