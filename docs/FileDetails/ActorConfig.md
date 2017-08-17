
# config.yaml (optional)
Contains information about the actor behavior and how services interact with each other through:
- Links which can be:
    - Parenting, for more details see [Parents & Children](../Definitions/Parents-Children.md)
    - Consumption, for more details see [Producers & Consumers](../Definitions/Producers-Consumers.md)
- [Recurring actions](#Recurring Actions), specifying repeatedly occurring actions
- [Timeouts](#Timeouts)

See [Example](#Example) for complete usage of these configs.

## RecurringActions:
Recurring actions are actions that are periodically (configured) fired up actions that are managed by the AYS server.
They are executed asynchronously with no runs.

#### Example
Assuming actions `monitor` is defined in an actor template's `actions.py`

In config.yaml
```yaml
recurring:
    - action: monitor
      period: 30s # will be triggered every 30 seconds
      log: True # Will keep its logs in the job model
```

## Timeouts:
Any action defined in an actor can either have the defaut timeout (3000 seconds) or have its own timeout configured.

This timeout is configured on actor level and is applied on all its services

#### Example
Assuming actions `action1` and `action2` are defined in an actor template's `actions.py`

In config.yaml
```yaml
timeouts:
    - action1: 10s # Action1 will timeout in 10 seconds
    - action2: 5m # Action2 will timeout in 5 minutes
```

## Config file example:
  ```yaml
  links:
      parent:
          role: something
          auto: False
          #if not same as role name
          argname: something

      consume:
          -   role: somethinconsume
              min: 1
              max: 1
              auto: False
              #if not same as role name
              argname: something
          -   role: somethinconsumeb
              #default is min=max=1, argname same as role

  recurring:
      -   action: monitor
          period: 30s
          log: True

      -   action: dosomething
          period: 1m
          log: True

  timeouts:
      - action1: 10s
      - action2: 5m

  events:
      -   channel: telegram
          command: install_mynode
          actions:
              - install
              - actionX
          log: True
          role: node.ssh
          service: mynode
          tags: color:red
          secrets:
              - 1234
      -   command: stop
          actions: stop,kill
          log: False
          secrets:  1234
      -   command: issue_delete
          role: issue
          instance: myissue
  ```
