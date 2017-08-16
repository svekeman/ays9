# AYS Template Repo

AYS actor template repositories contain all the metadata defining the lifecycle of a service, from pre-installation to monitoring.

An example are the available [templates](../../templates), defining the full life cycle of all JumpScale services.

You can add AYS template repositories by using provided API or by creating a repo under `/opt/code`.
The AYS server will clone the repositories as subdirectories of `/opt/code/$type/`:

- Repositories from GitHub are cloned into `/opt/code/github`

  - So `https://github.com/Jumpscale/ays9` is cloned into `/opt/code/github/jumpscale/ays9`

- Repositories from other Git systems are cloned into `/opt/code/git/`


```
!!!
title = "AYS Template Repo"
date = "2017-04-08"
tags = []
```
