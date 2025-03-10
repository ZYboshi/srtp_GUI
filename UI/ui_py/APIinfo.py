import requests
import json
import base64
import os

def get_info():

    input_image_path = os.path.join('.', 'resources', 'input.png')  # 要发送的图片路径
    output_image_path = os.path.join('.', 'resources', 'output.png')  # 要保存的返回图片路径
    url = "http://localhost:8080"
    headers = {
        "Content-Type": "application/octet-stream",
        "Accept": "application/octet-stream",
    }
    try:
        with open(input_image_path, "rb") as f:
            image_data = f.read()

        response = requests.post(url, headers=headers, data=image_data)

        response_json = response.json()
        print(response_json)
        status = response_json["status"]
        if  status == "success":
            img_data = base64.b64decode(response_json["result"])
            with open("output.jpg", "wb") as f:
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





