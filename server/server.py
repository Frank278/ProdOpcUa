import os.path
try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

from opcua import ua, uamethod, Server




@uamethod
def start_work(parent):
    status = "gestartet"
    # LED Grün leuchtet


@uamethod
def say_hello(parent, happy):
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(result)
    return result

def stop_programm(parent):
    status = "gestoppt"
    # LED Rot leuchtet

@uamethod
def say_hello_xml(parent, happy, hugo):
    print("Calling say_hello_xml")
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(hugo)
    print(result)
    return result


@uamethod
def say_hello(parent, happy):
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(result)
    return result


@uamethod
def say_hello_array(parent, happy):
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(result)
    return [result, "Actually I am"]

@uamethod
def say_hello_hugo(parent):
    print('ich säge nüüt')
    return 'hugo'


class HelloServer:
    def __init__(self, endpoint, name, model_filepath):
        self.server = Server()

        #  This need to be imported at the start or else it will overwrite the data
        self.server.import_xml(model_filepath)

        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)

        objects = self.server.get_objects_node()

        freeopcua_namespace = self.server.get_namespace_index("urn:freeopcua:python:server")
        hellower = objects.get_child("0:Hellower")
        hellower_say_hello = hellower.get_child("0:SayHello")

        self.server.link_method(hellower_say_hello, say_hello_xml)

        hellower.add_method(
            freeopcua_namespace, "SayHello2", say_hello, [ua.VariantType.Boolean], [ua.VariantType.String], [ua.VariantType.String])

        hellower.add_method(
            freeopcua_namespace, "SayHelloArray", say_hello_array, [ua.VariantType.Boolean], [ua.VariantType.String])

        hellower.add_method(
            freeopcua_namespace, "SayHelloHugo", say_hello_hugo)


    def __enter__(self):
        self.server.start()
        return self.server

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.stop()


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    with HelloServer(
            "opc.tcp://0.0.0.0:40840/freeopcua/server/",
            "FreeOpcUa Example Server",
            os.path.join(script_dir, "test_saying.xml")) as server:
        embed()