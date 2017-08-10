def init(job):
    service = job.service
    aysrepo = service.aysrepo
    sshactor = aysrepo.actorGet("sshkey")
    k1 = sshactor.serviceCreate("k1")
    k2 = sshactor.serviceCreate("k2")
    k3 = sshactor.serviceCreate("k3")

    service.consume(k1)
    service.consume(k2)
    service.consume(k3)


def install(job):
    service = job.service
    aysrepo = service.aysrepo
    k1 = aysrepo.serviceGet("sshkey", "k1")
    k2 = aysrepo.serviceGet("sshkey", "k2")
    k3 = aysrepo.serviceGet("sshkey", "k3")
    k3.consume(k2)


    k1.save()
    k3.save()
    k2.save()



def stop(job):
    print("Stopping cons cons1")

def uninstall(job):
    print("uninstall cons cons1")


def processChange(job):
    args = job.model.args
    category = args.pop('changeCategory')    
    if category=="links":
        producers=args.pop("producer_removed", None)
        print("producer was removed ", producers)
        

def printme(job):
    print("Start job.printme>>>")
    print("End job.printme...")
