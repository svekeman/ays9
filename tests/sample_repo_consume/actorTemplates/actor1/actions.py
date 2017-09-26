def firstact(job):
    import json
    cl = j.clients.atyourservice.get().api.ays
    content = """
    actor2__test:
        test: 'nonexistant'
    """
    data = {
        'name': 'wrong_consume',
        'content': content
    }
    cl.createBlueprint(data, job.service.aysrepo.name)
    try:
        cl.executeBlueprint(None, 'wrong_consume', job.service.aysrepo.name)
    except :
        cl.deleteBlueprint('wrong_consume', job.service.aysrepo.name)
        print("success")



def secondact(job):
    import time
    print("from secondact")
    time.sleep(50)
