# This Python file uses the following encoding: utf-8
# 保存文件，并发送数据库
import json
import os

import MySQLdb
import requests
import time
from datetime import datetime
import datetime
import shutil
import os

with open('cookie.json', 'r') as f:
    json_cookies = f.read()
cookie_list = json.loads(json_cookies)
for cookie in cookie_list:
    # 复制cookie字典
    cookie_dict = cookie.copy()

conn = MySQLdb.connect(host='localhost', user='root', password='fzs123456', db='test')


def remove_folder(path):
    """递归删除文件夹及其内容"""
    if os.path.isdir(path):
        shutil.rmtree(path)


# 使用json读取cookies
def send_data(data_list, space_name, pod_name):
    # 创建游标
    cursor = conn.cursor()
    if not data_list is None:
        for item in data_list:
            print(item)
            # 执行 INSERT 语句
            cursor.execute(
                "INSERT INTO canvas_data (`id`, `time`, `value`, `name`,`space_name`,`pod_name`) VALUES ("
                "NULL, %s, %s, %s,%s, %s)",
                (item['time'], item['value'], item['name'], space_name, pod_name))
            # 提交事务
            conn.commit()
    cursor.close()


# 创建表格
def create_table():
    # 创建游标对象
    cursor = conn.cursor()

    # 定义创建表格的SQL语句
    create_table_sql = "CREATE TABLE canvas_data (id int NOT NULL AUTO_INCREMENT PRIMARY KEY,time VARCHAR(50) ,name VARCHAR(" \
                       "50) ,value VARCHAR(50),space_name VARCHAR(50),pod_name VARCHAR(50)) "

    # 执行SQL语句，创建表格
    cursor.execute(create_table_sql)

    # 提交更改
    conn.commit()

    # 关闭游标和连接
    cursor.close()


# 删除表中的数据
def delete_data():
    # 创建游标
    cursor = conn.cursor()

    # 执行 INSERT 语句
    cursor.execute("TRUNCATE TABLE canvas_data")
    # 提交事务
    conn.commit()
    cursor.close()


# {code: 0, data: [{id: 19, name: "dmz-fgs-ccse"}]}
def cluster_get():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }

    cluster_list = requests.get(
        "http://www.ctgpaas.cn:9000/dcos/cluster/csCluster/pulldownList",
        headers=headers)
    print(cluster_list.text)
    cluster_list = cluster_list.json()["data"]
    return cluster_list


# 返回一个含有所有命名空间的列表
def namespace_get(clusterId):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    namespace_list = \
        requests.get(
            f"http://www.ctgpaas.cn:9000/dcos/cluster/namespace/page?pageNow=1&pageSize=100&keywords=&clusterId={clusterId}",
            headers=headers).json()['data']['records']
    return namespace_list


# 获取基本信息
def inf_get(clusterId, namespace):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    inf = requests.get(f"http://www.ctgpaas.cn:9000/dcos/cluster/namespace/{clusterId}/{namespace}",
                       headers=headers).json()
    return inf


# 获取工作负载
def list_get(clusterId, namespace, workloadKind):
    l = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
        'Content - Type': 'application / json;charset = UTF - 8'
    }
    jsondata = {"workloadKind": workloadKind, "appName": ""}
    pagenow = 1
    while True:
        res = requests.post(
            f"http://www.ctgpaas.cn:9000/dcos/workload/page/cluster/{clusterId}/namespace/{namespace}?pageNow={pagenow}&pageSize=10",
            headers=headers, json=jsondata).json()

        l += res['data']['records']
        if pagenow >= res['data']['pages']:
            break
        pagenow += 1
    return l


# 爬取工作负载中的pod列表
def pod_list_get(clusterId, namespace, workloadKind, workloadName):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    pod_list = requests.get(
        f"http://www.ctgpaas.cn:9000/dcos/workload/pods/?clusterId={clusterId}&namespaceName={namespace}&workloadName={workloadName}&workloadKind={workloadKind}",
        headers=headers).json()["data"]
    return pod_list


# 日志数据爬取
def diary_get(clusterId, namespace, pod_name, container_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    diary = requests.get(
        f"http://www.ctgpaas.cn:9000/dcos/workload/containerLogs?clusterId={clusterId}&namespaceName={namespace}&podName={pod_name}&tailingLines=1000&containerName={container_name}",
        headers=headers).json()["data"]
    return diary


# 爬取pod的三张图片数据
def pod_picture_get(clusterName, spacename, podname, now):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    list = []
    # podCPU使用率
    res1 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podCpuUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&startTime={now - 1200}&endTime={now}',
        headers=headers
    ).json()
    list.append(res1['data']['values'])
    # pod内存使用率
    res2 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podNetworkUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&startTime={now - 1200}&endTime={now}',
        headers=headers
    ).json()
    list.append(res2['data']['values'])
    # 网络流入流出速率
    res3 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podMemoryUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&startTime={now - 1200}&endTime={now}',
        headers=headers
    ).json()
    # print(res3['data']['values'])
    list.append(res3['data']['values'])
    for item in list:
        send_data(item, spacename, podname)
    return list


