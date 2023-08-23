# This Python file uses the following encoding: utf-8
import requests


def send_data_to_server(server_url, data):
    try:
        # 发送POST请求将数据发送到服务器
        response = requests.post(server_url, data=data)

        if response.status_code == 200:
            print("Data sent successfully to the server.")
        else:
            print(f"Failed to send data to the server. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")


if __name__ == '__main__':
    # 服务器的URL和端点
    server_url = 'http://132.97.54.148//endpoint'  # 替换为实际的服务器URL和端点

    # 要发送的数据
    data_to_send = {'key1': 'value1', 'key2': 'value2'}  # 替换为实际的数据

    # 发送数据到服务器
    send_data_to_server(server_url, data_to_send)
