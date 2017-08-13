def init_actions_(service, args):

    """

    this needs to returns an array of actions representing the depencies between actions.

    Looks at ACTION_DEPS in this module for an example of what is expected

    """
    # some default logic for simple actions
    return {

        'test': ['install']

    }


def test(job):
    """
    Test long actions
    """
    import sys
    import time
    RESULT_OK = 'OK : %s'
    RESULT_FAILED = 'FAILED : %s'
    RESULT_ERROR = 'ERROR : %s %%s' % job.service.name
    model = job.service.model
    model.data.result = RESULT_OK % job.service.name
    failures = []

    cl = j.clients.atyourservice.get().api.ays
    repo = "sample_repo_basicdelete"

    # prepare the repo.
    try:
        cl.executeBlueprint(data=None, repository=repo, blueprint="prepare.yaml")
    except Exception as ex:
        failures.append(str(ex))

    # execute run. (action install)
    run = cl.createRun(data=None, repository=repo).json()
    runid = cl.getRun(repository=repo, runid=run['key']).json()

    run = cl.executeRun(repository=repo, data=None, runid=runid).json()
    run = cl.getRun(repository=repo, runid=run['key']).json()
    while run['state'] != 'ok':
        time.sleep(2)
        run = cl.getRun(repository=repo, runid=runid).json()
   
   # delete knotconsumed 
    try:
        cl.executeBlueprint(data=None, repository=repo, blueprint="delete_knotconsumed.yaml")
    except Exception as ex:
        failures.append(str(ex))
    
    run = cl.createRun(data=None, repository=repo).json()
    runid = cl.getRun(repository=repo, runid=run['key']).json()

    run = cl.executeRun(repository=repo, data=None, runid=runid).json()
    run = cl.getRun(repository=repo, runid=run['key']).json()
    while run['state'] != 'ok':
        time.sleep(2)
        run = cl.getRun(repository=repo, runid=runid).json()


    expectedsteps = [[('knotconsumed', "stop")], [("knotconsumed", "uninstall")], [("knotconsumed", "delete")]] 
    tobesteps = []
    for step in run['steps']:
        for job in step['jobs']:
            tobesteps.append([(job['service_name'], job['action_name'])])
    for i, s in enumerate(tobesteps):
        if len(s) != len(expectedsteps[i]):
            failures.append("Expected step to have #{} jobs but it has #{} jobs.".format(len(s), len(expectedsteps[i])))
        for jidx, job in enumerate(s):
            expectedjob = expectedsteps[i][jidx]
            failures.append("Expected to have {}{} job but it has {}{}.".format(*expectedjob, *job)) 

    while run['state'] != 'ok':
        time.sleep(2)
        run = cl.getRun(repository=repo, runid=run['key']).json()

    # delete cons1  
    try:
        cl.executeBlueprint(data=None, repository=repo, blueprint="delete_cons1.yaml")
    except Exception as ex:
        failures.append(str(ex))
    
    run = cl.createRun(data=None, repository=repo).json()
    runid = cl.getRun(repository=repo, runid=run['key']).json()

    run = cl.executeRun(repository=repo, data=None, runid=runid).json()
    run = cl.getRun(repository=repo, runid=run['key']).json()
    while run['state'] != 'ok':
        time.sleep(2)
        run = cl.getRun(repository=repo, runid=runid).json()
    expectedsteps = [[('cons1', "stop")], [("cons1", "uninstall")], [("cons1", "delete")]]     
    tobesteps = []
    for step in run['steps']:
        for job in step['jobs']:
            tobesteps.append([(job['service_name'], job['action_name'])])
    for i, s in enumerate(tobesteps):
        if len(s) != len(expectedsteps[i]):
            failures.append("Expected step to have #{} jobs but it has #{} jobs.".format(len(s), len(expectedsteps[i])))
        for jidx, job in enumerate(s):
            expectedjob = expectedsteps[i][jidx]
            failures.append("Expected to have {}{} job but it has {}{}.".format(*expectedjob, *job)) 

    # delete kp  
    try:
        cl.executeBlueprint(data=None, repository=repo, blueprint="delete_kp.yaml")
    except Exception as ex:
        failures.append(str(ex))
    
    # execute run.
    run = cl.createRun(data=None, repository=repo).json()
    # run = cl.executeRun(repository=repo, data=None, runid=run.json()['key']).json()
    run = cl.getRun(repository=repo, runid=run['key']).json()

    expectedsteps = [[('kid', "stop")], [("kp", "stop"),("kid", "uninstall")], [("kp", "uninstall"), ("kid", "delete")], [("kp", "delete")]]
    tobesteps = []
    for step in run['steps']:
        for job in step['jobs']:
            tobesteps.append([(job['service_name'], job['action_name'])])
    for i, s in enumerate(tobesteps):
        if len(s) != len(expectedsteps[i]):
            failures.append("Expected step to have #{} jobs but it has #{} jobs.".format(len(s), len(expectedsteps[i])))
        for jidx, job in enumerate(s):
            expectedjob = expectedsteps[i][jidx]
            failures.append("Expected to have {}{} job but it has {}{}.".format(*expectedjob, *job)) 

    if failures:
        model.data.result = RESULT_FAILED % '\n'.join(failures)
