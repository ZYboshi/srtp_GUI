import requests
import json
import base64
import os

# 更改成类
class ImageProcessor:
    def __init__(
            self,
            input_path=None,
            output_path=None,
            url=None,
            headers=None
    ):
        """
        初始化图像处理器

        :param input_path: 输入图片路径（默认'./resources/input.png'）
        :param output_path: 输出图片路径（默认'./resources/output.png'）
        :param url: 服务端地址（默认'http://localhost:8080'）
        :param headers: 请求头（默认使用octet-stream类型）
        """
        self.input_image_path = input_path or os.path.join('.', 'resources', 'input.png')
        self.output_image_path = output_path or os.path.join('.', 'resources', 'output.png')
        self.url = url or "http://localhost:8080/revert"
        self.headers = headers or {
            "Content-Type": "application/octet-stream",
            "Accept": "application/octet-stream",
        }

    def get_info(self):
        try:
            with open(self.input_image_path, "rb") as f:
                image_data = f.read()

            response = requests.post(self.url, headers=self.headers, data=image_data)

            response_json = response.json()
            print(response_json)
            status = response_json["status"]
            if  status == "success":
                img_data = base64.b64decode(response_json["result"])
                with open(self.output_image_path, "wb") as f:
                    f.write(img_data)
                print("转换成功")
                return 1

            elif status == "error":
                print(f"服务错误: {response_json.get('message', '未知错误')}")
                return 2
            else:
                print("无效响应格式")
                return 3

        except requests.exceptions.JSONDecodeError:
            print("响应不是有效的 JSON")

        except Exception as e:
            print(f"操作失败: {str(e)}")


class ClassifyProcessor:
    ACCIDENT = 1
    OTHER    = 0
    def __init__(
            self,
            input_path=None,
            output_path=None,
            url=None,
            headers=None
    ):
        """
        初始化图像处理器

        :param input_path: 输入图片路径（默认'./resources/input.png'）
        :param output_path: 输出图片路径（默认'./resources/output.png'）
        :param url: 服务端地址（默认'http://localhost:8080'）
        :param headers: 请求头（默认使用octet-stream类型）
        """
        self.input_image_path = input_path or os.path.join('.', 'resources', 'input.png')
        self.output_image_path = output_path or os.path.join('.', 'resources', 'output.png')
        self.url = url or "http://localhost:8080/classify"
        self.headers = headers or {
            "Content-Type": "application/octet-stream",
            "Accept": "application/octet-stream",
        }

    def get_info(self):
        try:
            with open(self.input_image_path, "rb") as f:
                image_data = f.read()

            response = requests.post(self.url, headers=self.headers, data=image_data)

            response_json = response.json()
            print(response_json)
            status = response_json["status"]
            if  status == "success":
                print("转换成功")
                result = response_json.get("result")
                if result == "success":
                    return self.ACCIDENT
                if result == "other":
                    return self.OTHER

            elif status == "error":
                print(f"服务错误: {response_json.get('message', '未知错误')}")
                return 2
            else:
                print("无效响应格式")
                return 3

        except requests.exceptions.JSONDecodeError:
            print("响应不是有效的 JSON")

        except Exception as e:
            print(f"操作失败: {str(e)}")
