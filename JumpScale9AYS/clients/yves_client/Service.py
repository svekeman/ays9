from requests.exceptions import HTTPError

def _extract_error(resp):
    if isinstance(resp, HTTPError):
        if resp.response.headers['Content-type'] == 'application/json':
            content = resp.response.json()
            return content.get('error', resp.response.text)
        return resp.response.text
    raise resp

class Services:
    def __init__(self, repository):
        self._repository = repository
        self._api = repository._api

    def list(self, role=None, name=None):
        """
        List all AYS services with specific role and instance name.

        Args:
            role: role of the service
            name: name of the service

        Returns: list of services
        """
        try:
            resp = self._api.listServices(self._repository.model.get('name'))

            ays_services = resp.json()
            services = list()
            for service in sorted(ays_services, key=lambda service: '{role}!{name}'.format(**service)):
                if role and service['role'] != role:
                    continue
                if name and service['name'] != name:
                    continue
                services.append(Service(self._repository, service))
            return services

        except Exception as e:
            print("Error while listing services: {}".format(_extract_error(e)))

    def get(self, role, name):
        """
        Get the AYS service with a specific role and instance name.

        Args:
            role: role of the service
            name: name of the service

        Returns: service instance

        Raises: KeyError when no service match the specified arguments.
        """
        for service in self.list():
            if service.model['role'] == role and service.model['name'] == name:
                return service
        raise KeyError("Could not find service with role {} and name {}".format(role, name))

    def delete(self, role, name):
        """
        Delete all services with a specific role and instance name.

        Args:
            role: role of the service
            name: name of the service

        Returns: nothing if succesful. else error from HTTP response object
        """
        try:
            for service in sorted(self.list(role, name), key=lambda service: service['role']):
                self._api.deleteServiceByName(name=service['name'], role=service['role'], repository=self._repository.mode['name'])
        except Exception as e:
            return _extract_error(e)

class Service:
    def __init__(self, repository, model):
        self._repository = repository
        self._api = repository._api
        self.model = model

    def show(self):
        return

    def state(self):
        return

    def getChildren(self):
        """
        Get all children of the service

        Args: none

        Returns: list of children
        """
        children = list()
        if self.model['children']:
            for child in service['children']:
                children.append(Service(self._repository, service))

    def delete(self):
        """
        Delete a service and all its children.
        Be carefull with this action, there is undo option.

        Returns: HTTP response object
        """
        resp = self._api.deleteServiceByName(name=self.model['name'], role=self.model['role'], repository=self._repository.model['name'])
        return resp

    def __repr__(self):
        return "service: %s" % (self.model["name"])

    __str__ = __repr__
