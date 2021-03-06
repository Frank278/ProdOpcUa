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
from random import randint

from sqlalchemy import create_engine, DateTime
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
db_pasword = os.environ.get("db_pasword", "admin")
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
    dbname="opcuaDB", user=db_user, host=db_host, password=db_pasword, port=db_port
)
con.autocommit = True
cur = con.cursor()
# select exists(
#     SELECT datname FROM pg_catalog.pg_database WHERE lower(opcua) = lower('opcua')
# );
try:
    cur.execute("CREATE DATABASE {};".format("opcuaDB"))
except Exception as e:
    pass  # exists already
finally:
    con.close()

# --------------------------------------------------
# sqlalchemy session anlegen
# --------------------------------------------------
con_dic = {"user": db_user, "pw": db_pasword, "host": db_host, "port": db_port}
db_string = "postgres://%(user)s:%(pw)s@%(host)s:%(port)s/opcuaDB" % con_dic
db = create_engine(db_string)
base = declarative_base()


class opcuaDB(base):
    """[Schreiben der Daten in Postgres DB]

    Arguments:
        object {[type]} -- [description]
    """

    __tablename__ = "opc_serverdata"

    mkey = Column(String, primary_key=True)
    servername = Column(String)
    pid = Column(Integer)
    dockerid = Column(String)
    ip = Column(String)
    port = Column(Integer)
    status = Column(String)  # idle, gestarted, gestoppt, stoerung
    temp = Column(Integer)
    press = Column(Integer)
    time = Column(DateTime, default=datetime.utcnow)


