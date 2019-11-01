#!bin/python
# -*- encoding: utf-8 -*-
import threading

import docker
import os
import time
import sys
sys.path.insert(0, "..")
import logging
import time


from opcua import Client
from opcua import ua
#from ServerAndClient.client import client

class OcpuaClient(threading.Thread):
    """Neuen Client anlegen, ruft UA Methoden auf Server ausserhalb der Dockerumgebung an
    Eventuell braucht es Threading um mehrere Clients zu starten, zumindest wenn Sie auf den gleichen Port zugreifen
    """

    def __init__(self):
        logging.basicConfig(level=logging.WARN)

    # Einen Client Erzeugen und verbinden
    def create_client(self, servername, urlname, port):
        clientname = servername + "Client"
        clientnamename = Client("opc.tcp://"+urlname+":"+port+"/freeopcua/server/")
        clientname.load_type_definitions()  # load definition of server specific structures/extension objects
        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = clientname.get_root_node()
        print("Root node is: ", root)
        objects = clientname.get_objects_node()
        print("Objects node is: ", objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())

        # gettting our namespace idx
        uri = "http://examples.freeopcua.github.io"
        idx = clientname.get_namespace_index(uri)
        obj = root.get_child(["0:Objects", "{}:MyObject".format(idx)])
        res = obj.start_demoprogramm()




    def start_demoprogramm(self, clientname):
        res = clientname.obj.start_demoprogramm()
        pass



