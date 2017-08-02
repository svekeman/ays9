# template: disk.ovc

## Description:

This actor template represents a disk in ovc to be used later on by other services.

## Schema:
 - size: disk size in GB.
 - type: type of disk boot or normal.
 - description: description of disk. 
 - maxIOPS: max inputs outputs per second.
 - devicename: device name.
 - ssdSize: ssd size always available , will default to 10
 - location: location of the resource on cloud (i.e du-conv-2)

Replace \<with actual value \>

## Example for creating disks
```yaml
g8client__env:
    url: '<env_url>'
    login: '<login>'
    password: '<password>'
    account: '<account>'

disk.ovc__disk1:
    size: <disk size>
    g8client: 'env'
    devicename: '<disk name>'
    description: '<Description of the disk>'
    type: '<B or D. B for Boot and D for Data>'
    location: '<location of the disk>'

actions:

  - action: install
    actor: g8client
    service: env

  - action: create
    actor: disk.ovc
    service: disk1
```

## Example for deleting disks
```yaml
g8client__env:
    url: '<env_url>'
    login: '<login>'
    password: '<password>'
    account: '<account>'

disk.ovc__disk1:
    devicename: '<disk name>'

actions:

  - action: install
    actor: g8client
    service: env

  - action: delete
    actor: disk.ovc
    service: disk1
```

## Example for limit IO for disks
(note that the disk MUST be attached to a machine)
```yaml
g8client__env:
    url: '<env_url>'
    login: '<login>'
    password: '<password>'
    account: '<account>'

disk.ovc__disk1:
    devicename: '<disk name>'
    maxIOPS: 100

actions:

  - action: install
    actor: g8client
    service: env

  - action: limit_io
    actor: disk.ovc
    service: disk1
```

## Example for using disk with other services:

```yaml
sshkey__demo:

g8client__env1:
    # url: 'du-conv-3.demo.greenitglobe.com'
    url: '<env url>'
    login: '<login>'
    password: '<password>'
    account: '<account name>'

vdcfarm__vdcfarm1:

vdc__scality:
    vdcfarm: 'vdcfarm1'
    g8client: 'env1'
    location: '<location>'

disk.ovc__disk1:
  size: 1000

s3__demo:
    vdc: 'scality'
    disk:
      - 'disk1'
    domain: 'mystorage.com'
```