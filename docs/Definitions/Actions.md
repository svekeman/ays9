# Actions

AYS services are controlled through their actions, which are implemented as Python functions in their `actions.py` files. Each function corresponds to an action.

See [Actor Template Files](../ActorTemplateFiles/Actor.md) for an example of two actions: `install(job)` and `uninstall(job)`.

Actions are executed after they have been scheduled for execution.

Actions can get scheduled for execution in two ways:
- As a result of executing a blueprint that includes an `actions:` section; see [Blueprints](Blueprints.md) for more details
- Because the action was scheduled for recurring execution as specified in the `config.yaml` of the actor template; see [Actor Configuration](../ActorTemplateFiles/Config.md) for more details
- Triggered by an AYS event for which the action was registered as an event handler; see [Events](Events.md) for more details


scheduled for execution through blueprints, and are actually executed as part of a so call run.


## Action states

States of an action:

- scheduled
- ok
- error
- new

@todo copy all actions related stuff from the `ActorTemplatesFiles` here, and remove it there; same for all other `.md` files there
