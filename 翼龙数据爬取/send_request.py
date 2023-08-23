# This Python file uses the following encoding: utf-8
import requests
import time

# http://10.18.125.208:31071/
# http://127.0.0.1:5000/

url = 'http://127.0.0.1:5000/'


# 返回所有的命名空间
def get_namespace_list():
    namespace_list = requests.get(f'{url}namespace?').json()

    return namespace_list


# # 返回命名空间的基本信息
# def get_inf(clusterId,namespaceName):
#     inf = requests.get(f'{url}inf?clusterId={clusterId}&namespaceName={namespaceName}').json()
#     return inf


# 返回namespaceName, workkind下的所有工作负载
def get_workload_list(clusterId, namespaceName, workkind):
    workload_list = requests.get(
        f'{url}workload?clusterId={clusterId}&namespaceName={namespaceName}&workKind={workkind}').json()
    return workload_list


# 获取pod对应的三张图表
def get_pod_picture(clusterName, namespaceName, podName):
    picture = requests.get(
        f'{url}podpicture?clusterName={clusterName}&namespaceName={namespaceName}&podName={podName}').json()
    return picture


# def get_container_picture(clusterName,namespaceName, podName, container_name, startTime, end_time):
#     picture = requests.get(
#         f'{url}containerpicture?clusterName={clusterName}&namespaceName={namespaceName}&podName={podName}&containerName={container_name}&startTime={startTime}&endTime={end_time}').json()
#     return picture


# 获取工作负载下的pod列表和pod下的container
def get_pod(clusterId, namespaceName, workkind, workload):
    pod_list = requests.get(
        f'{url}pod?clusterId={clusterId}&namespaceName={namespaceName}&workKind={workkind}&workloadName={workload}').json()
    # list = []
    # for item in pod_list:
    #     contrainer_list = []
    #     for container in item["containers"]:
    #         contrainer_list.append(container['name'])
    #     dict = {item['podName']:contrainer_list}
    #     list.append(dict)
    return pod_list


#
# # 获取pod和container列表及数据
# def get_container(clusterName,namespaceName, workkind, workloadName):
#     list = requests.get(
#         f'{url}container?clusterName={clusterName}&namespaceName={namespaceName}&workKind={workkind}&workloadName={workloadName}').json()
#     return list


if __name__ == '__main__':
    now = time.time()
    now = int(now)
    print(now - 3600, now)
    print(get_namespace_list())
    print(get_workload_list('32', 'gzqw', 'Deployment'))
    # print(get_pod('19', 'gzqw', 'Deployment', 'gz-mysftp'))
    # print(get_pod_picture('dmz-fgs-ccse', 'gzqw', 'gz-mysftp-664b9cf66d-4l7hg'))
