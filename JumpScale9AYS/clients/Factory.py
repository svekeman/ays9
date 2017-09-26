from JumpScale9AYS.clients.sync_client import Client
from JumpScale9AYS.clients.yves_client import Client as Client2

class Factory:

    def __init__(self):
        self.__jslocation__ = "j.clients.atyourservice"

    def get(self, base_uri="http://localhost:5000"):
        return Client(base_uri=base_uri)

    def get2(self, base_uri="http://localhost:5000"):
        return Client2(base_uri=base_uri)
