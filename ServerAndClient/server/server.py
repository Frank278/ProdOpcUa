import os.path
import time
import sys
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from opcua import ua, uamethod, Server

# während dem entwickeln, ist die Umgebung ev. nicht gesetzt
try:
    from uamethods.uamethods import *
except ImportError:

    @uamethod
    def dummy(*args, **kwargs):
        pass

    start_programm = dummy
    stop_program = dummy
    get_status = dummy
    init_server = dummy

# sqlalchemy erwarted bereits eine datenbank
# lege datenbank an
# wenn sie schon vorhanden ist, ignoriere entsprechenden Fehler
con = psycopg2.connect(  #'postgres://frank:frank@localhost:55432'
    dbname="postgres", user="frank", host="dbserver", password="frank"
)  # ,
# port='55432')
con.autocommit = True

cur = con.cursor()
try:
    cur.execute("CREATE DATABASE {};".format("opcua"))
except Exception as e:
    pass  # exists already
finally:
    con.close()

# sql alchemy
db_string = "postgres://frank:frank@dbserver:55432/opcua"
db = create_engine(db_string)
base = declarative_base()


class Bearbeitungszentrum:
    def __init__(self, endpoint, name, model_filepath):
        self.server = Server()

        #  This need to be imported at the start or else it will overwrite the data
        self.server.import_xml(model_filepath)

        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)

        objects = self.server.get_objects_node()

        freeopcua_namespace = self.server.get_namespace_index(
            "urn:freeopcua:python:server"
        )
        baseserver = objects.get_child("0:BaseServer")
        baseserver_init = baseserver.get_child("0:InitServer")

        self.server.link_method(baseserver_init, init_server)

        baseserver.add_method(
            freeopcua_namespace,
            "StartProgram",
            start_programm,
            [ua.VariantType.Boolean],
            [ua.VariantType.String],
            [ua.VariantType.String],
        )

        baseserver.add_method(
            freeopcua_namespace,
            "StopProgram",
            stop_program,
            [ua.VariantType.Boolean],
            [ua.VariantType.String],
        )

        baseserver.add_method(freeopcua_namespace, "GetStatus", get_status)

    def __enter__(self):
        self.server.start()
        return self.server

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.stop()


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    with Bearbeitungszentrum(
        "opc.tcp://0.0.0.0:40840/freeopcua/server/",
        "FreeOpcUa Example Server",
        os.path.join(script_dir, "test_saying.xml"),
    ) as server:
        print("*" * 80)
        print("Wir sind gestartet")
        print("*" * 80)
        while True:
            print(".")
            sys.stdout.flush()
            time.sleep(10)
