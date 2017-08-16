
# config.yaml (optional)
Contains information about the actor behavior and how services interact with each other through:
- Links which can be:
    - Parenting, for more details see [Parents & Children](../Definitions/Parents-Children.md)
    - Consumption, for more details see [Producers & Consumers](../Definitions/Producers-Consumers.md)
- [Recurring actions](#Recurring Actions), specifying repeatedly occurring actions
- [Events](#Events)
- [Timeouts](#Timeouts)

See [Example](#Example) for complete usage of these configs.

## Recurring Actions:
Recurring actions are actions that are periodically (configured) fired up actions that are managed by the AYS server.
They are executed asynchronously with no runs.

## Events

To fire a new event you need to push a `payload` on the command queue. The payload has two keys:
- `command`, where the event_name is set.
-  `args`, which is a list of event arguments.

#### Example
Here we have a simple example around two actors `producer`and `consumer`, where `producer` executes a `longjob` and consumer wants to execute some specific action on that event.

- producer
    - schema.capnp
    ```yaml
    @0xe7f7fbc7a590904f;
    struct Schema {
        msg @0 :Text;
    }
    ```

    - actions.py
    ```python
    def install(job):
        sv = job.service
        cl = j.clients.atyourservice.get().api
        data = {'command': 'producer_installed'}
        cl.webhooks.webhooks_events_post(data=data)


    def longjob(job):
        from time import sleep
        sleep(5)
        cl = j.clients.atyourservice.get().api
        data = {'command': 'producer_longjob_done'}
        cl.webhooks.webhooks_events_post(data)

    ```

- Consumer

    - actions.py

    ```python
    def init(job):
        service = job.service
        # SET UP EVENT HANDLERS.
        handlers_map = [('producer_installed', ['on_prod_installed']),
                        ('producer_longjob_done', ['on_prod_longjob']),]

        for (event, callbacks) in handlers_map:
            service.model.eventFilterSet(channel='webservice', command=event, actions=callbacks)
        service.saveAll()


    def on_prod_installed(job):
        print("*************Producer done with install.")

    def on_prod_longjob(job):
        print("************Producer done with the long job")

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
