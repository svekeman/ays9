from js9 import j
from .Repository import Repositories

class Client:
    def __init__(self, base_uri="https://localhost:5000", jwt=None):
        self._ayscl = j.clients.atyourservice.get(base_uri)
        self.repositories = Repositories(self)
        if jwt:
            self._ayscl.api.set_auth_header('Bearer {}'.format(jwt))