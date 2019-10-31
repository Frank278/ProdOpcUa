#!bin/python
# -*- encoding: utf-8 -*-
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

class OcpuaClient(Client):
    """Neuen Client anlegen

    Arguments:

    """
    logging.basicConfig(level=logging.WARN)

    def create_client(self, name, port):

        pass


    def start_demoprogramm(self, name):
        pass



