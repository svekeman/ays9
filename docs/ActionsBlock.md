# Actions Block

You can schedule actions using blueprints by specifying actions block


```
actions:
    - action: ACTION NAME


```
in this case it will execute that action on all services.

Typical use case is calling `action install` on all services after services are `initilized` or `initted`


## action configuration
```
actions:
    - action: ACTIONNAME
      actor: ACTORNAME
      service: SERVICENAME
      force: false
```

- service: is used to specify the execution of action `ACTIONNAME` on a certain service `SERVICENAME`
- actor: is used to specify the execution of action only on services of actor `ACTORNAME`

- force (false/true): is used to `reschedule` action `ACTIONNAME` even if its state is `ok` to get picked up again by the `runscheduler`
force has a special meaning in the `delete action` context if it's set to `False` it'll execute checks if the delete action is doable and won't break `parent/child` or the minimum required producers of a current consumer.


## using the commandline
You can use the commandline to create action on the fly using `ays action`
- `ays action install` 
- `ays action ACTIONNAME -a ACTORNAME`
- `ays action ACTIONNAME -s SERVICENAME`
- `ays action ACTIONNAME -s SERVICENAME -f` 

check `ays action --help`