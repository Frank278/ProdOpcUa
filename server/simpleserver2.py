import sys
from _ast import Param

sys.path.insert(0, "..")
import time

from opcua import ua, Server
from random import randint
import datetime


if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://localhost:4840/")

    name = "OPC_SIMULATION_SERVER"
    addspace =server.register_namespace(name)

    # get Objects node, this is where we should put our nodes
    node = server.get_objects_node()

    Param = node.add_object(addspace, "Parameters")

    # add Parameter to the Object
    Temp = Param.add_variable(addspace, "Temperature", 0)
    Press = Param.add_variable(addspace, "Pressure", 0)
    Time = Param.add_variable(addspace, "Time", 0)


    Temp.set_writable()
    Press.set_writable()
    Time.set_writable()

    # populating our address space
    #myobj = objects.add_object(0, "MyObject")
    #myvar = myobj.add_variable(0, "MyVariable", 6.7)
    #myvar.set_writable()  # Set MyVariable to be writable by clients





    # starting!
    server.start()

    try:
        count = 0
        while True:
            time.sleep(5)
            #count += 0.1
            #myvar.set_value(count)

            Temperature = randint(10, 20)
            Pressure = randint(10, 20)
            TIME = datetime.datetime.now()

            print(Temperature, Pressure, TIME)
            Temp.set_value(Temperature)
            Press.set_value(Pressure)
            Time.set_value(TIME)

            time.sleep(5)


    finally:
        # close connection, remove subcsriptions, etc
        server.stop()