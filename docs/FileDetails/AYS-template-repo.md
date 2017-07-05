# AYS Template Repo

AYS actor template repositories contain all the metadata defining the lifecycle of a service, from pre-installation to monitoring.

An example are the available [templates](../../templates), defining the full life cycle of all JumpScale services.

You can add AYS template repositories by using provided API or by creating a repo under `/opt/code`.
The AYS server will clone the repositories as subdirectories of `/opt/code/$type/`:

- Repositories from GitHub are cloned into `/opt/code/github`

  - So `https://github.com/Jumpscale/ays9` is cloned into `/opt/code/github/jumpscale/ays9`

- Repositories from other Git systems are cloned into `/opt/code/git/`

Each AYS actor template has following files:

- **schema.capnp**

  - Which is the schema for the service instance metadata relevant for an instance of the service

  - Has parameter definitions used to configure the service

  - Example:

    ```
    @0x8e49424dcf7a20be;
    struct Schema {
    	os @0 :Text;
    	fs @1 :List(Text);
    	docker @2 :Text;
    	hostname @3 :Text;
    	image @4 :Text = "ubuntu";
    	ports @5 :List(Text);
    	volumes @6 :List(Text);
    	cmd @7 :Text;
    	sshkey @8 :Text;
    	id @9 :Text;
    	ipPublic @10 :Text;
    	ipPrivate @11 :Text;
    	sshLogin @12 :Text;
    	sshPassword @13 :Text;

    }
    ```

- **config.yaml (optional)**

  - Contains information about the services behavior and how they interact with each other through:

    - Parenting, for more details see [Parents & Children](../Definitions/Parents-Children.md)
    - Consumption, for more details see [Producers & Consumers](../Definitions/Producers-Consumers.md)
    - Recurring actions, specifying repeatedly occurring actions
    - Events, for more details see [Events](../Events.md)
  - Example:
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

- **actions.py** (optional)
  - Defines the behavior of the service, by defining the service actions
  - Example:
    ```py
    def input(job):
        r = job.service.aysrepo

        if "node" in job.model.args:
            res = job.model.args
            res["os"] = res["node"]
            res.pop("node")
            job.model.args = res

        return job.model.args
    ```
```
!!!
title = "AYS Template Repo"
date = "2017-04-08"
tags = []
```
