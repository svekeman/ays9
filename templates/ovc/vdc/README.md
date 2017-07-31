# template: vdc

## Description

This actor template creates a cloudspace (Virtual Data Center) on the specified environment. If required cloudspace already exists it will be used.

## Schema

- description: Description of the cloudspace.
- vdcfarm: Specify vdc group. If not specified group will be auto created.
- g8client: User login.
- account: Account used for this space(if doesn't exist will be created), if empty will use existing account that belongs to the specified user.
- location: Environment to deploy this cloudspace.
- uservdc: Users to have access to this cloudpsace. Name is name of user service to be consumed and accesstype is the user access right to this cloudspace.
- allowedVMSizes: Specify the allowed size ids for virtual machines on this cloudspace.
- cloudspaceID: id of the cloudspace (leave empty).
- maxMemoryCapacity: Cloudspace limits, maximum memory.
- maxCPUCapacity: Cloudspace limits, maximum CPU capacity.
- maxDiskCapacity: Cloudspace limits, maximum disk capacity.
- maxNumPublicIP: Cloudspace limits, maximum allowed number of public IPs.
- externalNetworkID: External network to be attached to this cloudspace.

## User access rights

Using process change it is possible to add, remove and update user access to the cloudspace. To add user after executing the run and creating the vdc, add a new user in the blueprint and execute the blueprint to trigger process change and add new user to the cloudspace or removing user by deleting the entry in the blueprint. changing the accesstype will update the user access when executing the blueprint.

## Example

```yaml
g8client__example:
    url: '<url of the environment>'
    login: '<username>'
    password: '<password>'
    account: '<account name>'

uservdc__usertest:
    password: 'test1234'
    email: 'fake@fake.com'
    groups:
      - user
    g8client: 'example'

vdcfarm__vdcfarm1:


vdc__cs2:
    description: '<description>'
    vdcfarm: 'vdcfarm1'
    g8client: 'example'
    account: '<account name>'
    location: '<name of the environment>'
    uservdc:
        - name: 'usertest'
          accesstype: 'ACDRUX'
    allowedVMSizes:
        - 1
        - 2
```
