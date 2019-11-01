import sys
sys.path.insert(0, "..")
import logging
import time

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()


from opcua import Client
from opcua import ua


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)

    client = Client("opc.tcp://192.168.1.112:50840/freeopcua/server/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        client.connect()
        client.load_type_definitions()  # load definition of server specific structures/extension objects

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Root node is: ", root)
        objects = client.get_objects_node()
        print("Objects node is: ", objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())

        # get a specific node knowing its node id

        # gettting our namespace idx
        uri = "http://examples.freeopcua.github.io"
        idx = client.get_namespace_index(uri)

        # Now getting a variable node using its browse path
        myvar = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:MyVariable".format(idx)])

        obj = root.get_child(["0:Objects", "{}:MyObject".format(idx)])
        print("myvar is: ", myvar)

        # subscribing to a variable node
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(myvar)
        time.sleep(0.1)

        # we can also subscribe to events from server
        sub.subscribe_events()
        # sub.unsubscribe(handle)
        # sub.delete()

        # calling a method on server
        res = obj.call_method("{}:multiply".format(idx), 5, "klk")
        print("method result is: ", res)

        while True:
            Temp = client.get_node("ns=2; i=20")
            Temperature = Temp.get_value()
            print(Temperature)

            Press = client.get_node("ns=2; i=21")
            Pressure = Press.get_value()
            print(Pressure)

            TIME = client.get_node("ns=2; i=22")
            TIME_Value = TIME.get_value()
            print(TIME_Value)
            time.sleep(5)

            Sta = client.get_node("ns=2; i=23")
            Status = Sta.get_value()
            print(Status)

            Servern = client.get_node("ns=2; i=24")
            Servername = Servern.get_value()
            print(Servername)

            Port = client.get_node("ns=2; i=25")
            Portnummmer = Port.get_value()
            print(Portnummmer)
            time.sleep(5)


        embed()
    finally:
        client.disconnect()