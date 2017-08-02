# template: account

## Description:

This actor template represents an account to be used later on by other services.

## Schema:
    - description: Description of the account
    - g8client: G8client service name which will be consumed by account service;
    - maxMemoryCapacity: Maximum memory limit for this account default -1(unlimited);
    - maxCPUCapacity: Maximum memory limit for this account default -1(unlimited);
    - maxNumPublicIP: Maximum public ips number limit for this account default -1(unlimited);
    - maxDiskCapacity: Maximum Disk Capacity for this account default -1(unlimited);

Replace \<with actual value \>

### Example for creating account:

```yaml
g8client__env:
    url: '<env-url>'
    login: '<login user>'
    password: '<login password>'

account__account1:
    description: "<description of account>"
    g8client: env

actions:
  - action: install
```

### Example for listing disks associated with account:

```yaml
g8client__env:
    url: '<env-url>'
    login: '<login user>'
    password: '<login password>'

account__account1:

actions:
  - action: install
    actor: g8client
    service: env
  - action: list_disks
    actor: account
    service: account1
```
