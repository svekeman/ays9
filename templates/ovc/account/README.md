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
```
