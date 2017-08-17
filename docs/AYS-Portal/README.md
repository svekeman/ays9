# G8 Cockpit

The G8 Cockpit provides a REST API, web portal and chatbot for managing and consuming aggregated G8 capacity through one more G8 Masters using AYS blueprints and AYS service templates, leveraging a single identity controlled by ItsYou.online.

# AYS Portal

AYS services and templates are visualized in the **AYS Portal**.

Using the portal it is possible to view the repositories and templates in the system. It is possible to navigate to AYS repos and perform various actions such as executing blueprints, editing blueprints, viewing the runs and the service instances created.

The portal is installed when using the `-p` option during the building of js9(see [js9 installation](https://github.com/Jumpscale/developer/blob/master/README.md)).

To add AYS app to the portal, use the following command:

`j.tools.prefab.local.apps.atyourservice.install()`

If portal is not installed you can use the option `install_portal` as follows:

`j.tools.prefab.local.apps.atyourservice.install(install_portal=True)`

For more information about the portal check the docs at [portal](https://github.com/Jumpscale/portal9/tree/master/docs/AYS/walkthrough)

```
!!!
title = "AYS Portal"
date = "2017-04-08"
tags = []
```