class Bearbeitungscenter(object):
    """Eine Maschine kann Aufträge ausführen
    es muss als singelton behandelt werden

    """

    def __init__(self, DBHandler_cls):
        """initialisiert die Datenbank und meldet die Maschine an

        Arguments:
            DBHandler_cls {MaschinenDB Klasse} -- wird genutzt um Operationen auf der DB auszuführen
        """
        self.CenterDB = DBHandler_cls
        Session = sessionmaker(db)
        self.session = Session()

        base.metadata.create_all(db)

        # Make ourselfs known to the outside world
        self.m_center = DBHandler_cls(
            mkey="Bearbeitungscenter_%s" % os.getpid(),
            servername="Seinbeisser",
            pid=os.getpid(),
            ip="2016",
            port=999,
            status="started",
            temp=20,
            press= 20,
            time= datetime.utcnow(),
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
        """Serverdateb updaten

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
            self.m_center.status = "am Arbeiten"
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
        print("Abmelden")
        # Delete
        self.session.delete(self.m_center)
        self.session.commit()
        sys.exit()

        # handle termination signals cleanly

    def updateValueServer(self, Temp, Status):

        """Melde der Server ab

        Arguments:
         
        """
        self.session.add(self.m_center)


        self.m_center.status = Status
        self.m_center.temp = Temp
        # print("received:", signalnumber)
        # if self.m_center.pid:
        #     self.m_center.pid = none
        #     self.m_center.status = "idle"
        # else:
        #     self.m_center.pid = os.getpid()
        #     self.m_center.status = "aktiv"
        self.session.commit()
        return


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
def start_demoprogramm(parent):
    status = " Demoprogramm gestartet"
    time.sleep(10)
    status = " Demoprogramm beendet"



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
    center = Bearbeitungscenter(opcuaDB)

    # Registrieren der zu erfassenden Signale
    signal.signal(signal.SIGALRM, center.updateServer)  # signal 14
    signal.signal(signal.SIGTERM, center.unregisterServer)  # signal 15

    # server.disable_clock()
    # server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("Fräsmaschine01 Server")
    # Anlegen der möglichen Endpunktrichtlinien für Clients fest,
    # über die eine Verbindung hergestellt werden soll
    server.set_security_policy(
        [
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign,
        ]
    )

    # Adressraum festlegen
    uri = "http://freeopcua.github.io"
    idx = server.register_namespace(uri)

    # Erstellen eines neuen Knotentyp, den wir in unserem Adressraum instanziieren können
    dev = server.nodes.base_object_type.add_object_type(idx, "MyDevice")
    dev.add_variable(idx, "sensor1", 1.0).set_modelling_rule(True)
    dev.add_property(idx, "device_id", "0340").set_modelling_rule(True)
    ctrl = dev.add_object(idx, "controller")
    ctrl.set_modelling_rule(True)
    ctrl.add_property(idx, "state", "Idle").set_modelling_rule(True)

    # unseren Adressraum einrichten
    # Zuerst einen Ordner, um unsere Knoten zu organisieren
    machinefolder = server.nodes.objects.add_folder(idx, "myFolder")
    # instanziieren einer Instanz unseres Geräts
    machinedevice = server.nodes.objects.add_object(idx, "Device0001", dev)
    machinedevice_var = machinedevice.get_child(
        ["{}:controller".format(idx), "{}:state".format(idx)])  # get proxy to our device state variable
    # Erstellen  einiger Objekte und Variablen
    machine = server.nodes.objects.add_object(idx, "MachineObject")
    machinevar = machine.add_variable(idx, "MachineVariable", 6.7)

    # Parameter zum Objekt hinzufügen
    machinesin = machine.add_variable(idx, "MachineSin", 0, ua.VariantType.Float)
    machinevar.set_writable()  # Set MyVariable to be writable by clients
    machinestringvar = machine.add_variable(idx, "MyStringVariable", "Really nice string")
    machinestringvar.set_writable()  # Set MyVariable to be writable by clients
    madtvar = machine.add_variable(idx, "MyDateTimeVar", datetime.utcnow())
    madtvar.set_writable()  # Set MyVariable to be writable by clients
    machinearrayvar = machine.add_variable(idx, "myarrayvar", [6.7, 7.9])
    machinestrongarrayvar = machine.add_variable(idx, "myStronglytTypedVariable", ua.Variant([], ua.VariantType.UInt32))
    machineprop = machine.add_property(idx, "myproperty", "I am a property")

    # Parameter zum Objekt hinzufügen
    Temp = machine.add_variable(idx, "Temperature", 0)
    Temp.set_writable()  # Stellt MyVariable so ein, dass es von Clients beschrieben werden kann
    Press = machine.add_variable(idx, "Pressure", 0)
    Press.set_writable()  # Stellt Press so ein, dass es von Clients beschrieben werden kann
    Time = machine.add_variable(idx, "Time", 0)
    Time.set_writable()  # Stellt Time so ein, dass es von Clients beschrieben werden kann
    Status = machine.add_variable(idx, "Status", 0)
    Status.set_writable()  # Stellt Staus so ein, dass es von Clients beschrieben werden kann
    Servername = machine.add_variable(idx, "Servername", 0)
    Servername.set_writable()  # Stellt Servername so ein, dass es von Clients beschrieben werden kann
    Portnummer = machine.add_variable(idx, "Portnummer", 0)
    Portnummer.set_writable()  # Stellt Portnummer so ein, dass es von Clients beschrieben werden kann

    # Parameter zum Objekt hinzufügen
    mymethod = machine.add_method(idx, "mymethod", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    start_programm = machine.add_method(idx, "startprogramm", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    stop_programm = machine.add_method(idx, "stop_programm", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    get_status = machine.add_method(idx, "get_status", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])

    multiply_node = machine.add_method(
        idx,
        "multiply",
        multiply,
        [ua.VariantType.Int64, ua.VariantType.Int64],
        [ua.VariantType.Int64],
    )

    # import der Kn oten aus dem xml
    server.import_xml("custom_nodes.xml")

    # Erstellen eines Standardereignisobjekts
    # Das Ereignisobjekt hat automatisch Mitglieder für alle Ereignisseigenschaften
    myevgen = server.get_event_generator()
    myevgen.event.Severity = 300

    # starting!
    server.start()
    print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
    vup = VarUpdater(machinesin)  # just  a stupide class update a variable
    vup.start()
    try:

        var = machinearrayvar.get_value()  # # Rückgabe eines Verweises auf den Wert auf der DB-Serverseite! keine Kopie!
        var = copy.copy(
            var)  # WARNING: Wir müssen vor dem erneuten Schreiben kopieren, da sonst kein Datenänderungsereignis generiert wird
        var.append(9.3)
        machinearrayvar.set_value(var)
        machinedevice_var.set_value("Running")
        myevgen.trigger(message="This is BaseEvent")
        server.set_attribute_value(machinevar.nodeid, ua.DataValue(
            9.9))  # Serverseitige Schreibmethode, die jedoch schneller ist als die Verwendung von set_value
        # gibt unsere PID aus
        print("My PID is:", os.getpid())

        # zum testen
        count = 0
        while True:
            time.sleep(5)
            # count += 0.1
            # myvar.set_value(count)

            Temperature = randint(10, 20)
            Pressure = randint(10, 20)
            TIME = datetime.utcnow()
            count = randint(1, 3)
            if count == 1:
                status = 'Gestartet'
            elif count == 2:
                status = 'Gestoppt'
            elif count == 3:
                status = 'Störung'

            servername = "Fräsmachine01"
            portnummer = "50840"
            # Ausgeben der Werte
            print(Temperature, Pressure, TIME, status, servername, portnummer)
            # Setzen der Werte in die UA Variablen
            Temp.set_value(Temperature)
            Press.set_value(Pressure)
            Time.set_value(TIME)
            Status.set_value(status)
            Servername.set_value(servername)
            Portnummer.set_value(portnummer)

            # Hier werden die Variablen der Funtktion Update übergeben
            center.updateValueServer(Temperature, status)

            time.sleep(5)

        #embed()



    finally:
        vup.stop()
        server.stop()
