# This Python file uses the following encoding: utf-8
import json
import os

root_dir = './gzznjk'
# 遍历目录树
for dirpath, dirnames, filenames in os.walk(root_dir):
    # 遍历文件名列表
    for filename in filenames:
        # Canvas数据处理
        if filename == 'Canvas0.json':
            filepath = os.path.join(dirpath, filename)
            print(filepath)
            with open(filepath, 'r') as f:
                Canvas0_json = f.read()
            Canvas0_list = json.loads(Canvas0_json)
            Canvas0_dic_list = [
                {'时间': s.split('\n')[0], s.split('\n')[1].split(':')[0]: s.split('\n')[1].split(':')[1]} for s in
                Canvas0_list]
            print(Canvas0_dic_list)
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