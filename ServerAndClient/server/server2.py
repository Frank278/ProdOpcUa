from threading import Thread
import copy
import logging
from datetime import datetime
import time
from math import sin
import sys
import signal
import os
import time
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import psycopg2
import psutil

sys.path.insert(0, "..")

from opcua import ua, uamethod, Server

# --------------------------------------------------
# relevante Umgebungsvariablen lesen
# --------------------------------------------------
db_host = os.environ.get("db_host", "localhost")
db_user = os.environ.get("db_user", "frank")
db_pasword = os.environ.get("db_pasword", "frank")
db_port = os.environ.get("db_port", 5432)
opcua_host = os.environ.get("opcua_host", "0.0.0.0")
opcua_user = os.environ.get("opcua_user", "")  # unused
opcua_pasword = os.environ.get("opcua_pasword", "")  # unused
opcua_port = os.environ.get("opcua_port", "4840")

# --------------------------------------------------
# zuerst sicherstellen, dass die Datenbank existiert
# --------------------------------------------------
# sqlalchemy erwarted bereits eine datenbank
# lege datenbank mit "nackten" psycopg2 Befehlen an
# wenn sie schon vorhanden ist, ignoriere entsprechenden Fehler
# sudo -u postgres psql -e --command "CREATE USER frank WITH SUPERUSER PASSWORD 'frank'"
con = psycopg2.connect(  #'postgres://frank:frank@localhost:55432'
    dbname="postgres", user=db_user, host=db_host, password=db_pasword, port=db_port
)
con.autocommit = True
cur = con.cursor()
# select exists(
#     SELECT datname FROM pg_catalog.pg_database WHERE lower(opcua) = lower('opcua')
# );
try:
    cur.execute("CREATE DATABASE {};".format("opcua"))
except Exception as e:
    pass  # exists already
finally:
    con.close()

# --------------------------------------------------
# sqlalchemy session anlegen
# --------------------------------------------------
con_dic = {"user": db_user, "pw": db_pasword, "host": db_host, "port": db_port}
db_string = "postgres://%(user)s:%(pw)s@%(host)s:%(port)s/opcua" % con_dic
db = create_engine(db_string)
base = declarative_base()


class BearbeitungscenterDB(base):
    """[Schreiben der Daten in Postgres DB]

    Arguments:
        object {[type]} -- [description]
    """

    __tablename__ = "servers"

    mkey = Column(String, primary_key=True)
    name = Column(String)
    pid = Column(Integer)
    dockerid = Column(String)
    ip = Column(String)
    port = Column(Integer)
    status = Column(String)  # idle, gestarted, gestoppt, fehler


class Bearbeitungscenter(object):
    """Ein bearbeitungszentrum kann Aufträge ausführen
    es muss als singelton behandelt werden

    """

    def __init__(self, DBHandler_cls):
        """initialisiert die Datenbank und meldet das Bearbeitungszentrum an

        Arguments:
            DBHandler_cls {BearbeitungscenterDB Klasse} -- wird genutzt um Operationen auf der DB auszuführen
        """
        self.CenterDB = DBHandler_cls
        Session = sessionmaker(db)
        self.session = Session()

        base.metadata.create_all(db)

        # Make ourselfs known to the outside world
        self.m_center = DBHandler_cls(
            mkey="Bearbeitungscenter_%s" % os.getpid(),
            name="Kann Schruppen, Fräsen und Jodeln",
            pid=os.getpid(),
            ip="2016",
            port=999,
            status="started",
        )
        try:
            self.session.add(self.m_center)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            self.m_center.status="started"
            self.session.commit()

    # handle termination signals cleanly
    def updateServer(self, signalNumber, frame):
        """Melde der Server ab

        Arguments:
            signalNumber {Signal} -- das Terminate Signal, das an den Prozess geschickt wird
            Nur Signal 14 wird abgefange
            frame {[type]} -- [description]
        """
        print("Received:", signalNumber)
        if self.m_center.pid:
            self.m_center.pid = None
            self.m_center.status = "idle"
        else:
            self.m_center.pid = os.getpid()
            self.m_center.status = "am chrampfe"
        self.session.commit()
        return

    # handle termination signals cleanly
    def unregisterServer(self, signalNumber, frame):
        """Melde der Server ab

        Arguments:
            signalNumber {Signal} -- das Terminate Signal, das an den Prozess geschickt wird
            Nur Signal 15 wird abgefangen
            frame {[type]} -- [description]
        """
        print("Received:", signalNumber)
        print("Tschüss zäme")
        # Delete
        self.session.delete(self.m_center)
        self.session.commit()
        sys.exit()


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


# method to be exposed through server


