
# template: ovc.account

## Description:
This actor template is responsible for creating an account on any openVCloud environment.

## Schema:

- description: Arbitrary description of the account. **Optional**

- g8client: Name of the g8client used to connect to the environment.

- accountusers: List of usernames that will be authorized.

- accountID: The ID of the account. **Filled in automatically, don't specify it in the blueprint**

- maxMemoryCapacity: The limit on the memory capacity that can be used by the account.

- maxCPUCapacity: The limit on the CPUs that can be used by the account.

- maxNumPublicIP: The limit on the number of public IPs that can be used by the account.

- maxDiskCapacity: The limit on the disk capacity that can be used by the account.



## Example for creating an account

```yaml
g8client__env:
  url: '<env_url>'
  login: '<username>'
  password: '<password>'
  account: '<account>'

account__acc:
  description: '<random>'
  g8client: 'env'
  accountusers:
    - '<username>'
  maxMemoryCapacity: <value>
  maxCPUCapacity:  <value>
  maxDiskCapacity: <value>
  maxNumPublicIP: <value>

actions:
  - action: install
=======
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
