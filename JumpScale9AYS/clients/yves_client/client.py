from js9 import j
from requests.exceptions import HTTPError

#todo: support JWT

def _extract_error(resp):
    if isinstance(resp, HTTPError):
        if resp.response.headers['Content-type'] == 'application/json':
            content = resp.response.json()
            return content.get('error', resp.response.text)
        return resp.response.text
    raise resp

class Client:
    def __init__(self, base_uri="https://localhost:5000"):
        self.ayscl = j.clients.atyourservice.get(base_uri)

    @property
    def repositories(self):
        ays_repositories = self.ayscl.api.ays.listRepositories().json()
        repositories = list()
        for repository in ays_repositories:
            repositories.append(Repository(self.ayscl, repository))
        return repositories

    def repository_get(self, name, create=True, git=None):
        for repository in self.repositories:
            if repository.model.get('name') == name:
                return repository
        else:
            if create is False:
                raise KeyError("No repository with name \"%s\" found" % name)
            if git == None:
                raise j.exceptions.RuntimeError("Missing value for git argument.")
            data = j.data.serializer.json.dumps({'name': name, 'git_url': git})
            self.ayscl.api.ays.createRepository(data)
            return self.repository_get(name, False)


class Repository:
    def __init__(self, client, model):
        self.ayscl = client
        self.model = model

    def __repr__(self):
        return "repository: %s" % (self.model["name"])

    __str__ = __repr__

    @property
    def blueprints(self):
        ays_blueprints = self.ayscl.api.ays.listBlueprints(self.model.get('name')).json()
        blueprints = list()
        for blueprint in ays_blueprints:
            blueprints.append(Blueprint(self, blueprint))
        return blueprints

    @property
    def services(self):
        ays_services = self.ayscl.api.ays.listServices(self.model.get('name')).json()
        services = list()
        for service in ays_services:
            services.append(Service(self, service))
        return services

    @property
    def runs(self):
        ays_runs = self.ayscl.api.ays.listRuns(self.model.get('name')).json()
        runs = list()
        for run in ays_runs:
            runs.append(Run(self, run))
        return runs

    def blueprint_create(self, name, blueprint):
        data = j.data.serializer.json.dumps({'name': name, 'content': blueprint})

        try:
            resp = self.ayscl.api.ays.createBlueprint(data, self.model["name"], headers=None)

        except Exception as e:
            return

    def blueprint_execute(self, name=None, blueprint=None):
        if name is None:
            for blueprint in sorted(self.blueprints):
                try:
                    resp = self.ayscl.api.ays.executeBlueprint('', blueprint.model.get('name'), self.model.get('name'), headers=None)
                    return resp
                except Exception as e:
                    return
        else:
            if blueprint is not None:
                data = j.data.serializer.json.dumps({'name': name, 'content': blueprint})
            else:
                data = ''

            try:
                resp = self.ayscl.api.ays.executeBlueprint(data, name, self.model.get('name'), headers=None)
                return resp

            except Exception as e:
                return

    def run_execute(self, name=None, callback=None, yes=False):
        try:
            resp = self.ayscl.api.ays.createRun(data=None, repository=self.model["name"], query_params={'simulate': True, 'callback_url': callback})
        except Exception as e:
            print("error during execution of the run: {}".format(_extract_error(e)))
            return


        run = resp.json()
        if len(run['steps']) <= 0:
            print("Nothing to do.")
            return

        if yes == False:
            resp = j.tools.console.askYesNo('Do you want to execute this run ?', True)
            if resp is False:
                runid = run['key']
                self.ayscl.deleteRun(runid=runid, repository=self.model["name"])
                return

        try:
            resp = self.ayscl.api.ays.executeRun(data=None, runid=run['key'], repository=self.model["name"])
        except Exception as e:
            print("error during execution of the run: {}".format(_extract_error(e)))
            return

        print("execution of the run started: {}".format(run['key']))
        return run['key']


class Blueprint:
    def __init__(self, repository, model):
        self.repository = repository
        self.model = model


    def __repr__(self):
        return "blueprint: %s" % (self.model["name"])

    __str__ = __repr__

class Service:
    def __init__(self, repository, model):
        self.repository = repository
        self.model = model


    def __repr__(self):
        return "service: %s" % (self.model["name"])

    __str__ = __repr__

class Run:
    def __init__(self, repository, model):
        self.repository = repository
        self.model = model


    def __repr__(self):
        return "run: %s" % (self.model["key"])

    __str__ = __repr__
