from opcua import Client, ua
from opcua.ua import ua_binary as uabin
from opcua.common.methods import call_method


class HelloClient:
    def __init__(self, endpoint):
        self.client = Client(endpoint)

    def __enter__(self):
        self.client.connect()
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.disconnect()


if __name__ == '__main__':
    #with HelloClient("opc.tcp://10.42.0.77:40840/freeopcua/server/") as client:

    with HelloClient("opc.tcp://192.168.1.112:4840/freeopcua/server/") as client:
    #with HelloClient("opc.tcp://localhost:40840/freeopcua/server/") as client:
        root = client.get_root_node()
        print("Root node is: ", root)
        objects = client.get_objects_node()
        print("Objects node is: ", objects)

        hellower = objects.get_child("0:Hellower")
        print("Hellower is: ", hellower)

        resulting_text = hellower.call_method("0:StartProgram", True)
        print(resulting_text)


        resulting_text = hellower.call_method("0:SayHello", False, 'tums züg')
        print(resulting_text)

        resulting_text = hellower.call_method("1:SayHello2", True)
        print(resulting_text)

        resulting_array = hellower.call_method("1:SayHelloArray", False)
        print(resulting_array)
        
        resulting_array = hellower.call_method("1:SayHelloHugo")

        print(resulting_array)

        while True:
            Temp = client.get_node("ns=2; i=2")
            Temperature = Temp.get_value()
            print(Temperature)

            Press = client.get_node("ns=2; i=3")
            Pressure = Press.get_value()
            print(Pressure)

            TIME = client.get_node("ns=2; i=4")
            TIME_Value = TIME.get_value()


       # DB API von Django
       # test = Test(Temperature, Pressure, TIME_Value)
       # test.save()




