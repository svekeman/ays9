def init(job):
    service = job.service
    aysrepo = service.aysrepo
    sshactor = aysrepo.actorGet("sshkey")
    k1 = sshactor.serviceCreate("k1")
    k2 = sshactor.serviceCreate("k2")
    k3 = sshactor.serviceCreate("k3")

def install(job):
    service = job.service
    aysrepo = service.aysrepo
    k1 = aysrepo.serviceGet("sshkey", "k1")
    k2 = aysrepo.serviceGet("sshkey", "k2")
    k3 = aysrepo.serviceGet("sshkey", "k3")
    k1.consume(k2)
    k3.consume(k2)
    k1.save()
    k3.save()
    k2.save()


def long1(job):
    print("JOB LONG1 STARETED")
    from asyncio import sleep, get_event_loop
    async def inner(job):
        while True:
            print("IN LOOP")
            await sleep(5)
    return inner(job)
