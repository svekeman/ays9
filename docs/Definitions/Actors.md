# Actors

The actor of an AYS service is actually the combination of the files in the `actors/<actor-name>` subdirectory of the AYS repo:
- `actions.py`: copy of the `actions.py` from the actor template
- `schema.capnp`: copy of the `schema.capnp` from the actor template
- `actor.json`: repository-specific metadata of all actions and events as defined in the actor template

All AYS services in the repository are instantiated from the actor as defined in the `actors` subdirectory. The `actions.py` Python code for instance is the actual code that will be executed by the actions of all AYS services that are instantiated from the actor.

By having a local copy in the `actors` directory of each actor template that is used in the AYS repository, AYS allows to have different versions - and thus behavior - of the AYS services per repository. And since an actor is part of the AYS repository you can keep track of the changes, again per repository.
