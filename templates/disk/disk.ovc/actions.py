def init_actions_(service, args):
    dependencies = {
        'create': ['init'],
        'limit_io': ['init'],
        'delete': ['init'],
    }
    return dependencies


def init(job):
    service = job.service
    if service.model.data.type and service.model.data.type.upper() not in ["D", "B"]:
        raise j.exceptions.Input("disk.ovc's type must be data (D) or boot (B) only")
    if 'g8client' not in service.producers:
        raise j.exceptions.AYSNotFound("no producer g8client found. cannot continue init of %s" % service)


def create(job):
    service = job.service
    g8client = service.producers["g8client"][0]
    client = j.clients.openvcloud.getFromService(g8client)
    account = client.account_get(g8client.model.data.account, create=True)
    for loc in client.locations:
        if loc['name'] == service.model.data.location:
            location = loc
            break
    else:
        raise j.exceptions.AYSNotFound("Location not found. cannot continue init of %s" % service)

    account.create_disk(
        name=service.model.data.devicename,
        gid=location['gid'],
        description=service.model.data.description,
        size=service.model.data.size,
        type=service.model.data.type,
        ssd_size= service.model.data.ssdSize
    )


def delete(job):
    service = job.service
    g8client = service.producers["g8client"][0]
    client = j.clients.openvcloud.getFromService(g8client)
    account = client.account_get(g8client.model.data.account, create=True)
    for disk in account.disks:
        if disk['name'] in [service.model.data.devicename, service.model.dbobj.name]:
            disk_to_delete = disk
            break
    else:
        raise j.exceptions.AYSNotFound("Data Disk was not found. cannot continue init of %s" % service)
    account.delete_disk(disk_to_delete['id'])


def limit_io(job):
    service = job.service
    g8client = service.producers["g8client"][0]
    client = j.clients.openvcloud.getFromService(g8client)
    account = client.account_get(g8client.model.data.account, create=True)
    for disk in account.disks:
        if disk['machineId'] and disk['name'] in [service.model.data.devicename, service.model.dbobj.name]:
            disk_to_set = disk
            break
    else:
        raise j.exceptions.AYSNotFound("Data Disk was not found. cannot continue init of %s" % service)
    client.api.cloudapi.disks.limitIO(diskId=disk_to_set['id'], iops=service.model.data.maxIOPS)
