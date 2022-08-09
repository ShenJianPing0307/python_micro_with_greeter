import socket


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    _, port = tcp.getsockname()
    tcp.close()
    return port


# Consul info
CONSUL_HOST = '192.168.111.5'
CONSUL_PORT = 8500

# Server info
SERVICE_HOST = '192.168.0.118'
SERVICE_PORT = get_free_tcp_port() | 8008
SERVICE_NAME = "greeter_api"
SERVICE_TAGS = ["api"]

# Consul key
CONSUL_FILTER_KEY = 'Service'
CONSUL_FILTER_VALUE = 'greeter_srv'
