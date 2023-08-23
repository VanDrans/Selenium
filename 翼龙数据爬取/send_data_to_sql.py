# This Python file uses the following encoding: utf-8
import MySQLdb  # 连接数据库

conn = MySQLdb.connect(host='localhost', user='root', password='fzs123456', db='test')


def send_data(data_list, pod_name):
    # 创建游标
    cursor = conn.cursor()

    for item in data_list:
        print(item)
        # 执行 INSERT 语句
        cursor.execute("INSERT INTO canvas (`id`, `time`, `value`, `name`,`pod_name`) VALUES (NULL, %s, %s, %s, %s)",
                       (item['time'], item['value'], item['name'], pod_name))
        # 提交事务
        conn.commit()



def delete_data():
    conn = MySQLdb.connect(host='localhost', user='root', password='fzs123456', db='test')

    # 创建游标
    cursor = conn.cursor()

    # 执行 INSERT 语句
    cursor.execute("TRUNCATE TABLE canvas")
    # 提交事务
    conn.commit()


if __name__ == '__main__':
    delete_data()
    data = [
        {
            "time": 1691051607000,
            "value": 0.81,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691051667000,
            "value": 1.89,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691051727000,
            "value": 1.86,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691051787000,
            "value": 1.85,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691051847000,
            "value": 1.59,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691051907000,
            "value": 1.86,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691051967000,
            "value": 1.89,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052027000,
            "value": 1.29,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052087000,
            "value": 1.86,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052147000,
            "value": 1.89,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052207000,
            "value": 1.89,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052267000,
            "value": 1.94,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052327000,
            "value": 1.92,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052387000,
            "value": 1.61,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052447000,
            "value": 1.64,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052507000,
            "value": 1.85,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052567000,
            "value": 1.47,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052627000,
            "value": 1.86,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052687000,
            "value": 1.9,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052747000,
            "value": 1.59,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052807000,
            "value": 1.92,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052867000,
            "value": 1.94,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052927000,
            "value": 1.67,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691052987000,
            "value": 1.66,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053047000,
            "value": 1.33,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053107000,
            "value": 1.87,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053167000,
            "value": 1.9,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053227000,
            "value": 1.84,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053287000,
            "value": 1.85,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053347000,
            "value": 1.85,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053407000,
            "value": 1.88,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053467000,
            "value": 1.62,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053527000,
            "value": 1.66,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053587000,
            "value": 1.36,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053647000,
            "value": 1.4,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053707000,
            "value": 1.83,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053767000,
            "value": 1.85,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053827000,
            "value": 1.89,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053887000,
            "value": 1.88,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691053947000,
            "value": 1.31,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054007000,
            "value": 1.87,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054067000,
            "value": 1.9,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054127000,
            "value": 1.64,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054187000,
            "value": 1.84,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054247000,
            "value": 1.87,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054307000,
            "value": 1.86,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054367000,
            "value": 1.92,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054427000,
            "value": 1.89,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054487000,
            "value": 2.87,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054547000,
            "value": 3.43,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054607000,
            "value": 1.97,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054667000,
            "value": 2.37,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054727000,
            "value": 2.3,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054787000,
            "value": 2.22,
            "name": "cpu_use_rate"
        },
        {
            "time": 1691054847000,
            "value": 2.22,
            "name": "cpu_use_rate"
        }
    ]
    send_data(data, "a")
