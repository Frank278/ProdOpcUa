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
    Abonnement-Handler. Um Ereignisse vom Server für ein Abonnement zu erhalten
    Die Methoden data_change und event werden direkt vom empfangenden Thread aufgerufen.
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
        client.load_type_definitions()  # Ladet Definition von serverspezifischen Strukturen / Erweiterungsobjekten


        # Der Client verfügt über einige Methoden, um einen Proxy für UA-Knoten abzurufen,
        # die sich immer im Adressraum befinden sollten, z. B. Root oder Objects

        root = client.get_root_node()
        print("Root node is: ", root)
        objects = client.get_objects_node()
        print("Objects node is: ", objects)


        # Knotenobjekte verfügen über Methoden zum Lesen und Schreiben von Knotenattributen
        # sowie zum Durchsuchen oder Auffüllen des Adressraums
        print("Children of root are: ", root.get_children())

        # Holen Sie sich Informationen eines Knoten mit Kenntnis seiner Knoten-ID

        # gettting our namespace idx
        uri = "http://freeopcua.github.io"
        idx = client.get_namespace_index(uri)

        # Jetzt wird ein variabler Knoten über den Suchpfad abgerufen
        myvar = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:MyVariable".format(idx)])

        obj = root.get_child(["0:Objects", "{}:MyObject".format(idx)])
        print("myvar is: ", myvar)

        # Abonnieren eines variablen Knotens
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(myvar)
        time.sleep(0.1)

        # Wir können auch Ereignisse vom Server abonnieren
        sub.subscribe_events()
        # sub.unsubscribe(handle)
        # sub.delete()

        # Aufrufen einer Methode auf dem Server
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