# AYS Blueprints

An AYS blueprint is a YAML file for interacting with AYS.

Through a blueprint you specify to AYS what needs to be done.

Blueprints can describe any of the following:
- a full application setup in one single blueprint
- what needs to be changed to the existing setup, by only including the parts of the initial blueprint that require changes
- the components that need to be added to the current application setup
- actions that need to be executed by the AYS services

Blueprints actually contain any combination of the following data:
- AYS service definitions, and/or changes to apply to previously defined AYS services
- Actions that need to be scheduled for executing

By having AYS process blueprints you actually:
- Instantiate AYS services, or change the attributes of previously instantiated AYS services
- And let the AYS services do the actual work through their actions

Example:

```yaml
actorX__service1:
  configuration_parameter: value1

actorX__service2:
  configuration_parameter: value2

actorY__service3:
  key:
      - service1
      - service2

actions:
  - action: install
```

The above blueprint describes three AYS services:
- the first two AYS services, `service1` and `service2`, are both instances on the same actor `actorABC`
- the third AYS service, `service3`, is an instance of the actor `actor_with_dependencies`, which consumes [consumes](Producers-Consumers.md) (uses) the two other AYS services

It also contains an `actions` section specifying that the `install` action of all AYS service should be scheduled. More details about the actions section here below.


## Actions section

You can schedule actions using blueprints by including an actions section.

A simple example, as used above:

```yaml
actions:
    - action: {ACTION-NAME}
```

In this case it will execute the action {ACTION-NAME} on all AYS services.

You can be more specific by using the attributes `actor`, `service` and `force`:
```yaml
actions:
    - action: {ACTION-NAME}
      actor: {ACTOR-NAME}
      service: {SERVICE-NAME}
      force: false
```

Attribute values:
- `service`: is used to specify the execution of action `{ACTION-NAME}` of a specific AYS service `{SERVICE-NAME}`
- `actor`: is used to specify the execution of action only on services of actor `{ACTOR-NAME}`
- `force` (false/true): is used to reschedule an action to get picked up again by the **Run Scheduler**, for more information on this see [Runs](../Definitions/Runs.md)


## Using the AYS command line tool

You can use the AYS command line tool to create actions on the fly using the `ays action` command:
- `ays action install`
- `ays action ACTIONNAME -a ACTORNAME`
- `ays action ACTIONNAME -s SERVICENAME`
- `ays action ACTIONNAME -s SERVICENAME -f`

Check `ays action --help`.

Also see: [How to debug actor templates](../Howto/Debug_actor_template/README). 
