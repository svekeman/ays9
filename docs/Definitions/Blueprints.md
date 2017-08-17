# AYS Blueprints

An AYS _blueprint_ is a [YAML](http://yaml.org/) file used as the entry point for interacting with AYS [Actor Templates](ActorTemplates.md). It describes the deployment of a specific application/setup or the the reality that will be deployed.

It does so by defining all service instances that make up a specific application, configuring them and describing how these AYS services instances interact with each other.

Example:

```yaml
actor__service1:
  configuration_parameter: value

actor__service2:
  configuration_parameter: value

actor_with_dependencies__name:
  key:
      - service1
      - service2
```

The above example deploys two `actors` and an `actor_with_dependencies` where `actor_with_dependencies` [consumes](Producers-Consumers.md)/uses those services.

```toml
!!!
title = "AYS Blueprints"
tags= ["ays","def"]
date = "2017-03-02"
categories= ["ays_def"]
```
