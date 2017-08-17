## Actor Templates


An actor template defines the full life cycle from pre-installation and installation to upgrades and monitoring of a service.

 More specifically an actor template describes:

- The parameters to configure a service
- How a service behaves (actions of a service)
- How a service interacts with other services (Can be [parent/child](Parents-children.md) or [producer/consumer](Producers-Consumers.md) links)

All this is described in the actor template files:

- [config.yaml](../FileDetails/ActorConfig.md)
- [schema.capnp](../FileDetails/ActorSchema.md)
- [actions.py](../FileDetails/ActorActions.md)


```toml
!!!
title = "AYS Template Recipe"
tags= ["ays","def"]
date = "2017-03-02"
categories= ["ays_def"]
```
