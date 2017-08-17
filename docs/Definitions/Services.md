## Service

A _service_ is a deployed unique instance of an _actor_.

For example a Docker application running on a host node is an service instance of an actor template for that Docker application, for which there is a version-controlled actor specific to that environment.

Read the section about the [Life cycle of an service instance](../Service-Lifecycle.md) for more details.


### Service Name & Role

Each AYS service has a name and a role.

For example in `node.ovc`:

- The name of the service is `node.ovc`
- The role of the service is `node`. So a role is the first part of the name before the `.` (dot). Multiple actor template can have the same role, but a name needs to be unique.

Roles are used to define categories of actors.

For instance, "node.physical", "node.docker" and "node.kvm" all serve the role "node".


```toml
!!!
title = "Services"
tags= ["ays","def"]
date = "2017-03-02"
categories= ["ays_def"]
```
