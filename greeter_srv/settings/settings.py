import socket


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port


# consul配置
CONSUL_HOST = "192.168.111.5"
CONSUL_PORT = 8500

# service配置
SERVICE_NAME = "greeter_srv"
SERVICE_TAGS = ["srv"]

# server配置
ADDRESS_IP = "192.168.0.118"
ADDRESS_PORT = get_free_tcp_port() | 50051
