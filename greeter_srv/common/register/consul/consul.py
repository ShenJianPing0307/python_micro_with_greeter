from common.register.consul.base import Register

import consul
import requests
import random


class ConsulRegister(Register):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.c = consul.Consul(host=host, port=port)

    def register(self, name, id, address, port, tags, check):

        if check is None:
            check = {
                "GRPC": f"{address}:{port}",
                "GRPCUseTLS": False,
                "Timeout": "5s",
                "Interval": "5s",
                "DeregisterCriticalServiceAfter": "5s"
            }
        else:
            check = check
        return self.c.agent.service.register(
            name=name,
            service_id=id,
            address=address,
            port=port,
            tags=tags,
            check=check,
        )

    def deregister(self, service_id):
        return self.c.agent.service.deregister(service_id)

    def get_all_service(self):
        return self.c.agent.services()

    def filter_service(self, filter):
        url = f"http://{self.host}:{self.port}/v1/agent/services"
        params = {
            "filter": filter
        }
        return requests.get(url, params=params).json()

    def get_host_port(self, filter):
        url = f"http://{self.host}:{self.port}/v1/agent/services"
        params = {
            "filter": filter
        }
        data = requests.get(url, params=params).json()
        if data:
            service_info = random.choice(list(data.values()))
            return service_info["Address"], service_info["Port"]
        return None, None
