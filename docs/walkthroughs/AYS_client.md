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
