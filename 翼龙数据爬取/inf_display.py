from prometheus_client import Gauge, start_http_server, CollectorRegistry, push_to_gateway

# 创建Gauge指标，使用'filename'标签来区分不同文件的数据
cpu_request_total = Gauge('cpu_request_total', 'CPU的Request总和', ['space_name'])
cpu_limit_total = Gauge('cpu_limit_total', 'CPU的Limit总和', ['space_name'])
memory_request_total = Gauge('memory_request_total', '内存的Request总和', ['space_name'])
memory_limit_total = Gauge('memory_limit_total', '内存的Limit总和', ['space_name'])
pod_number_total = Gauge('pod_number_total', 'Pod数', ['space_name'])
cpu_request_used = Gauge('cpu_request_used', 'CPU Request Used', ['space_name'])
cpu_limit_used = Gauge('cpu_limit_used', 'CPU Limit Used', ['space_name'])
memory_request_used = Gauge('memory_request_used', 'Memory Request Used', ['space_name'])
memory_limit_used = Gauge('memory_limit_used', 'Memory Limit Used', ['space_name'])
pod_number_used = Gauge('pod_number_used', 'pod Used', ['space_name'])


# 处理可能为空的字段
def inf_send(space_name, data):
    fields = [
        ('cpuRequestTotal', cpu_request_total),
        ('cpuLimitTotal', cpu_limit_total),
        ('memoryRequestTotal', memory_request_total),
        ('memoryLimitTotal', memory_limit_total),
        ('podsNumTotal', pod_number_total),
        ('cpuRequestUsed', cpu_request_used),
        ('cpuLimitUsed', cpu_limit_used),
        ('memoryRequestUsed', memory_request_used),
        ('memoryLimitUsed', memory_limit_used),
        ('podsNumUsed', pod_number_used)
    ]

    for field_name, gauge in fields:
        field_value = data.get(field_name, None)
        if field_value is None:
            field_value = float('nan')

        # 将数据上传到Prometheus
        gauge.labels(space_name=space_name).set(field_value)
    # 将指标数据推送到Prometheus服务器
    push_to_gateway('132.97.54.148:8000', job='testPro')
