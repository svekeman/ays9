from js9 import j

class Client:
    def __init__(self, base_uri="https://localhost:5000"):
        self.ayscl = j.clients.atyourservice.get(base_uri)


    def create(self, name, git):
        """
        create a new AYS repository
        """
        if git is None:
            #print("you have to specify an gi repository using --git")
            return

        if name is None:
            #name = j.sal.fs.getBaseName(j.sal.fs.getcwd())
            return

        data = j.data.serializer.json.dumps({'name': name, 'git_url': git})

        try:
            resp = self.ayscl.api.ays.createRepository(data=data)
            #print("AYS repository created at {}".format(resp.json()['path']))

        except Exception as e:
            print("Error during creation of the repository: {}".format(_extract_error(e)))
