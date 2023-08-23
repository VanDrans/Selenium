# This Python file uses the following encoding: utf-8
import json
import time
from datetime import datetime

import MySQLdb

import datetime
import requests

conn = MySQLdb.connect(host='localhost', user='root', password='fzs123456', db='test')


def send_data(data_list, pod_name):
    # 创建游标
    cursor = conn.cursor()
    if not data_list is None:
        for item in data_list:
            print(item)
            # 执行 INSERT 语句
            cursor.execute(
                "INSERT INTO canvas (`id`, `time`, `value`, `name`,`pod_name`) VALUES (NULL, %s, %s, %s, %s)",
                (item['time'], item['value'], item['name'], pod_name))
            # 提交事务
            conn.commit()


def delete_data():
    # 创建游标
    cursor = conn.cursor()

    # 执行 INSERT 语句
    cursor.execute("TRUNCATE TABLE canvas")
    # 提交事务
    conn.commit()


# 使用json读取cookies
with open('cookie.json', 'r') as f:
    json_cookies = f.read()
cookie_list = json.loads(json_cookies)
for cookie in cookie_list:
    # 复制cookie字典
    cookie_dict = cookie.copy()


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


# 爬取图片的数据
def picture_get(clusterName, spacename, podname, now):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }

    res1 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podCpuUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&startTime={now - 3600}&endTime={now}',
        headers=headers
    ).json()
    list1 = res1['data']['values']
    send_data(list1, podname)
    res2 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podNetworkUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&startTime={now - 3600}&endTime={now}',
        headers=headers
    ).json()
    list2 = res2['data']['values']
    send_data(list2, podname)
    res3 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podMemoryUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&startTime={now - 3600}&endTime={now}',
        headers=headers
    ).json()
    list3 = res3['data']['values']
    send_data(list3, podname)


# 保存在数据库中
def yilong_get_MySQL():
    delete_data()
    now = time.time()
    now = int(now)
    print(now)
    print(f"爬取时间范围为{datetime.datetime.fromtimestamp(now)}前一个小时")
    for cluster in cluster_get():
        clusterId = cluster['id']
        clusterName = cluster['name']
        # 遍历所有命名空间
        for namespace in namespace_get(clusterId):
            space_name = namespace['namespaceName']
            print("正在爬取命名空间:" + space_name)
            kind_list = ["Deployment", "StatefulSet", "DaemonSet", "Job"]
            # 遍历四种工作负载
            for kind in kind_list:
                print("-正在爬取" + kind + "中的工作负载")
                workload_list = list_get(clusterId, space_name, kind)
                for workload in workload_list:
                    workload_name = workload["workloadName"]
                    print("--正在爬取工作负载:" + workload_name)
                    pod_list = pod_list_get(clusterId, space_name, kind, workload_name)
                    # 遍历pod列表中的所有实例
                    for pod in pod_list:
                        pod_name = pod["podName"]
                        print("---正在爬取pod:" + pod_name)
                        picture_get(clusterName, space_name, pod_name, now)
# 上传到Prometheus
def yilong_get_prometheus():
    now = time.time()
    now = int(now)
    print(f"爬取时间范围为{datetime.datetime.fromtimestamp(now)}前一个小时")
    for cluster in cluster_get():
        clusterId = cluster['id']
        clusterName = cluster['name']
        # 遍历所有命名空间
        for namespace in namespace_get(clusterId):
            space_name = namespace['namespaceName']
            print("正在爬取命名空间:" + space_name)
            inf = inf_get(clusterId, space_name)['data']['resourceQuotaVO']
            inf_send(space_name, inf)
            print("-已爬取基本信息")
            # kind_list = ["Deployment", "StatefulSet", "DaemonSet", "Job"]
            # # 遍历四种工作负载
            # for kind in kind_list:
            #     if not os.path.exists(f'{space_name}/{kind}'):
            #         os.makedirs(f'{space_name}/{kind}')
            #     print("-正在爬取" + kind + "中的工作负载")
            #     workload_list = list_get(clusterId, space_name, kind)
            #     for workload in workload_list:
            #         workload_name = workload["workloadName"]
            #         print("--正在爬取工作负载:" + workload_name)
            #         if not os.path.exists(f'{space_name}/{kind}/{workload_name}'):
            #             os.makedirs(f'{space_name}/{kind}/{workload_name}')
            #         pod_list = pod_list_get(clusterId, space_name, kind, workload_name)
            #         # 遍历pod列表中的所有实例
            #         for pod in pod_list:
            #             pod_name = pod["podName"]
            #             print("---正在爬取pod:" + pod_name)
            #             if not os.path.exists(f'{space_name}/{kind}/{workload_name}/{pod_name}'):
            #                 os.makedirs(f'{space_name}/{kind}/{workload_name}/{pod_name}')
            #             for container in pod['containerStatuses']:
            #                 container_name = container['name']
            #                 print("----正在爬取容器:" + container_name)
            #                 if not os.path.exists(
            #                         f'{space_name}/{kind}/{workload_name}/{pod_name}/{container_name}'):
            #                     os.makedirs(f'{space_name}/{kind}/{workload_name}/{pod_name}/{container_name}')
            #                 diary = diary_get(clusterId, space_name, pod_name, container_name)
            #                 diary = json.dumps(diary, ensure_ascii=False)
            #                 with open(f'{space_name}/{kind}/{workload_name}/{pod_name}/{container_name}/diary.json',
            #                           'w') as f:
            #                     f.write(diary)
            #                 print("-----日志已爬取")
            #                 canvas_data = picture_get(clusterName, space_name, pod_name, container_name, now)
            #                 canvas_data = json.dumps(canvas_data, ensure_ascii=False)
            #                 with open(
            #                         f'{space_name}/{kind}/{workload_name}/{pod_name}/{container_name}/canvas_data.json',
            #                         'w') as f:
            #                     f.write(canvas_data)
            #                 print("-----监控已爬取")



yilong_get_MySQL()
conn.close()
