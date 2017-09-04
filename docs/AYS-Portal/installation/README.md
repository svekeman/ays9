# Installation of an AYS Portal

In order to install an AYS Portal you need a JumpScale environment with the JumpScale Portal Framework installed.

This portal framework is installed as part of a JS9 Docker container when using the `-p` option during the build step, as documented in the [jumpscale/developer](https://github.com/Jumpscale/developer/blob/master/README.md)) repository.

Once the portal is installed on your JumpScale environment, you can add the AYS Portal by executing the following command in the interactive shell:
```python
j.tools.prefab.local.apps.atyourservice.install()
```

In case you didn't yet install the portal framework, you can use the option `install_portal` as follows:
```python
j.tools.prefab.local.apps.atyourservice.install(install_portal=True)
```
