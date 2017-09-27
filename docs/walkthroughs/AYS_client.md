# Use the JumpScale client for AYS

## List all repositories

```python
ayscl = j.clients.atyourservice.get(base_uri='http://localhost:5000')
repositories=ayscl.api.ays.listRepositories()
repositories.json()
```

## Create a repository

```python
data={'name': 'test', 'git_url': 'http://whatever'}
ayscl = j.clients.atyourservice.get(base_uri='http://localhost:5000')
ayscl.api.ays.createRepository(data)
```

## Use a blueprint template
...

## Get JWT for interacting with the OpenvCloud API

See: https://gig.gitbooks.io/ovcdoc_public/content/API/GettingStarted.html

```bash
CLIENT_ID="..."
CLIENT_SECRET="..."
JWT=$(curl -d 'grant_type=client_credentials&client_id='"$CLIENT_ID"'&client_secret='"$CLIENT_SECRET"'&response_type=id_token' https://itsyou.online/v1/oauth/access_token)
```

## Create a blueprint for creating a VDC

```yaml
g8client__g8:
  url: 'be-gen-1.demo.greenitglobe.com'
  jwt: '...'
  account: 'myaccount'

vdc__testvdc10:
  g8client: 'g8'
  location: 'be-gen-1'

actions:
  - action: install
```


## Use the experimental AYS client

```python
file_name="vdc.bp"
blueprint_file = open(file_name,'r')
blueprint = blueprint_file.read()

client=j.clients.atyourservice.get2()
repository = client.repository_get("...")

```

Three  options.

**First option**, in two steps:
```bash
resp = repository.blueprint_create("myvdc.yaml", blueprint)
resp = repository.blueprint_execute("myvdc.yaml")
```

**Second option**, is the same as the first option, but ommitting the last argument in the second command, which will execute all blueprints in alphabetical order:

```bash
resp = repository.blueprint_create("myvdc.yaml", blueprint)
resp = repository.blueprint_execute()
```

**Third option**, in one step:
```bash
resp = repository.blueprint_execute("myvdc.yaml", blueprint)
```

Checking the response:
```bash
resp.content
```




```
