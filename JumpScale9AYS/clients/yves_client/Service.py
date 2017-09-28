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
        List all AYS service instances with specific role and instance name.
        """
        try:
            resp = self._api.listServices(self._repository.model.get('name'))
            ays_services = resp.json()
            services = list()
            for service in sorted(ays_services, key=lambda service: '{role}!{name}'.format(**service)):
                if role and s['role'] != role:
                    continue
                if name and s['name'] != name:
                    continue
                services.append(Service(self._repository, service))
            return services

        except Exception as e:
            print("Error while listing services: {}".format(_extract_error(e)))

    def get(self, name, role):
        for service in self.list():
            if service.model['name'] == name and service.model['role'] == role:
                return service
        raise ValueError("Could not find service with name {}".format(name))

class Service:
    def __init__(self, repository, model):
        self._repository = repository
        self.model = model

    def show(self):
        return

    def state(self):
        return

    def delete(self):
        return

    def __repr__(self):
        return "service: %s" % (self.model["name"])

    __str__ = __repr__
