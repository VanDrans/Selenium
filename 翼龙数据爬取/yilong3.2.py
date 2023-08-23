# This Python file uses the following encoding: utf-8
# 提供接口
import json
import time
import requests
from flask import Flask, request, jsonify
import threading
app = Flask(__name__)
# 打开cookie.json读取cookie
with open('cookie.json', 'r') as f:
    json_cookies = f.read()
cookie_list = json.loads(json_cookies)
for cookie in cookie_list:
    # 复制cookie字典
    cookie_dict = cookie.copy()

#[{'tenantId': '2520010', 'tenantName': 'gdB1_plat', 'tenantType': 2, 'status': 1, 'parentId': None, 'children': []}, {'tenantId': '4120823', 'tenantName': 'gdB1_offices', 'tenantType': 2, 'status': 1, 'parentId': None, 'children': []}]
# 获取租户信息
def tenants_get():
    # 设置请求标头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }

    tenants_list = requests.get(
        "http://www.ctgpaas.cn:9000/cloudportal/iam/users/current",
        headers=headers)
    tenants_list = tenants_list.json()["tenants"]
    return tenants_list


# 切换租户
def tenants_change(id):
    # 设置请求标头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    tenants_list = requests.post(
        f"http://www.ctgpaas.cn:9000/cloudportal/iam/users/current/tenants/{id}",
        headers=headers)

# 确认资源地
def post_region():
    # 设置请求标头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }

    requests.post(
        "http://www.ctgpaas.cn:9000/gw/regions/choose?region=GD_B001&spuCode=dcos",
        headers=headers)


# 获取clusterID和clusterName
# {code: 0, data: [{id: 19, name: "dmz-fgs-ccse"}]}
def cluster_get():
    # 设置请求标头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }

    cluster_list = requests.get(
        "http://www.ctgpaas.cn:9000/dcos/cluster/csCluster/pulldownList",
        headers=headers).json()
    if cluster_list['code'] == -1:
        print("无内容")
        return []
    cluster_list = cluster_list['data']
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
def workload_list_get(clusterId, namespace, workloadKind):
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
        if res['code'] == 1102:
            print(res)
            return l
        l += res['data']['records']
        # 判断现在的页数和网页中总页数
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
        headers=headers).json()
    pod_list = pod_list["data"]
    return pod_list


# pod和container 里面的数据获取
def container_data_get(clusterName, namespace, workloadKind, workloadName):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    list = requests.get(
        f"http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podMonitor?clusterName={clusterName}&namespaceName={namespace}&workloadName={workloadName}&workloadKind={workloadKind}",
        headers=headers).json()["data"]
    return list


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
def pod_picture_get(clusterName, spacename, podname, start_time, end_time):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    list = []
    # podCPU使用率
    res1 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podCpuUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&startTime={start_time}&endTime={end_time}',
        headers=headers
    ).json()
    list.append(res1['data']['values'])
    # pod内存使用率
    res2 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podNetworkUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&startTime={start_time}&endTime={end_time}',
        headers=headers
    ).json()
    list.append(res2['data']['values'])
    # 网络流入流出速率
    res3 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/podMemoryUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&startTime={start_time}&endTime={end_time}',
        headers=headers
    ).json()
    # print(res3['data']['values'])
    list.append(res3['data']['values'])
    return list


# 爬取容器图片的数据
def container_picture_get(clusterName, spacename, podname, container_name, start_time, end_time):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': f"SESSION={cookie_dict['value']}",
    }
    list = []
    # containerCPU使用率
    res4 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/containerCpuUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&containerName={container_name}&startTime={start_time}&endTime={end_time}',
        headers=headers
    ).json()
    list.append(res4['data']['values'])
    res5 = requests.get(
        f'http://www.ctgpaas.cn:9000/dcos/workloadMonitor/containerMemoryUsage?clusterName={clusterName}&namespaceName={spacename}&podName={podname}&containerName={container_name}&startTime={start_time}&endTime={end_time}',
        headers=headers
    ).json()
    # container内存使用率
    list.append(res5['data']['values'])
    return list


