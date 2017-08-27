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


    
!!!
title = "Events"
date = "2017-04-08"
tags = []
```
