#!bin/python
# -*- encoding: utf-8 -*-

import docker
import os
import sys
sys.path.insert(0, "..")
import logging
import time
from opcua import Client
from opcua import ua

# Um mit dem Docker-Daemon zu kommunizieren, müssen Sie zuerst einen Client instanziieren.
# Am einfachsten geht das, indem Sie die Funktion from_env () aufrufen.
# Es kann auch manuell konfiguriert werden, indem eine DockerClient-Klasse instanziiert wird.
client = docker.from_env()

class DockerHandler(object):
    """Neuen Server anlegen
    
    Arguments:
        object {[type]} -- [description]
    """

    registry = {}
    client = None
    #Suche nach dem Verzeichnis Server und den benötigten Dateien
    home_dir = '%s/server' % os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    home_dir = os.environ.get('BASE_PATH')

    def __init__(self):
        # Ein weiterer Client auf dem Self Objekt
        self.client = docker.from_env()
        # check if home_dir is ok and look for server2.py
        server_py = '%s/ServerAndClient/server/server2.py' % self.home_dir
        # if not os.path.exists(server_py):
        #     raise ValueError('%s does not exists' % server_py)
        self._refresh_registry()
        print(self.registry)


    # Aktualisiert die Registry
    def _refresh_registry(self, all=False):
        self.registry = {}
        for container in self.client.containers.list(all=all):
            name = container.name
            self.registry[name] = container
    # Erstellung der ausgewählten Server
    def create_server(self, name, port):
        """
           docker run --name frank_server \
            --link dbserver:dbserver -p 40840:40840 opcua_server
        """
        self._refresh_registry(all=True)
        container = self.registry.get(name)
        # Falls der Container noch nicht existiert, wird ein neuer erstellt
        if not container:
            links_dic = {
                'productionopcua_dbserver_1' : 'dbserver'
            }
            volumes_dic = {
                '%s/ServerAndClient/server' % self.home_dir :
                    {'bind': '/app', 'mode': 'ro'}
            }
            ports_dic = {
                '40840' : port
            }
            env_dic = {
                'CONTAINERNAME': name,
            }
            result = client.containers.run(
                'opcua_server',
                name = name,
                auto_remove = False,
                detach = True,
                links = links_dic,
                volumes = volumes_dic,
                ports = ports_dic,
                network = 'productionopcua_default',
                environment = env_dic,
            )
            self.registry[name] = result
            print(result.status)
            print(self.registry)
            return result.short_id
        else:
            # check if the container is running
            # if not , then start container
            if container.status !='running':
                container.start()

        # Erstellung der ausgewählten Server

    def create_client(self, name, port):
        """
            wenn der Server nicht Virtuell ist, kann ein Client im Docker erzeugt um Verbindung zum Server auzubauen.
            Die Unterscheidung ob Virtuell oder Real wird im GUI abgefangen.
        """
        clientname = name+"client"
        self._refresh_registry(all=True)
        container = self.registry.get(clientname)
        # Falls der Container noch nicht existiert, wird ein neuer erstellt
        if not container:
            volumes_dic = {
                '%s/ServerAndClient/client' % self.home_dir:
                    {'bind': '/app', 'mode': 'ro'}
            }
            ports_dic = {
                '40840': port
            }
            env_dic = {
                'CONTAINERNAME': clientname,
            }
            result = client.containers.run(
                'opcua_client',
                name=clientname,
                auto_remove=False,
                detach=True,
                volumes=volumes_dic,
                ports=ports_dic,
                network='prodopcua_default',
                environment=env_dic,
            )
            self.registry[name] = result
            print(result.status)
            print(self.registry)
            return result.short_id
        else:
            # check if the container is running
            # if not , then start container
            if container.status != 'running':
                container.start()

    # Fährt die ausgewählten Server herunter
    def remove_server(self, name, counter=0):
        """
        remove a server from the database
        and delete the container
        """
        self._refresh_registry()
        container = self.registry.get(name)
        if container:
            print(name+"ist abgemeldet")
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
                if counter < 4:
                    time.sleep(1)
                    counter += 1
                    self.remove_server(name, counter)
                else:
                    raise ValueError('Hoppala, should not happen')

    # sendet ein Signal an die Server
    def signal_server(self, name):
        """
        remove a server from the database
        and delete the container
        """
        self._refresh_registry()
        container = self.registry.get(name)
        if container:
            # signal 14 informs the dbhandler within
            # the container to change its status
            container.kill(signal = 14)



    # gibt eine Liste der erstellten Server aus
    def list_servers(self, filter=[]):
        """list existing containers
        
        Keyword Arguments:
            filter {list} -- list of filter arguments (default: {[]})
        """
        print(self.registry.keys())



    # sendet ein Signal an die Server
    def start_uaprogramm(self, name, serverurl, port, uamethod= "start_demoprogramm"):

        """
        ruft die UA Methode über den im Docker erzeugten Client auf

        """

        # Suche, ob der Container existiert
        clientname = name+"client"
        self._refresh_registry()
        container = self.registry.get(clientname)
        if container:

            connectstring = "opc.tcp://"+serverurl+":"+port+"/freeopcua/server/"
            client = Client(connectstring)
            # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/")
            try:
                client.connect()
                client.load_type_definitions()


                # # Der Client verfügt über einige Methoden, um einen Proxy für UA-Knoten abzurufen,
                # die sich immer im Adressraum befinden sollten, z. B. Root oder Objects
                root = client.get_root_node()
                print("Root node is: ", root)
                objects = client.get_objects_node()
                print("Objects node is: ", objects)

                # Knotenobjekte verfügen über Methoden zum Lesen und Schreiben von Knotenattributen sowie zum Duchsuchen
                # des Adressraums
                print("Children of root are: ", root.get_children())



                # Der Adressraum  idx
                uri = "http://freeopcua.github.io"
                idx = client.get_namespace_index(uri)

                # Jetzt wird ein variabler Knoten über den Suchpfad abgerufen
                myvar = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:MyVariable".format(idx)])

                obj = root.get_child(["0:Objects", "{}:MyObject".format(idx)])
                # Aufrufen unserer übergebenen Methode
                res = obj.call_method(uamethod.format(idx))
            finally:
                client.disconnect()


if __name__ == "__main__":
    handler = DockerHandler()
    s_id = handler.create_server('hugo', 40845)
    handler.list_servers()
    handler.remove_server('hugo')
    