def func(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


# method to be exposed through server
# uses a decorator to automatically convert to and from variants


@uamethod
def multiply(parent, x, y):
    print("multiply method call with parameters: ", x, y)
    return x * y


class VarUpdater(Thread):
    def __init__(self, var):
        Thread.__init__(self)
        self._stopev = False
        self.var = var

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            v = sin(time.time() / 10)
            self.var.set_value(v)
            time.sleep(0.1)


if __name__ == "__main__":
    # optional: setup logging
    logging.basicConfig(level=logging.WARN)
    # logger = logging.getLogger("opcua.address_space")
    # logger.setLevel(logging.DEBUG)
    # logger = logging.getLogger("opcua.internal_server")
    # logger.setLevel(logging.DEBUG)
    # logger = logging.getLogger("opcua.binary_server_asyncio")
    # logger.setLevel(logging.DEBUG)
    # logger = logging.getLogger("opcua.uaprocessor")
    # logger.setLevel(logging.DEBUG)

    # now setup our server
    server = Server()
    # Bearbeitungszentrum anlegen, mit BearbeitungscenterDB-Klasse als parameter
    center = Bearbeitungscenter(BearbeitungscenterDB)
    # register the signals to be caught
    signal.signal(signal.SIGALRM, center.updateServer) # signal 14
    signal.signal(signal.SIGTERM, center.unregisterServer) # signal 15

    # server.disable_clock()
    # server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("FreeOpcUa Example Server")
    # set all possible endpoint policies for clients to connect through
    server.set_security_policy(
        [
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign,
        ]
    )

    # setup our own namespace
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # create a new node type we can instantiate in our address space
    dev = server.nodes.base_object_type.add_object_type(idx, "MyDevice")
    dev.add_variable(idx, "sensor1", 1.0).set_modelling_rule(True)
    dev.add_property(idx, "device_id", "0340").set_modelling_rule(True)
    ctrl = dev.add_object(idx, "controller")
    ctrl.set_modelling_rule(True)
    ctrl.add_property(idx, "state", "Idle").set_modelling_rule(True)

    # populating our address space

    # First a folder to organise our nodes
    myfolder = server.nodes.objects.add_folder(idx, "myEmptyFolder")
    # instanciate one instance of our device
    mydevice = server.nodes.objects.add_object(idx, "Device0001", dev)
    mydevice_var = mydevice.get_child(
        ["{}:controller".format(idx), "{}:state".format(idx)]
    )  # get proxy to our device state variable
    # create directly some objects and variables
    myobj = server.nodes.objects.add_object(idx, "MyObject")
    myvar = myobj.add_variable(idx, "MyVariable", 6.7)
    mysin = myobj.add_variable(idx, "MySin", 0, ua.VariantType.Float)
    myvar.set_writable()  # Set MyVariable to be writable by clients
    mystringvar = myobj.add_variable(idx, "MyStringVariable", "Really nice string")
    mystringvar.set_writable()  # Set MyVariable to be writable by clients
    mydtvar = myobj.add_variable(idx, "MyDateTimeVar", datetime.utcnow())
    mydtvar.set_writable()  # Set MyVariable to be writable by clients
    myarrayvar = myobj.add_variable(idx, "myarrayvar", [6.7, 7.9])
    myarrayvar = myobj.add_variable(
        idx, "myStronglytTypedVariable", ua.Variant([], ua.VariantType.UInt32)
    )
    myprop = myobj.add_property(idx, "myproperty", "I am a property")
    mymethod = myobj.add_method(
        idx, "mymethod", func, [ua.VariantType.Int64], [ua.VariantType.Boolean]
    )
    multiply_node = myobj.add_method(
        idx,
        "multiply",
        multiply,
        [ua.VariantType.Int64, ua.VariantType.Int64],
        [ua.VariantType.Int64],
    )

    # import some nodes from xml
    server.import_xml("custom_nodes.xml")

    # creating a default event object
    # The event object automatically will have members for all events properties
    # you probably want to create a custom event type, see other examples
    myevgen = server.get_event_generator()
    myevgen.event.Severity = 300

    # starting!
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    vup = VarUpdater(mysin)  # just  a stupide class update a variable
    vup.start()
    try:
        # enable following if you want to subscribe to nodes on server side
        # handler = SubHandler()
        # sub = server.create_subscription(500, handler)
        # handle = sub.subscribe_data_change(myvar)
        # trigger event, all subscribed clients wil receive it
        var = (
            myarrayvar.get_value()
        )  # return a ref to value in db server side! not a copy!
        var = copy.copy(
            var
        )  # WARNING: we need to copy before writting again otherwise no data change event will be generated
        var.append(9.3)
        myarrayvar.set_value(var)
        mydevice_var.set_value("Running")
        myevgen.trigger(message="This is BaseEvent")
        server.set_attribute_value(
            myvar.nodeid, ua.DataValue(9.9)
        )  # Server side write method which is a but faster than using set_value

        # tell us what PID we have
        print("My PID is:", os.getpid())
        # run for ever
        while True:
            time.sleep(0.1)
        # embed()

    finally:
        vup.stop()
        server.stop()
