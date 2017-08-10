def install(job):
    service = job.service
    aysrepo = service.aysrepo
    kp = aysrepo.serviceGet("sshkey", "kp")
    k1 = aysrepo.serviceGet("sshkey", "k1")
    k1.consume(kp)
    k1.save()


def printme(job):
    print("Start job.printme>>>")
    print("End job.printme...")