# 根据命名空间确定租户
def determine_tenants_based_on_namespaces(namespaceName):
    tenants_list = tenants_get()
    for tenants in tenants_list:
        tenants_change(tenants['tenantId'])
        cluster_list = cluster_get()
        for cluster in cluster_list:
            # 根据id获取此id下的所有命名空间
            namespace_list = namespace_get(cluster['id'])
            for namespace in namespace_list:
                if namespace['namespaceName'] == namespaceName:
                    print(tenants['tenantId'])
                    return


# 发送命名空间列表
@app.route('/namespace', methods=['GET'])
def send_namespace_list():
    list = []
    tenants_list = tenants_get()
    for tenants in tenants_list:
        tenants_change(tenants['tenantId'])
        cluster_list = cluster_get()
        for cluster in cluster_list:
            # 根据id获取此id下的所有命名空间
            namespace_list = namespace_get(cluster['id'])

            list.extend(namespace_list)
    return list


# 基本信息
@app.route('/inf', methods=['GET'])
def send_inf():
    # 接受参数
    clusterID = request.args.get('clusterId')
    spacename = request.args.get('namespaceName')
    determine_tenants_based_on_namespaces(spacename)
    # 根据给出的参数获取信息
    inf = inf_get(clusterID, spacename)
    return inf


# 获取工作负载列表
@app.route('/workload', methods=['GET'])
def send_workload_list():
    clusterId = request.args.get('clusterId')
    spacename = request.args.get('namespaceName')
    workkind = request.args.get('workKind')
    determine_tenants_based_on_namespaces(spacename)
    data = workload_list_get(clusterId, spacename, workkind)
    list = []
    for workload in data:
        dict = {}
        dict['workloadName']=workload['workloadName']
        dict['runningPodNum'] = workload['runningPodNum']
        dict['replicas']  = workload['replicas']
        dict['createdTime'] = workload['createdTime']
        list.append(dict)
    return jsonify(list)


# 发送pod列表
@app.route('/pod', methods=['GET'])
def send_pod_list():
    clusterId = request.args.get('clusterId')
    spacename = request.args.get('namespaceName')
    workkind = request.args.get('workKind')
    workload = request.args.get('workloadName')
    determine_tenants_based_on_namespaces(spacename)
    pod_list = []
    data = pod_list_get(clusterId, spacename, workkind, workload)
    print(data)
    for item in data:
        dict1 = {'podName': item['podName'], 'hostIp': item['hostIp'], 'podIp': item['podIp'],
                 'podPhase': item['podPhase'], 'podRunTime': item['podRunTime']}
        pod_list.append(dict1)
    return jsonify(pod_list)


# 发送container列表
@app.route('/container', methods=['GET'])
def send_container_list():
    clusterName = request.args.get('clusterName')
    spacename = request.args.get('namespaceName')
    workkind = request.args.get('workKind')
    workloadName = request.args.get('workloadName')
    data = container_data_get(clusterName, spacename, workkind, workloadName)
    return jsonify(data)


# 发送pod图表数据
@app.route('/podpicture', methods=['GET'])
def send_pod_picture():
    now = time.time()
    now = int(now)
    clusterName = request.args.get('clusterName')
    spacename = request.args.get('namespaceName')
    podname = request.args.get('podName')
    determine_tenants_based_on_namespaces(spacename)
    start_time = now - 3000
    end_time = now
    data = pod_picture_get(clusterName, spacename, podname, start_time, end_time)
    return jsonify(data)


# 发送container图表数据
@app.route('/containerpicture', methods=['GET'])
def send_container_picture():
    clusterName = request.args.get('clusterName')
    spacename = request.args.get('namespaceName')
    podname = request.args.get('podName')
    containername = request.args.get('containerName')
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')
    data = container_picture_get(clusterName, spacename, podname, containername, start_time, end_time)
    return jsonify(data)


# 启动服务器
if __name__ == '__main__':
    post_region()
    # 定义一个任务函数
    def task1(name):
        app.run(host='0.0.0.0', port=5000)
    def task2(name):
        while True:
            print(cluster_get())
            time.sleep(30)
    # 创建线程对象并启动线程
    thread1 = threading.Thread(target=task1, args=("Thread 1",))
    thread2 = threading.Thread(target=task2, args=("Thread 2",))

    thread1.start()
    thread2.start()
