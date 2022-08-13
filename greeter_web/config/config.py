import socket
import nacos
import json


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port


NACOS = {
    "Host": "192.168.111.5",
    "Port": 8848,
    "NameSpace": "0a6d3e81-e929-4afe-9771-0eb4dbcda6ef",
    "User": "nacos",
    "Password": "nacos",
    "DataId": "greeter_web",
    "Group": "dev"
}
client = nacos.NacosClient(f'{NACOS["Host"]}:{NACOS["Port"]}', namespace=NACOS["NameSpace"],
                           username=NACOS["User"],
                           password=NACOS["Password"])

# client取出的数据是json字符串
config_data = client.get_config(NACOS["DataId"], NACOS["Group"])
config_data = json.loads(config_data)
"""
nacos中配置的json数据格式：
{
    "CONSUL_HOST":"192.168.111.5",
    "CONSUL_PORT":8500,
    "SERVICE_HOST":"192.168.0.118",
    "SERVICE_PORT":8008,
    "SERVICE_NAME":"greeter_api",
    "SERVICE_TAGS":["api"],
    "CONSUL_FILTER_KEY":"Service",
    "CONSUL_FILTER_VALUE":"greeter_srv"
}
"""

# Consul info
CONSUL_HOST = config_data['CONSUL_HOST']
CONSUL_PORT = int(config_data['CONSUL_PORT'])

# Server info
SERVICE_HOST = config_data['SERVICE_HOST']
SERVICE_PORT = get_free_tcp_port() | int(config_data['SERVICE_PORT'])
SERVICE_NAME = config_data['SERVICE_NAME']
SERVICE_TAGS = config_data['SERVICE_TAGS']

# Consul key
CONSUL_FILTER_KEY = config_data['CONSUL_FILTER_KEY']
CONSUL_FILTER_VALUE = config_data['CONSUL_FILTER_VALUE']
