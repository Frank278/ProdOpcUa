#!bin/python
# -*- encoding: utf-8 -*-

import docker
client = docker.from_env()
print(client.containers.list())



class DockerHandler(object):
    """Neue Server anlegen
    
    Arguments:
        object {[type]} -- [description]
    """
    registry = {}
    client = None
    def __init__(self):
        self.client = docker.from_env()
        for container in self.client.containers.list():
            name = container.name
            print(name)
            self.registry[name] = container
    
    def create_server(self, name, port):
        if not self.registry.get(name):
            self.registry[name] = 77
    
    def remove_server(self, name):
        if not self.registry.get(name):
            self.registry[name] = 77
    
    def list_servers(self, filter = []):
        """list existing containers
        
        Keyword Arguments:
            filter {list} -- list of filter arguments (default: {[]})
        """
        print(self.registry.keys())



if __name__ == '__main__':
    handler = DockerHandler()
