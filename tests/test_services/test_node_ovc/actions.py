def test_create(job):
    """
    Test Create node
    """
    import sys
    RESULT_OK = 'OK : %s'
    RESULT_ERROR = 'ERROR : %s %%s' % job.service.name
    model = job.service.model
    model.data.result = RESULT_OK % job.service.name
    repo = 'sample_node_ovc'
    client = j.clients.atyourservice.get().api.ays
    try:
        client.executeBlueprint(data=None, repository=repo, blueprint='create.yaml')
        run = client.createRun(data=None, repository=repo).json()
        client.executeRun(data=None, runid=run['key'], repository=repo)
        model.data.result = RESULT_OK % 'Node Created Successfully'
    except:
        model.data.result = RESULT_ERROR % str(sys.exc_info()[:2])
    finally:
        job.service.save()
        client.destroyRepository(data=None, repository=repo)


def test_delete(job):
    """
    Test Delete node
    """
    import sys
    RESULT_OK = 'OK : %s'
    RESULT_ERROR = 'ERROR : %s %%s' % job.service.name
    model = job.service.model
    model.data.result = RESULT_OK % job.service.name
    repo = 'sample_node_ovc'
    client = j.clients.atyourservice.get().api.ays
    try:
        client.executeBlueprint(data=None, repository=repo, blueprint='delete.yaml')
        run = client.createRun(data=None, repository=repo).json()
        client.executeRun(data=None, runid=run['key'], repository=repo)
        model.data.result = RESULT_OK % 'Node Deleted Successfully'
    except:
        model.data.result = RESULT_ERROR % str(sys.exc_info()[:2])
    finally:
        job.service.save()
        client.destroyRepository(data=None, repository=repo)
