
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
