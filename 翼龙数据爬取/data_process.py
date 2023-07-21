# This Python file uses the following encoding: utf-8
import json
import os
import matplotlib.pyplot as plt


def paint(data_list):
    # 定义时间和CPU使用率的列表
    time_list = []
    cpu_usage_list = []

    for data in data_list:
        time_list.append(data['时间'])
        cpu_usage_list.append(float(data['CPU使用率'].strip('%')))

    # 创建一个折线图
    plt.plot(time_list, cpu_usage_list)

    # 添加标题和坐标轴标签
    plt.title('CPU使用率随时间变化曲线', fontproperties='SimHei')
    plt.xlabel('时间', fontproperties='SimHei')
    plt.ylabel('CPU使用率(%)', fontproperties='SimHei')

    # 显示图形
    plt.show()


root_dir = './gzznjk'
# 遍历目录树
for dirpath, dirnames, filenames in os.walk(root_dir):
    # 遍历文件名列表
    for filename in filenames:
        # Canvas数据处理
        if filename == 'containerCanvas0.json':
            filepath = os.path.join(dirpath, filename)
            print(filepath)
            with open(filepath, 'r') as f:
                Canvas0_json = f.read()
            Canvas0_list = json.loads(Canvas0_json)
            Canvas0_dic_list = [
                {'时间': s.split('\n')[0], s.split('\n')[1].split(':')[0]: s.split('\n')[1].split(':')[1]} for s in
                Canvas0_list]
        if filename == 'Canvas1.json':
            filepath = os.path.join(dirpath, filename)
            print(filepath)
            with open(filepath, 'r') as f:
                Canvas0_json = f.read()
            Canvas0_list = json.loads(Canvas0_json)
            Canvas0_dic_list = [
                {'时间': s.split('\n')[0], s.split('\n')[1].split(':')[0]: s.split('\n')[1].split(':')[1],
                 s.split('\n')[2].split(':')[0]: s.split('\n')[2].split(':')[1]} for s in
                Canvas0_list]
            print(Canvas0_dic_list)
        if filename == 'Canvas2.json':
            filepath = os.path.join(dirpath, filename)
            print(filepath)
            with open(filepath, 'r') as f:
                Canvas0_json = f.read()
            Canvas0_list = json.loads(Canvas0_json)
            Canvas0_dic_list = [
                {'时间': s.split('\n')[0], s.split('\n')[1].split(':')[0]: s.split('\n')[1].split(':')[1],
                 s.split('\n')[2].split(':')[0]: s.split('\n')[2].split(':')[1]} for s in
                Canvas0_list]
            print(Canvas0_dic_list)
