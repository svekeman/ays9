class Blueprints:
    def __init__(self, repository):
        self._repository = repository
        self._api = repository._api

    def list(self):
        """
        List all blueprints.
        """
        ays_blueprints = self._api.listBlueprints(self._repository.model.get('name')).json()
        blueprints = list()
        for blueprint in ays_blueprints:
            blueprints.append(Blueprint(self._repository, blueprint))
        return blueprints

    def get(self, name):
        for blueprint in self.list():
            if blueprint.model.get('name') == name:
                return blueprint
        raise ValueError("Could not find blueprint with name {}".format(name))

    def create(self, name, blueprint):
        data = j.data.serializer.json.dumps({'name': name, 'content': blueprint})

        resp = self._api.createBlueprint(data, self.model["name"], headers=None)

        return self.get(name)

    def execute(self):
        for blueprint in sorted(self.list()):
            blueprint.execute()

class Blueprint:
    def __init__(self, repository, model):
        self._repository = repository
        self._api = repository._api
        self.model = model

    def execute(self):
        resp = self._api.executeBlueprint('', self.model['name'], self._repository.model['name'], headers=None)

    def __repr__(self):
        return "blueprint: %s" % (self.model["name"])

    __str__ = __repr__
