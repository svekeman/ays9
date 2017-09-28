from js9 import j
from .Repository import Repositories

#todo: support JWT

class Client:
    def __init__(self, base_uri="https://localhost:5000"):
        self._ayscl = j.clients.atyourservice.get(base_uri)
        self.repositories = Repositories(self)