# 爬取容器图片的数据
def container_picture_get(clusterName, spacename, podname, container_name, now):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    list = []
    # containerCPU使用率
    res4 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/containerCpuUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&containerName={container_name}&startTime={now - 1200}&endTime={now}',
        headers=headers
    ).json()
    list.append(res4['data']['values'])
    res5 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/containerMemoryUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&containerName={container_name}&startTime={now - 1200}&endTime={now}',
        headers=headers
    ).json()
    # container内存使用率
    list.append(res5['data']['values'])
    return list


# 以文件形式保存爬取到的数据
def yilong_get():
    delete_data()
    now = time.time()
    now = int(now)
    print(f"爬取时间范围为{datetime.datetime.fromtimestamp(now)}前一个小时")
    if os.path.exists('data'):
        remove_folder('data')
    os.makedirs('data')
    for cluster in cluster_get():
        clusterId = cluster['id']
        clusterName = cluster['name']
        namespacelist = namespace_get(clusterId)
        print(namespacelist)
        # 遍历所有命名空间
        for namespace in namespacelist:
            space_name = namespace['namespaceName']
            print("正在爬取命名空间:" + space_name)
            if not os.path.exists(f'data/{space_name}'):
                os.makedirs(f'data/{space_name}')
            inf = inf_get(clusterId, space_name)['data']['resourceQuotaVO']
            inf = json.dumps(inf, ensure_ascii=True)
            with open(f'data/{space_name}/inf.json', 'w') as f:
                f.write(inf)
            print("-已爬取基本信息")
            kind_list = ["Deployment", "StatefulSet", "DaemonSet", "Job"]
            # 遍历四种工作负载
            for kind in kind_list:
                if not os.path.exists(f'data/{space_name}/{kind}'):
                    os.makedirs(f'data/{space_name}/{kind}')
                print("-正在爬取" + kind + "中的工作负载")
                workload_list = list_get(clusterId, space_name, kind)
                for workload in workload_list:
                    workload_name = workload["workloadName"]
                    print("--正在爬取工作负载:" + workload_name)
                    if not os.path.exists(f'data/{space_name}/{kind}/{workload_name}'):
                        os.makedirs(f'data/{space_name}/{kind}/{workload_name}')
                    pod_list = pod_list_get(clusterId, space_name, kind, workload_name)
                    # 遍历pod列表中的所有实例
                    for pod in pod_list:
                        pod_name = pod["podName"]
                        print("---正在爬取pod:" + pod_name)
                        if not os.path.exists(f'data/{space_name}/{kind}/{workload_name}/{pod_name}'):
                            os.makedirs(f'data/{space_name}/{kind}/{workload_name}/{pod_name}')
                        for container in pod['containerStatuses']:
                            container_name = container['name']
                            print("----正在爬取容器:" + container_name)
                            if not os.path.exists(
                                    f'data/{space_name}/{kind}/{workload_name}/{pod_name}/{container_name}'):
                                os.makedirs(f'data/{space_name}/{kind}/{workload_name}/{pod_name}/{container_name}')
                            pod_picture = pod_picture_get(clusterName, space_name, pod_name, now)
                            pod_picture = json.dumps(pod_picture)
                            with open(
                                    f'data/{space_name}/{kind}/{workload_name}/{pod_name}/canvas_data.json',
                                    'w') as f:
                                f.write(pod_picture)
                            print("-----pod监控已爬取")
                            diary = diary_get(clusterId, space_name, pod_name, container_name)
                            diary = json.dumps(diary)
                            with open(
                                    f'data/{space_name}/{kind}/{workload_name}/{pod_name}/{container_name}/diary.json',
                                    'w') as f:
                                f.write(diary)
                            print("-----日志已爬取")
                            canvas_data = container_picture_get(clusterName, space_name, pod_name, container_name, now)
                            canvas_data = json.dumps(canvas_data)
                            with open(
                                    f'data/{space_name}/{kind}/{workload_name}/{pod_name}/{container_name}/canvas_data.json',
                                    'w') as f:
                                f.write(canvas_data)
                            print("-----容器监控已爬取")


if __name__ == '__main__':
    # create_table()
    yilong_get()

