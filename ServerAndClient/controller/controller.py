#!bin/python
# -*- encoding: utf-8 -*-

import docker
import os
import time

client = docker.from_env()

class DockerHandler(object):
    """Neue Server anlegen
    
    Arguments:
        object {[type]} -- [description]
    """

    registry = {}
    client = None
    home_dir = '%s/server' % os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

    def __init__(self):
        self.client = docker.from_env()
        # check if home_dir is ok
        server_py = '%s/server2.py' % self.home_dir
        if not os.path.exists(server_py):
            raise ValueError('%s does not exists' % server_py)
        self._refresh_registry()
        # make sure the db container is up and running
        # docker run -d -e POSTGRES_USER=frank -e POSTGRES_PASSWORD=frank -e POSTGRES_DB=postgres --name dbserver -p 55432:5432 postgres
        if not self.registry.get('dbserver'):
            # not running, check if it exists
            dbserver = self.client.containers.list(all=True, filters={'name' : 'dbserver'})
            if dbserver:
                # container is stopped
                dbserver[0].restart()
            else:
                ports_dic = {
                    '5432' : 55432
                }
                dbserver = client.containers.run(
                    'postgres',
                    name = 'dbserver',
                    auto_remove = False,
                    detach = True,
                    ports = ports_dic,
                )
                self.registry['dbserver'] = dbserver
                    
    def _refresh_registry(self):
        self.registry = {}
        for container in self.client.containers.list():
            name = container.name
            self.registry[name] = container
        
    def create_server(self, name, port):
        """
           docker run --name rottis_server \
            -v /home/robert/erp-workbench/helpers/opcua/server:/app \
            --link dbserver:dbserver -p 40840:40840 opcua_server
        """
        if not self.registry.get(name):
            links_dic = {
                'dbserver' : 'dbserver'
            }
            volumes_dic = {
                self.home_dir : 
                    {'bind': '/app', 'mode': 'ro'}
            }
            ports_dic = {
                '40840' : port
            }
            result = client.containers.run(
                'opcua_server',
                name = name,
                auto_remove = True,
                detach = True,
                links = links_dic,
                volumes = volumes_dic,
                ports = ports_dic,
            )
            self.registry[name] = result
            return result.short_id

    def remove_server(self, name):
        """
        remove a server from the database
        and delete the container
        """
        container = self.registry.get(name)
        if container:
            # signal 15 informs the dbhandler within
            # the container to remove itself from
            # the database
            # and then exit
            container.kill(signal = 15)
            # now refresh the registry
            # name should not exist anymore
            time.sleep(1)
            self._refresh_registry()
            if self.registry.get(name):
                raise ValueError('Hoppala, should not happen')

    def list_servers(self, filter=[]):
        """list existing containers
        
        Keyword Arguments:
            filter {list} -- list of filter arguments (default: {[]})
        """
        print(self.registry.keys())


if __name__ == "__main__":
    handler = DockerHandler()
    s_id = handler.create_server('hugo', 40845)
    handler.list_servers()
    handler.remove_server('hugo')
    

