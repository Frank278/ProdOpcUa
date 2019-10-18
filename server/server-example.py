from threading import Thread
import copy
import logging
from datetime import datetime
import time
from math import sin
import sys


from random import randint

sys.path.insert(0, "..")


try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()


from opcua import ua, uamethod, Server


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
status="gestoppt"

@uamethod
def multiply(parent, x, y):
    print("multiply method call with parameters: ", x, y)
    return x * y

@uamethod
def start_programm(parent):
    print("startprogramm method call  ")

    global status
    print("Der Staus war: ", status)
    status = "gestartet"
    print("Jetzt ist der Status: ", status)
    time.sleep(5)
    status = "beendet"



@uamethod
def stop_programm(parent):
    print("stop method call : ")
    global status
    status = "gestoppt"


@uamethod
def get_status(parent):
    print("get_status method call : ")
    return get_status


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
    #logger = logging.getLogger("opcua.address_space")
    # logger.setLevel(logging.DEBUG)
    #logger = logging.getLogger("opcua.internal_server")
    # logger.setLevel(logging.DEBUG)
    #logger = logging.getLogger("opcua.binary_server_asyncio")
    # logger.setLevel(logging.DEBUG)
    #logger = logging.getLogger("opcua.uaprocessor")
    # logger.setLevel(logging.DEBUG)

    # now setup our server
    server = Server()
    #server.disable_clock()
    #server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
    server.set_endpoint("opc.tcp://0.0.0.0:50840/freeopcua/server/")
    server.set_server_name("FreeOpcUa Example Server")
    # set all possible endpoint policies for clients to connect through
    server.set_security_policy([
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ua.SecurityPolicyType.Basic256Sha256_Sign])

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
    machinefolder = server.nodes.objects.add_folder(idx, "myFolder")
    # instanciate one instance of our device
    machinedevice = server.nodes.objects.add_object(idx, "Device0001", dev)
    machinedevice_var = machinedevice.get_child(["{}:controller".format(idx), "{}:state".format(idx)])  # get proxy to our device state variable
    # create directly some objects and variables
    machine = server.nodes.objects.add_object(idx, "MachineObject")
    machinevar = machine.add_variable(idx, "MachineVariable", 6.7)

    # add Parameter to the Object
    machinesin = machine.add_variable(idx, "MachineSin", 0, ua.VariantType.Float)
    machinevar.set_writable()    # Set MyVariable to be writable by clients
    machinestringvar = machine.add_variable(idx, "MyStringVariable", "Really nice string")
    machinestringvar.set_writable()    # Set MyVariable to be writable by clients
    madtvar = machine.add_variable(idx, "MyDateTimeVar", datetime.utcnow())
    madtvar.set_writable()    # Set MyVariable to be writable by clients
    machinearrayvar = machine.add_variable(idx, "myarrayvar", [6.7, 7.9])
    machinearrayvar = machine.add_variable(idx, "myStronglytTypedVariable", ua.Variant([], ua.VariantType.UInt32))
    machineprop = machine.add_property(idx, "myproperty", "I am a property")

    # add Parameter to the Object
    Temp = machine.add_variable(idx, "Temperature", 0)
    Temp.set_writable()  # Set MyVariable to be writable by clients
    Press = machine.add_variable(idx, "Pressure", 0)
    Press.set_writable()  # Set MyVariable to be writable by clients
    Time = machine.add_variable(idx, "Time", 0)
    Time.set_writable()  # Set MyVariable to be writable by clients
    Status = machine.add_variable(idx, "Time", 0)
    Status.set_writable()  # Set MyVariable to be writable by clients
    Servername = machine.add_variable(idx, "Time", 0)
    Servername.set_writable()  # Set MyVariable to be writable by clients
    Portnummer = machine.add_variable(idx, "Time", 0)
    Portnummer.set_writable()  # Set MyVariable to be writable by clients





    mymethod = machine.add_method(idx, "mymethod", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    start_programm = machine.add_method(idx, "startprogramm", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    stop_programm = machine.add_method(idx, "stop_programm", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])
    get_status = machine.add_method(idx, "get_status", func, [ua.VariantType.Int64], [ua.VariantType.Boolean])








    multiply_node = machine.add_method(idx, "multiply", multiply, [ua.VariantType.Int64, ua.VariantType.Int64], [ua.VariantType.Int64])

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
    vup = VarUpdater(machinesin)  # just  a stupide class update a variable
    vup.start()
    try:
        # enable following if you want to subscribe to nodes on server side
        #handler = SubHandler()
        #sub = server.create_subscription(500, handler)
        #handle = sub.subscribe_data_change(myvar)
        # trigger event, all subscribed clients wil receive it
        var = machinearrayvar.get_value()  # return a ref to value in db server side! not a copy!
        var = copy.copy(var)  # WARNING: we need to copy before writting again otherwise no data change event will be generated
        var.append(9.3)
        machinearrayvar.set_value(var)
        machinedevice_var.set_value("Running")
        myevgen.trigger(message="This is BaseEvent")
        server.set_attribute_value(machinevar.nodeid, ua.DataValue(9.9))  # Server side write method which is a but faster than using set_value


        #zum testen
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

            servername = "Server-example"
            portnummer = "50840"

            print(Temperature, Pressure, TIME, status, servername, portnummer)
            Temp.set_value(Temperature)
            Press.set_value(Pressure)
            Time.set_value(TIME)
            Status.set_value(status)
            Servername.set_value(servername)
            Portnummer.set_value(portnummer)



            time.sleep(5)

        embed()
    finally:
        vup.stop()
        server.stop()