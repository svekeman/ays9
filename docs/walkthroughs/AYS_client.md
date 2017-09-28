# Use the JumpScale client for AYS

## preparation

Install ZeroTier (optionally):
```bash
curl -s https://install.zerotier.com/ | sudo bash
```

Start ZeroTier daemon (optionally):
```bash
zerotier-one -d
```

Join ZeroTier network (optionally):
```bash
ZT_ID=""
zerotier-cli join $ZT_ID
```

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

Connect to you AYS server:
```python
base_uri="http://172.25.0.238:5000"
cl=j.clients.atyourservice.get2(base_uri)
```

List all repositories:
```bash
client.repositories.list()
```

Create a new repository:
```bash
repo_name = "4test2"
git_url = "http://gitrepo"
repo=cl.repositories.create(repo_name, git_url)
```

Or use an existing repository:
```bash
repo=cl.repositories.get(repo_name)
```

Read blueprint from a file:
```python
file_name="vdc.bp"
blueprint_file = open(file_name,'r')
blueprint = blueprint_file.read()
```

Create a blueprint:
```python
bp_name="myvdc.yaml"
bp=repo.blueprints.create(bp_name, blueprint)
```

Or use an existing blueprint:
```bash
bp=repo.blueprints.get(bp_name)
```

Execute the blueprint:
```python
resp=b.execute()
```

Check result:
```python
resp.content
```

Check created services:
```python
r.services.list()
```

Create a run:
```pyton
key=r.runs.create()
```

List all runs:
```python
r.runs.list()
```

Check run:
```python
myrun=r.runs.get(key)
myrun.model
```


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
