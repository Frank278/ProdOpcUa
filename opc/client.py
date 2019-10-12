from opcua import Client, ua
from opcua.ua import ua_binary as uabin
from opcua.common.methods import call_method
from .models import Test
url = "opc.tpc://10.42.0.77:4840"

client = Client(url)
client.connect()

while True:
    Temp = client.get_node("ns=2; i=2")
    Temperature = Temp.get_value()

    Press = client.get_node("ns=2; i=3")
    Pressure = Press.get_value()

    TIME = client.get_node("ns=2; i=4")
    TIME_Value = TIME.get_value()

    test = Test(Temperature, Pressure, TIME_Value)
    test.save()
    #start = client.